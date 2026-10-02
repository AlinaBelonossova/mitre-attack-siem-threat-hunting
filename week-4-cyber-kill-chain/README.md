# Week 4 — Cyber Kill Chain Analysis

## MITRE ATT&CK-Based SIEM Threat Hunting and Detection

---

## 1. Introduction

The Cyber Kill Chain is a framework developed by Lockheed Martin to describe the stages that an adversary must progress through to achieve a cyberattack objective.

The original Cyber Kill Chain consists of seven stages:

1. Reconnaissance
2. Weaponization
3. Delivery
4. Exploitation
5. Installation
6. Command and Control
7. Actions on Objectives

For this week's practical analysis, the **SolarWinds Compromise** was selected as a real-world cyberattack case.

The SolarWinds incident demonstrates how an adversary can compromise a software build environment, distribute malicious code through a legitimate software update, establish command and control, and perform post-compromise activities.

This analysis connects the Cyber Kill Chain with the **MITRE ATT&CK framework** and the project's broader objective of **SIEM-based threat hunting and detection**.

---

## 2. Objectives

- Understand the seven stages of the Cyber Kill Chain.
- Analyze a real-world cyberattack using the Cyber Kill Chain model.
- Study the SolarWinds Compromise as a real-world supply chain attack.
- Identify important adversary behaviors.
- Map relevant behaviors to MITRE ATT&CK techniques.
- Identify opportunities for detection and threat hunting.
- Connect Cyber Kill Chain analysis with SIEM monitoring.
- Connect attack stages with technical telemetry and detection logic.

---

## 3. Cyber Kill Chain Model

The Cyber Kill Chain developed by Lockheed Martin contains seven stages.

```text
Reconnaissance
       ↓
Weaponization
       ↓
Delivery
       ↓
Exploitation
       ↓
Installation
       ↓
Command & Control
       ↓
Actions on Objectives
```

### 3.1 Reconnaissance

The adversary gathers information about the target environment, organizations, users, infrastructure, and potential attack opportunities.

### 3.2 Weaponization

The adversary prepares malicious tools, code, files, or other capabilities.

### 3.3 Delivery

The malicious capability is delivered to the target environment.

Examples include malicious email attachments, malicious links, compromised websites, removable media, and compromised software updates.

### 3.4 Exploitation

The adversary triggers or exploits a condition that allows malicious activity to execute or gain access.

Not every real-world intrusion contains a separate vulnerability exploitation step.

### 3.5 Installation

Malicious software or another mechanism is installed or established on the victim system.

### 3.6 Command and Control

The compromised system communicates with attacker-controlled infrastructure.

Examples include HTTP/HTTPS, DNS, other application-layer protocols, and dynamic resolution mechanisms.

### 3.7 Actions on Objectives

The adversary performs activities related to the ultimate objectives of the operation, such as credential access, account discovery, data collection, lateral movement, cloud access, persistence, or exfiltration.

---

# 4. Case Study — SolarWinds Compromise

## 4.1 Overview

The SolarWinds Compromise is a major software supply chain compromise involving the SolarWinds Orion IT management software.

MITRE ATT&CK identifies the campaign as:

- **Campaign:** SolarWinds Compromise
- **Campaign ID:** C0024
- **Associated group:** APT29
- **Important malware:** SUNBURST and SUNSPOT

The attackers compromised the SolarWinds Orion software build process and inserted malicious code into legitimate software builds. The compromised software was subsequently distributed through normal software update mechanisms.

---

## 4.2 Main Malware Components

### SUNSPOT

SUNSPOT is an implant associated with the SolarWinds build process. Its purpose was to inject the SUNBURST backdoor into SolarWinds Orion software builds.

The most important technique for this analysis is:

**T1195.002 — Supply Chain Compromise: Compromise Software Supply Chain**

### SUNBURST

SUNBURST is a trojanized DLL designed to operate within the SolarWinds Orion software update framework.

Relevant MITRE ATT&CK techniques include:

- T1071.001 — Application Layer Protocol: Web Protocols
- T1071.004 — Application Layer Protocol: DNS
- T1132.001 — Data Encoding: Standard Encoding
- T1005 — Data from Local System
- T1568 — Dynamic Resolution
- T1546.012 — Event Triggered Execution: Image File Execution Options Injection
- T1218.011 — System Binary Proxy Execution: Rundll32
- T1083 — File and Directory Discovery
- T1057 — Process Discovery
- T1082 — System Information Discovery
- T1016 — System Network Configuration Discovery
- T1033 — System Owner/User Discovery

