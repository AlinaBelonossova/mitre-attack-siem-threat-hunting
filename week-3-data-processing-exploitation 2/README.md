# Week 3 — Data Processing and Exploitation

This folder continues the CTI project after Week 1 (fundamentals) and Week 2 (data collection).

## Week 3 objectives

According to the course plan, Week 3 focuses on:

- data enrichment and correlation;
- MISP, Elastic Stack, and Sigma as processing/detection tools;
- deploying MISP and importing IOCs;
- filtering and normalizing collected threat-intelligence data.

This implementation provides a reproducible IOC-processing pipeline, a MISP-ready event,
an API import helper, and a Sigma rule.

## Project structure

```text
week-3-data-processing-exploitation/
├── README.md
├── .env.example
├── data/
│   └── raw_iocs.csv
├── output/
│   ├── normalized_iocs.csv
│   ├── rejected_iocs.csv
│   ├── stats.json
│   ├── misp_event.json
│   ├── RUN_OUTPUT.txt
│   └── TEST_OUTPUT.txt
├── scripts/
│   ├── process_iocs.py
│   ├── import_to_misp.py
│   └── run_all.sh
├── misp/
│   └── README.md
├── sigma/
│   └── suspicious_powershell_encoded_command.yml
├── report/
│   └── WEEK3_REPORT.md
├── tests/
│   └── test_process_iocs.py
└── evidence/
    └── README.md
```

## 1. Process the IOC data

Run from the Week 3 folder:

```bash
python3 scripts/process_iocs.py
```

The pipeline:

1. reads raw IOC records from CSV;
2. normalizes IOC type names;
3. validates IP addresses, domains, URLs, and hashes;
4. canonicalizes domains, URLs, and hashes;
5. filters low-confidence indicators;
6. correlates duplicate indicators from multiple sources;
7. merges source and tag metadata;
8. exports normalized IOC data;
9. generates a MISP-compatible event JSON;
10. writes processing statistics.

The included dataset is a safe lab dataset that imitates data collected from Shodan,
VirusTotal, Maltego, and manual OSINT. Replace it with your Week 2 export later if needed,
keeping the same CSV columns.

### Input columns

```text
indicator,type,source,confidence,description,tags
```

Accepted type aliases include:

```text
ip, ipv4, ip-src, ip-dst, domain, hostname, url, md5, sha1, sha256
```

## 2. Inspect the output

```bash
cat output/normalized_iocs.csv
cat output/rejected_iocs.csv
cat output/stats.json
```

Run automated checks:

```bash
python3 -m unittest discover -s tests -v
```

Or run everything:

```bash
bash scripts/run_all.sh
```

## 3. Deploy MISP

Use the official `MISP/misp-docker` project:

```bash
git clone https://github.com/MISP/misp-docker.git
cd misp-docker
cp template.env .env
docker compose pull
docker compose up -d
docker compose ps
```

Default lab login documented by the official project:

```text
URL:      http://localhost
User:     admin@admin.test
Password: admin
```

For a real deployment, change the default credentials.

Detailed steps are in `misp/README.md`.

## 4. Import the processed IOCs into MISP

### Option A — Web interface

Import:

```text
output/misp_event.json
```

### Option B — REST API

Create an API key in MISP and set:

```bash
export MISP_URL="http://localhost"
export MISP_API_KEY="PASTE_YOUR_KEY_HERE"
export MISP_VERIFYCERT="false"
```

Then:

```bash
python3 scripts/import_to_misp.py
```

## 5. Sigma rule

The project includes:

```text
sigma/suspicious_powershell_encoded_command.yml
```

It maps suspicious encoded PowerShell execution to MITRE ATT&CK:

- Tactic: Execution
- Technique: T1059.001 — PowerShell

## 6. Evidence for submission

Add screenshots of:

1. `python3 scripts/process_iocs.py`;
2. `output/normalized_iocs.csv`;
3. `output/rejected_iocs.csv`;
4. `docker compose ps`;
5. the imported MISP event;
6. the MISP Attributes page.

Use `report/WEEK3_REPORT.md` as the written report.
