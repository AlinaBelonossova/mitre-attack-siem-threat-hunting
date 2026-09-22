#!/usr/bin/env python3
"""
Import output/misp_event.json into a running MISP instance through the REST API.

Environment variables:
    MISP_URL
    MISP_API_KEY
    MISP_VERIFYCERT=true|false
"""

from __future__ import annotations

import json
import os
import ssl
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    event_path = root / "output" / "misp_event.json"

    url = os.environ.get("MISP_URL", "").strip().rstrip("/")
    api_key = os.environ.get("MISP_API_KEY", "").strip()
    verify_cert = truthy(os.environ.get("MISP_VERIFYCERT", "true"))

    if not url or not api_key:
        print("Missing MISP_URL or MISP_API_KEY.", file=sys.stderr)
        print("Example:", file=sys.stderr)
        print('  export MISP_URL="http://localhost"', file=sys.stderr)
        print('  export MISP_API_KEY="YOUR_KEY"', file=sys.stderr)
        print('  export MISP_VERIFYCERT="false"', file=sys.stderr)
        raise SystemExit(2)

    payload = event_path.read_bytes()

    request = Request(
        f"{url}/events/add",
        data=payload,
        method="POST",
        headers={
            "Authorization": api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    context = None
    if url.startswith("https://") and not verify_cert:
        context = ssl._create_unverified_context()

    try:
        with urlopen(request, context=context, timeout=60) as response:
            body = response.read().decode("utf-8", errors="replace")

    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"MISP returned HTTP {exc.code}", file=sys.stderr)
        print(body, file=sys.stderr)
        raise SystemExit(1)

    except URLError as exc:
        print(f"Could not connect to MISP: {exc}", file=sys.stderr)
        raise SystemExit(1)

    try:
        result = json.loads(body)
    except json.JSONDecodeError:
        print("MISP response was not JSON:")
        print(body)
        return

    event = result.get("Event", result)
    print("MISP import successful.")

    if isinstance(event, dict):
        if event.get("id"):
            print(f"Event ID:   {event['id']}")
        if event.get("uuid"):
            print(f"Event UUID: {event['uuid']}")
        if event.get("info"):
            print(f"Event info: {event['info']}")


if __name__ == "__main__":
    main()