---

# 5. SolarWinds Attack Flow

The overall attack can be represented as follows:

```text
Attacker / APT29
        ↓
Compromise SolarWinds build environment
        ↓
SUNSPOT modifies Orion build process
        ↓
SUNBURST inserted into legitimate software
        ↓
Trojanized Orion software update
        ↓
Victim installs legitimate-looking update
        ↓
SUNBURST executes
        ↓
C2 communication
        ↓
Victim/environment discovery
        ↓
Additional tools and credentials
        ↓
Lateral movement and cloud access
        ↓
Data access and other objectives
```

The SolarWinds operation was more complex than a simple linear attack. Therefore, the Cyber Kill Chain is used as a **high-level analytical model**, while MITRE ATT&CK is used to describe more specific technical behaviors.

---

# 6. Cyber Kill Chain Analysis of the SolarWinds Compromise

## 6.1 Stage 1 — Reconnaissance

During reconnaissance, an adversary gathers information needed to identify targets, infrastructure, accounts, and potential opportunities.

The SolarWinds operation involved extensive targeting and post-compromise discovery activities.

Examples include:

- Account Discovery
- File and Directory Discovery
- Process Discovery
- System Information Discovery
- System Network Configuration Discovery

One documented example is:

**T1087.002 — Account Discovery: Domain Account**

The Reconnaissance stage should not be interpreted as a direct one-to-one equivalent of a single MITRE ATT&CK technique. The Cyber Kill Chain describes the overall phase, while ATT&CK provides more specific behaviors.

---

## 6.2 Stage 2 — Weaponization

Weaponization represents the preparation of malicious capabilities.

Important components included:

- SUNSPOT
- SUNBURST
- Other malware and post-compromise tools

SUNSPOT was specifically designed to manipulate the SolarWinds Orion build process and inject SUNBURST into software builds.

### Important ATT&CK Association

**T1195.002 — Supply Chain Compromise: Compromise Software Supply Chain**

The malicious capability was introduced into legitimate software before it reached final victims.

---

## 6.3 Stage 3 — Delivery

Delivery was one of the most distinctive parts of the SolarWinds attack.

The attackers compromised the software supply chain instead of simply sending a malicious executable to every victim.

```text
SolarWinds Build Environment
          ↓
SUNSPOT
          ↓
SUNBURST inserted
          ↓
Legitimate Orion software build
          ↓
Software update
          ↓
Victim organization
```

### MITRE ATT&CK Mapping

**T1195.002 — Supply Chain Compromise: Compromise Software Supply Chain**

The malicious component was delivered through software that the victim expected to trust.

---

## 6.4 Stage 4 — Exploitation

The Exploitation stage normally represents exploitation of a vulnerability or another mechanism that allows malicious activity to execute.

The SolarWinds case does not map cleanly to a traditional vulnerability-exploitation technique at this stage.

Instead, the operation relied heavily on the compromise of the software supply chain and the trusted software update mechanism.

```text
Traditional attack:

Vulnerability
      ↓
Exploit
      ↓
Execution


SolarWinds:

Compromised software build
      ↓
Trojanized update
      ↓
Victim trusts update
      ↓
Malicious code executes
```

This demonstrates an important limitation of applying a rigid seven-stage model to complex real-world attacks. Not every campaign contains a clearly separable exploitation step.

---

## 6.5 Stage 5 — Installation

After the compromised software was installed and executed, SUNBURST provided a foothold for additional activity.

### T1218.011 — System Binary Proxy Execution: Rundll32

SUNBURST used Rundll32 to execute payloads.

### T1546.012 — Event Triggered Execution: Image File Execution Options Injection

SUNBURST created an Image File Execution Options (IFEO) Debugger registry value for `dllhost.exe` to trigger the installation of Cobalt Strike.

These techniques demonstrate how malicious code could execute and enable additional post-compromise activity.

---

## 6.6 Stage 6 — Command and Control

Command and Control was a major component of the SolarWinds operation.

### T1071.001 — Application Layer Protocol: Web Protocols

SUNBURST communicated using HTTP GET and HTTP POST requests.

### T1071.004 — Application Layer Protocol: DNS

SUNBURST also used DNS for command and control.

### T1568 — Dynamic Resolution

SUNBURST dynamically resolved command-and-control infrastructure using randomly generated subdomains.

