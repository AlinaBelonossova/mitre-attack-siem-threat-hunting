#!/usr/bin/env python3
"""
Week 3 IOC processing pipeline.

Input CSV:
    indicator,type,source,confidence,description,tags

Outputs:
    output/normalized_iocs.csv
    output/rejected_iocs.csv
    output/stats.json
    output/misp_event.json
"""

from __future__ import annotations

import argparse
import csv
import ipaddress
import json
import re
from collections import OrderedDict
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

TYPE_ALIASES = {
    "ip": "ip",
    "ipv4": "ip",
    "ipv6": "ip",
    "ip-src": "ip",
    "ip-dst": "ip",
    "domain": "domain",
    "hostname": "domain",
    "url": "url",
    "uri": "url",
    "md5": "md5",
    "sha1": "sha1",
    "sha-1": "sha1",
    "sha256": "sha256",
    "sha-256": "sha256",
}

MISP_TYPES = {
    "ip": "ip-dst",
    "domain": "domain",
    "url": "url",
    "md5": "md5",
    "sha1": "sha1",
    "sha256": "sha256",
}

HASH_LENGTHS = {"md5": 32, "sha1": 40, "sha256": 64}
DOMAIN_LABEL = re.compile(r"^(?!-)[a-z0-9-]{1,63}(?<!-)$")


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def canonical_type(raw_type: str) -> str:
    key = raw_type.strip().lower()
    if key not in TYPE_ALIASES:
        raise ValueError(f"unsupported IOC type: {raw_type}")
    return TYPE_ALIASES[key]


def _is_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def normalize_domain(value: str) -> str:
    domain = value.strip().rstrip(".").lower()
    if not domain or " " in domain or "." not in domain:
        raise ValueError("invalid domain")

    try:
        ascii_domain = domain.encode("idna").decode("ascii")
    except UnicodeError as exc:
        raise ValueError("invalid domain") from exc

    if len(ascii_domain) > 253:
        raise ValueError("invalid domain")

    labels = ascii_domain.split(".")
    if not all(DOMAIN_LABEL.fullmatch(label) for label in labels):
        raise ValueError("invalid domain")

    return ascii_domain


def normalize_url(value: str) -> str:
    value = value.strip()

    try:
        parts = urlsplit(value)
    except ValueError as exc:
        raise ValueError("invalid URL") from exc

    scheme = parts.scheme.lower()
    if scheme not in {"http", "https"} or not parts.hostname:
        raise ValueError("invalid URL")

    host = (
        str(ipaddress.ip_address(parts.hostname))
        if _is_ip(parts.hostname)
        else normalize_domain(parts.hostname)
    )

    try:
        port = parts.port
    except ValueError as exc:
        raise ValueError("invalid URL port") from exc

    if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        port = None

    netloc = host if port is None else f"{host}:{port}"
    path = parts.path or "/"

    # URL fragments are removed because they are not transmitted to the server.
    return urlunsplit((scheme, netloc, path, parts.query, ""))


