# Week 3 — Data Processing and Exploitation

## 1. Objective

The objective of Week 3 was to transform raw cyber threat intelligence collected during
the previous stage into structured and usable IOC data. The practical work focused on
data validation, normalization, filtering, correlation, MISP preparation/import, and the
creation of a basic Sigma detection rule.

## 2. Data Processing Method

Raw CTI feeds and OSINT results often contain inconsistent formatting, duplicate
indicators, invalid values, and records with different confidence levels. To address this,
a Python-based IOC processing pipeline was implemented.

The input dataset uses the fields:

- indicator;
- IOC type;
- source;
- confidence score;
- description;
- tags.

The pipeline performs the following processing stages:

1. **Type normalization.** Common aliases such as `ip-dst`, `ipv4`, and `hostname`
   are mapped to canonical internal types.
2. **Validation.** IP addresses are parsed with Python's `ipaddress` module; domains,
   URLs, and cryptographic hashes are checked for valid structure.
3. **Canonicalization.** Domain names and hashes are converted to lowercase,
   trailing dots are removed from domains, default URL ports are removed, and URL
   fragments are discarded.
4. **Confidence filtering.** Indicators below the minimum confidence threshold are rejected.
5. **Correlation.** Duplicate normalized indicators are merged. Their source lists and
   tags are combined, the highest confidence score is retained, and a sightings counter
   is increased.
6. **Export.** Clean indicators are written to CSV and converted into a MISP event JSON structure.

This processing reduces noise and produces a consistent dataset for threat-intelligence
and SIEM workflows.

## 3. Processing Results

Run:

```bash
python3 scripts/process_iocs.py
```

The generated files are:

- `output/normalized_iocs.csv`;
- `output/rejected_iocs.csv`;
- `output/stats.json`;
- `output/misp_event.json`.

The included dataset intentionally demonstrates:

- duplicate correlation across different sources;
- low-confidence filtering;
- malformed IOC rejection.

### Evidence

**Figure 1. IOC processing command output**

> Insert screenshot here.

**Figure 2. Normalized IOC dataset**

> Insert screenshot here.

**Figure 3. Rejected IOC records**

> Insert screenshot here.

## 4. MISP Deployment and Import

MISP is used to store, correlate, and manage the processed indicators. The lab uses the
official Docker deployment. After MISP is started, `output/misp_event.json` can be imported
through the web interface or through `scripts/import_to_misp.py`.

The generated event includes IP addresses, domains, URLs, and hashes. Source,
confidence, sighting count, descriptions, and local tags are preserved in the exported data.

### Evidence

**Figure 4. Running MISP Docker containers**

> Insert screenshot here.

**Figure 5. Imported MISP event**

> Insert screenshot here.

**Figure 6. MISP Attributes table**

> Insert screenshot here.

## 5. Sigma Detection Rule

The file:

```text
sigma/suspicious_powershell_encoded_command.yml
```

detects PowerShell or PowerShell Core process creation with encoded-command arguments.
It is mapped to MITRE ATT&CK technique **T1059.001 — PowerShell** under the
**Execution** tactic.

This links CTI processing with detection engineering and prepares the project for later
SIEM and threat-hunting work.

## 6. Validation

Automated tests cover:

- domain normalization;
- URL canonicalization;
- duplicate correlation;
- low-confidence filtering;
- invalid IOC rejection.

Run:

```bash
python3 -m unittest discover -s tests -v
```

## 7. Conclusion

Week 3 established the processing stage between OSINT collection and later SIEM analysis.
Raw indicators were normalized, validated, filtered, and correlated before being exported
as structured CTI. MISP provides a practical platform for operationalizing the processed
indicators, while the Sigma rule connects the CTI workflow to MITRE ATT&CK-aligned
detection engineering.