### T1132.001 — Data Encoding: Standard Encoding

SUNBURST used Base64 encoding in its C2 traffic.

```text
Compromised Host
      ↓
SUNBURST
      ↓
DNS / HTTP communication
      ↓
Dynamic resolution
      ↓
Attacker infrastructure
      ↓
Commands / responses
```

### Threat Hunting Opportunities

A SIEM can investigate:

- Unusual DNS requests
- Rare domains
- Random-looking subdomains
- Repeated external connections
- Suspicious HTTP traffic
- Unusual process-to-network relationships
- Unexpected communication from SolarWinds-related processes
- Abnormal DNS frequency
- Connections to previously unseen infrastructure

---

## 6.7 Stage 7 — Actions on Objectives

The final stage represents the adversary's mission-related activities.

Examples include:

- Account discovery
- Credential access
- Email collection
- Lateral movement
- Cloud access
- SAML token abuse
- Data collection

### T1005 — Data from Local System

SUNBURST collected information from compromised hosts.

### T1087.002 — Account Discovery: Domain Account

APT29 obtained information about accounts and roles in victim environments.

### T1606.002 — Forge Web Credentials: SAML Tokens

During the SolarWinds Compromise, APT29 created tokens using compromised SAML signing certificates.

### T1550 — Use Alternate Authentication Material

APT29 used forged SAML tokens to impersonate users and access enterprise cloud applications and services.

### T1114.002 — Email Collection: Remote Email Collection

MITRE documents collection of emails from selected individuals during the SolarWinds Compromise.

### T1021.002 — SMB/Windows Admin Shares

APT29 used administrative accounts to connect over SMB to targeted users.

These activities demonstrate that the SolarWinds compromise was not limited to the initial malware infection.

---

# 7. Cyber Kill Chain and MITRE ATT&CK Mapping

This table provides an analytical mapping between the high-level Cyber Kill Chain stages and selected MITRE ATT&CK techniques.

This is **not a one-to-one official mapping**. MITRE ATT&CK and the Cyber Kill Chain serve different purposes.

| Cyber Kill Chain Stage | SolarWinds Activity | MITRE ATT&CK |
|---|---|---|
| Reconnaissance | Target and environment information gathering | Related Discovery techniques |
| Weaponization | SUNSPOT and SUNBURST preparation | Related malware / supply-chain behaviors |
| Delivery | Trojanized SolarWinds Orion update | **T1195.002** |
| Exploitation | Abuse of trusted software update mechanism | No clean one-to-one exploit mapping |
| Installation | SUNBURST execution and additional payload execution | **T1218.011**, **T1546.012** |
| Command & Control | HTTP/HTTPS communication | **T1071.001** |
| Command & Control | DNS-based communication | **T1071.004** |
| Command & Control | Dynamic C2 infrastructure resolution | **T1568** |
| Command & Control | Base64 encoding | **T1132.001** |
| Actions on Objectives | Local data collection | **T1005** |
| Actions on Objectives | Domain account discovery | **T1087.002** |
| Actions on Objectives | SAML token abuse | **T1606.002**, **T1550** |
| Actions on Objectives | Email collection | **T1114.002** |
| Actions on Objectives | SMB-based activity | **T1021.002** |

---

# 8. Attack Timeline

A simplified timeline is shown below.

```text
2019
 │
 ├── Initial activity associated with the SolarWinds operation
 │
2020
 │
 ├── SUNSPOT used in the SolarWinds build environment
 │
 ├── SUNBURST inserted into Orion software builds
 │
 ├── Trojanized updates distributed
 │
 ├── Selected victim environments compromised
 │
 └── Post-compromise activity begins
 │
December 2020
 │
 ├── SUNBURST / Solorigate publicly identified
 │
 └── Investigation and response begin
 │
2021
 │
 ├── Additional technical details disclosed
 │
 ├── Broader campaign activity analyzed
 │
 └── Government and industry reporting published
```

The exact campaign timeline is more complex than this simplified representation.

---

# 9. SIEM and Threat Hunting Connection

The SolarWinds case provides a useful example of how Cyber Kill Chain analysis can be connected to SIEM-based threat hunting.

The overall process can be represented as:

```text
Cyber Kill Chain
       ↓
Attack Stage
       ↓
MITRE ATT&CK Technique
       ↓
Observable Behavior
       ↓
Logs / Telemetry
       ↓
SIEM
       ↓
Threat Hunting
       ↓
Detection
       ↓
Investigation
```

