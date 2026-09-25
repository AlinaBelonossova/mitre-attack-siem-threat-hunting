# MISP deployment and IOC import

## 1. Verify Docker

```bash
docker -v
docker compose version
```

The official MISP Docker project documents Docker Engine 25+ and Docker Compose 2.17+ as prerequisites.

## 2. Start MISP

```bash
git clone https://github.com/MISP/misp-docker.git
cd misp-docker

cp template.env .env
docker compose pull
docker compose up -d
docker compose ps
```

Open:

```text
http://localhost
```

Default lab credentials documented by the official project:

```text
admin@admin.test
admin
```

For a non-lab environment, change the default credentials and review `.env`.

## 3. Import the generated IOC event

First generate the Week 3 outputs:

```bash
python3 scripts/process_iocs.py
```

Then import:

```text
output/misp_event.json
```

through the MISP web interface.

## 4. REST API import

Create an authentication key in MISP and set:

```bash
export MISP_URL="http://localhost"
export MISP_API_KEY="PASTE_YOUR_KEY_HERE"
export MISP_VERIFYCERT="false"
```

Run:

```bash
python3 scripts/import_to_misp.py
```

## 5. Evidence

Take screenshots of:

- `docker compose ps`;
- the imported event page;
- event ID/UUID;
- the MISP Attributes table;
- at least one network IOC;
- at least one hash IOC.