def normalize_indicator(value: str, ioc_type: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("empty indicator")

    if ioc_type == "ip":
        return str(ipaddress.ip_address(value))

    if ioc_type == "domain":
        return normalize_domain(value)

    if ioc_type == "url":
        return normalize_url(value)

    if ioc_type in HASH_LENGTHS:
        h = value.lower()
        if len(h) != HASH_LENGTHS[ioc_type] or not re.fullmatch(r"[0-9a-f]+", h):
            raise ValueError(f"invalid {ioc_type}")
        return h

    raise ValueError(f"unsupported IOC type: {ioc_type}")


def split_tags(raw_tags: str) -> list[str]:
    tags = []
    for item in (raw_tags or "").replace(";", ",").split(","):
        tag = item.strip().lower()
        if tag and tag not in tags:
            tags.append(tag)
    return tags


def parse_confidence(raw: str) -> int:
    try:
        confidence = int(str(raw).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError("confidence is not an integer") from exc

    if not 0 <= confidence <= 100:
        raise ValueError("confidence must be between 0 and 100")

    return confidence


def process_rows(rows: list[dict], min_confidence: int = 50):
    correlated = OrderedDict()
    rejected = []

    stats = {
        "input_records": len(rows),
        "accepted_unique_indicators": 0,
        "correlated_duplicate_records": 0,
        "rejected_records": 0,
        "rejected_low_confidence": 0,
        "rejected_invalid": 0,
        "minimum_confidence": min_confidence,
    }

    for row_no, row in enumerate(rows, start=2):
        raw_indicator = (row.get("indicator") or "").strip()
        raw_type = (row.get("type") or "").strip()
        source = (row.get("source") or "unknown").strip() or "unknown"
        description = (row.get("description") or "").strip()

        try:
            ioc_type = canonical_type(raw_type)
            confidence = parse_confidence(row.get("confidence", "0"))
            normalized = normalize_indicator(raw_indicator, ioc_type)
        except Exception as exc:
            rejected.append({
                "row": row_no,
                "indicator": raw_indicator,
                "type": raw_type,
                "reason": str(exc),
            })
            stats["rejected_invalid"] += 1
            continue

        if confidence < min_confidence:
            rejected.append({
                "row": row_no,
                "indicator": normalized,
                "type": ioc_type,
                "reason": f"low confidence ({confidence} < {min_confidence})",
            })
            stats["rejected_low_confidence"] += 1
            continue

        key = (ioc_type, normalized)
        tags = split_tags(row.get("tags", ""))

        if key in correlated:
            item = correlated[key]
            stats["correlated_duplicate_records"] += 1

            if source not in item["_sources"]:
                item["_sources"].append(source)

            item["confidence"] = max(item["confidence"], confidence)
            item["sightings_count"] += 1

            for tag in tags:
                if tag not in item["_tags"]:
                    item["_tags"].append(tag)

            if description and description not in item["_descriptions"]:
                item["_descriptions"].append(description)

        else:
            correlated[key] = {
                "indicator": normalized,
                "type": ioc_type,
                "misp_type": MISP_TYPES[ioc_type],
                "confidence": confidence,
                "sightings_count": 1,
                "_sources": [source],
                "_tags": tags,
                "_descriptions": [description] if description else [],
            }

    accepted = []
    for item in correlated.values():
        accepted.append({
            "indicator": item["indicator"],
            "type": item["type"],
            "misp_type": item["misp_type"],
            "sources": ";".join(item["_sources"]),
            "confidence": item["confidence"],
            "sightings_count": item["sightings_count"],
            "description": " | ".join(item["_descriptions"]),
            "tags": ";".join(item["_tags"]),
        })

    stats["accepted_unique_indicators"] = len(accepted)
    stats["rejected_records"] = len(rejected)

    return accepted, rejected, stats


def read_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        required = {"indicator", "type", "source", "confidence", "description", "tags"}
        missing = required - set(reader.fieldnames or [])

        if missing:
            raise ValueError(f"missing CSV columns: {', '.join(sorted(missing))}")

        return list(reader)


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def misp_category(ioc_type: str) -> str:
    if ioc_type in {"ip", "domain", "url"}:
        return "Network activity"
    return "Payload delivery"


def build_misp_event(rows: list[dict]) -> dict:
    attributes = []

    for row in rows:
        comment_parts = [
            f"Sources: {row['sources']}",
            f"Confidence: {row['confidence']}/100",
            f"Sightings: {row['sightings_count']}",
        ]

        if row.get("description"):
            comment_parts.append(row["description"])

        if row.get("tags"):
            comment_parts.append(f"Tags: {row['tags']}")

        attributes.append({
            "type": row["misp_type"],
            "category": misp_category(row["type"]),
            "value": row["indicator"],
            "to_ids": bool(int(row["confidence"]) >= 70),
            "comment": "; ".join(comment_parts),
        })

    return {
        "Event": {
            "date": date.today().isoformat(),
            "info": "CTI Week 3 - Normalized and Correlated IOC Dataset",
            "distribution": "0",
            "threat_level_id": "2",
            "analysis": "1",
            "Tag": [
                {"name": "tlp:amber"},
                {"name": "course:cti-week3"},
            ],
            "Attribute": attributes,
        }
    }


def main() -> None:
    root = project_root()

    parser = argparse.ArgumentParser(
        description="Normalize, filter, and correlate IOC data."
    )
    parser.add_argument("--input", type=Path, default=root / "data" / "raw_iocs.csv")
    parser.add_argument("--output", type=Path, default=root / "output" / "normalized_iocs.csv")
    parser.add_argument("--rejected", type=Path, default=root / "output" / "rejected_iocs.csv")
    parser.add_argument("--stats", type=Path, default=root / "output" / "stats.json")
    parser.add_argument("--misp", type=Path, default=root / "output" / "misp_event.json")
    parser.add_argument("--min-confidence", type=int, default=50)
    args = parser.parse_args()

    if not 0 <= args.min_confidence <= 100:
        parser.error("--min-confidence must be between 0 and 100")

    rows = read_csv(args.input)
    accepted, rejected, stats = process_rows(rows, args.min_confidence)

    write_csv(
        args.output,
        accepted,
        [
            "indicator",
            "type",
            "misp_type",
            "sources",
            "confidence",
            "sightings_count",
            "description",
            "tags",
        ],
    )

    write_csv(
        args.rejected,
        rejected,
        ["row", "indicator", "type", "reason"],
    )

    args.stats.parent.mkdir(parents=True, exist_ok=True)
    args.stats.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    args.misp.parent.mkdir(parents=True, exist_ok=True)
    args.misp.write_text(
        json.dumps(build_misp_event(accepted), indent=2),
        encoding="utf-8",
    )

    print("Week 3 IOC processing complete")
    print(f"Input records:                {stats['input_records']}")
    print(f"Accepted unique indicators:   {stats['accepted_unique_indicators']}")
    print(f"Correlated duplicate records: {stats['correlated_duplicate_records']}")
    print(f"Rejected records:             {stats['rejected_records']}")
    print(f"  - low confidence:           {stats['rejected_low_confidence']}")
    print(f"  - invalid:                  {stats['rejected_invalid']}")
    print()
    print(f"Normalized CSV: {args.output}")
    print(f"Rejected CSV:   {args.rejected}")
    print(f"MISP event:     {args.misp}")
    print(f"Statistics:     {args.stats}")


if __name__ == "__main__":
    main()