## 9.1 Data Sources

### Network telemetry

- DNS logs
- Firewall logs
- Proxy logs
- HTTP/HTTPS logs
- Network flow data

### Endpoint telemetry

- Windows Event Logs
- Process creation logs
- PowerShell logs
- Registry modification logs
- File creation/deletion logs
- Endpoint Detection and Response telemetry

### Identity and authentication telemetry

- Active Directory logs
- Authentication events
- Account activity
- Privilege changes
- Cloud authentication logs
- SAML-related events

---

# 10. Threat Hunting Hypothesis

A threat hunting hypothesis based on the SolarWinds case can be defined as:

> **A compromised endpoint may communicate with attacker-controlled infrastructure through DNS or HTTP while attempting to make the traffic appear legitimate.**

The hunting workflow is:

```text
Threat Hypothesis
       ↓
Collect DNS / HTTP / Endpoint Logs
       ↓
Normalize Events
       ↓
Search for Suspicious Communication
       ↓
Correlate Network + Endpoint Activity
       ↓
Map Findings to MITRE ATT&CK
       ↓
Investigate Host and User
       ↓
Create Detection Logic
```

---

# 11. Example SIEM Hunting Questions

## Network Hunting

- Which hosts communicate with rare external domains?
- Are there randomly generated or unusual DNS subdomains?
- Which hosts generate repeated DNS queries to the same unusual domain?
- Are SolarWinds-related processes communicating with unexpected external destinations?
- Are there unusual HTTP GET or POST requests?

## Endpoint Hunting

- Which processes initiate unexpected network connections?
- Are there unusual `rundll32.exe` executions?
- Are IFEO registry values being modified?
- Are unexpected DLLs loaded by trusted processes?
- Are suspicious files created in Windows directories?

## Identity Hunting

- Are privileged accounts being used from unusual systems?
- Are there unusual authentication patterns?
- Are new or unexpected privileges assigned?
- Are suspicious SAML tokens or authentication events observed?
- Are accounts accessing systems or services they normally do not use?

---

# 12. Detection Opportunities by Kill Chain Stage

| Kill Chain Stage | Potential Detection | Example Data Source |
|---|---|---|
| Reconnaissance | Unusual discovery activity | Endpoint / AD logs |
| Weaponization | Suspicious software/build modifications | Build logs / EDR |
| Delivery | Unexpected software update or binary change | Software inventory / EDR |
| Exploitation | Suspicious execution after update | Process logs / EDR |
| Installation | Rundll32 or IFEO activity | Windows Event Logs / EDR |
| Command & Control | Suspicious DNS/HTTP communication | DNS / Proxy / Firewall |
| Actions on Objectives | Account, credential, email, or data access anomalies | AD / Cloud / SIEM |

---

# 13. Defensive Opportunities

### Reconnaissance

- Monitor unusual external reconnaissance
- Reduce unnecessary exposure
- Monitor public-facing infrastructure

### Weaponization

- Protect software development environments
- Monitor source-code and build-process modifications
- Restrict access to build servers

### Delivery

- Verify software integrity
- Monitor software updates
- Validate digital signatures
- Maintain software inventories

### Exploitation

- Monitor unusual execution after software updates
- Apply security controls to endpoint execution

### Installation

- Monitor suspicious DLL execution
- Monitor Rundll32 activity
- Monitor IFEO registry modifications

### Command & Control

- Monitor DNS anomalies
- Monitor unusual outbound HTTP connections
- Use network detection controls
- Correlate endpoint and network telemetry

### Actions on Objectives

- Monitor privileged account activity
- Detect abnormal authentication
- Monitor cloud access
- Protect identity infrastructure
- Monitor sensitive data access

---

# 14. Relationship to the Project

This Week 4 analysis extends the previous project work.

```text
Week 1
Cyber Threat Intelligence Fundamentals
        ↓
Week 2
Data Collection
        ↓
Week 3
Data Processing and Exploitation
        ↓
Week 4
Cyber Kill Chain
        ↓
MITRE ATT&CK Mapping
        ↓
SIEM Threat Hunting
        ↓
Detection
```

Week 2 focused on collecting information from external intelligence sources.

Week 3 focused on processing, normalizing, validating, correlating, and enriching IOC data.

Week 4 adds an attack lifecycle perspective.

The Cyber Kill Chain helps answer:

> **Where is the adversary in the attack process?**

MITRE ATT&CK helps answer:

> **What specific technique or behavior is being used?**

SIEM and threat hunting help answer:

> **What telemetry can we use to detect or investigate the behavior?**

---

# 15. Key Findings

### Finding 1 — Supply chain compromise can bypass traditional trust assumptions

The malicious code was introduced into legitimate software before reaching victims.

### Finding 2 — Cyberattacks are multi-stage operations

The initial compromise was only one part of the overall operation.

### Finding 3 — Command and Control can be designed to blend into normal traffic

SUNBURST used DNS and HTTP-based communication and attempted to resemble legitimate SolarWinds-related activity.

### Finding 4 — Attackers can use legitimate tools and credentials

Post-compromise operations can involve legitimate accounts, administrative mechanisms, and remote-access technologies.

### Finding 5 — Multiple telemetry sources are required

Detecting complex attacks requires correlation between:

- Network telemetry
- Endpoint telemetry
- Identity logs
- Cloud logs
- SIEM events

### Finding 6 — Cyber Kill Chain and MITRE ATT&CK complement each other

The Cyber Kill Chain provides a high-level attack progression model.

MITRE ATT&CK provides detailed adversary techniques and procedures.

Using both models allows defenders to understand an attack at different levels of abstraction.

---

# 16. Conclusion

The SolarWinds Compromise provides a real-world example for analyzing the Cyber Kill Chain.

The attack involved a compromised software development and build process, malicious code insertion, distribution through legitimate software updates, command-and-control communication, discovery, credential and identity abuse, lateral movement, and other post-compromise activities.

The analysis also demonstrates why Cyber Kill Chain and MITRE ATT&CK should not be treated as identical frameworks.

The Cyber Kill Chain provides a high-level representation of attack progression, while MITRE ATT&CK provides detailed techniques that describe specific adversary behaviors.

For a SIEM-based threat hunting project, these frameworks can be combined with security telemetry to create hypotheses, investigate suspicious activity, map findings to ATT&CK techniques, and develop detection logic.

The overall analytical model for this project is:

```text
Cyber Kill Chain
       ↓
MITRE ATT&CK
       ↓
Observable Behavior
       ↓
Security Telemetry
       ↓
SIEM
       ↓
Threat Hunting
       ↓
Detection and Response
```

---

# 17. References

1. Lockheed Martin. *The Lockheed Martin Cyber Kill Chain.*
2. Lockheed Martin. *Seven Ways to Apply the Cyber Kill Chain with a Threat Intelligence Platform.*
3. MITRE ATT&CK. *SolarWinds Compromise — Campaign C0024.*
4. MITRE ATT&CK. *SUNBURST — Software S0559.*
5. MITRE ATT&CK. *SUNSPOT — Software S0562.*
6. MITRE ATT&CK. *Supply Chain Compromise: Compromise Software Supply Chain — T1195.002.*
7. MITRE ATT&CK. *Application Layer Protocol: Web Protocols — T1071.001.*
8. MITRE ATT&CK. *Application Layer Protocol: DNS — T1071.004.*
9. MITRE ATT&CK. *Dynamic Resolution — T1568.*
10. MITRE ATT&CK. *System Binary Proxy Execution: Rundll32 — T1218.011.*
11. MITRE ATT&CK. *Event Triggered Execution: Image File Execution Options Injection — T1546.012.*
12. MITRE ATT&CK. *Data from Local System — T1005.*
13. MITRE ATT&CK. *Account Discovery: Domain Account — T1087.002.*
14. MITRE ATT&CK. *Forge Web Credentials: SAML Tokens — T1606.002.*
15. MITRE ATT&CK. *Use Alternate Authentication Material — T1550.*
16. Microsoft Threat Intelligence. *Deep dive into the Solorigate second-stage activation: From SUNBURST to TEARDROP and Raindrop.*
17. CISA. *Supply Chain Compromise: Detecting APT Activity from Known TTPs.*

---

# 18. Project Relevance

This Week 4 analysis supports the overall project:

**MITRE ATT&CK-Based SIEM Threat Hunting and Detection**

The analysis demonstrates how a real-world attack can be transformed from:

**Attack Scenario**

→ **Cyber Kill Chain**

→ **MITRE ATT&CK Techniques**

→ **Observable Indicators**

→ **SIEM Telemetry**

→ **Threat Hunting Hypothesis**

→ **Detection Logic**

This methodology will be used in later weeks to develop more detailed threat hunting and detection capabilities.

