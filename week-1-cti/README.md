# Week 1 — Cyber Threat Intelligence Fundamentals

## 1. Introduction

This section presents the first stage of the project, focusing on Cyber Threat Intelligence (CTI) fundamentals.

The goal of this week is to understand key CTI concepts, classify major cyber threats and their sources, and identify how threat intelligence can support SIEM-based threat hunting and detection.

The work is connected to the main project:

**MITRE ATT&CK-Based SIEM Threat Hunting and Detection**

---

## 2. Objectives

The objectives of Week 1 are:

- Understand the basic concepts of Cyber Threat Intelligence.
- Create a glossary of important CTI terms.
- Classify major types of cyber threats.
- Identify common sources of cyber threats.
- Understand the relationship between CTI and threat hunting.
- Identify how CTI can support SIEM-based detection.
- Prepare a foundation for MITRE ATT&CK-based analysis.

---

## 3. Cyber Threat Intelligence Glossary

| Term | Definition | Relevance to This Project |
|---|---|---|
| Cyber Threat Intelligence (CTI) | Information and analysis about threats, threat actors, their capabilities, activities, and behavior that can support security decision-making. | Provides context for threat hunting and detection. |
| Threat Actor | An individual, group, or organization that conducts or supports malicious cyber activity. | Helps identify who may be responsible for observed activity. |
| Indicator of Compromise (IOC) | An observable artifact that may indicate malicious or suspicious activity. | IOCs can be used to enrich SIEM investigations and detection. |
| Tactics, Techniques and Procedures (TTPs) | A description of an adversary's goals, methods, and specific ways of carrying out activities. | TTPs are used to understand and map attacker behavior. |
| Threat Hunting | A proactive process of searching for evidence of malicious or suspicious activity in an environment. | Threat hunting is the main analytical activity of this project. |
| SIEM | A platform that collects, stores, correlates, and analyzes security-related events and logs. | Provides the main environment for security monitoring and detection. |
| MITRE ATT&CK | A knowledge base that categorizes adversary behavior using tactics, techniques, sub-techniques, and procedures. | Provides the main framework for mapping detected behavior. |
| Threat Intelligence Source | A source that provides information about cyber threats, threat actors, indicators, vulnerabilities, or adversary behavior. | Provides information that can be used for investigation and detection. |
| Adversary | A person, group, or organization conducting hostile activity against a target. | Represents the source of malicious activity investigated by defenders. |
| Threat Hunting Hypothesis | A testable assumption about potentially malicious activity that can be investigated using available data. | Helps structure systematic SIEM investigations. |
| Detection Rule | Logic used to identify potentially suspicious or malicious activity in collected data. | Used to convert threat knowledge into SIEM detections. |
| Context | Additional information that helps explain the meaning and significance of an indicator or event. | Helps distinguish potentially malicious events from normal activity. |

---

## 4. Classification of Cyber Threats

Cyber threats can be classified according to the type of activity, the objective of the attacker, and the techniques used.

### 4.1 Phishing and Social Engineering

Phishing involves deceptive communication intended to manipulate users into performing an action such as opening a malicious link, providing credentials, or executing a file.

**Examples of relevant indicators:**

- Suspicious URLs
- Malicious domains
- Credential harvesting pages
- Suspicious email attachments

**SIEM relevance:**

Authentication logs, endpoint events, DNS logs, proxy logs, and email security events may provide useful evidence for investigation.

---

### 4.2 Ransomware

Ransomware is a form of malicious activity in which attackers seek to disrupt access to systems or data and commonly demand payment from victims.

**Potential indicators:**

- Unusual file modifications
- Suspicious process execution
- Abnormal authentication activity
- Large-scale file access
- Suspicious network connections

**SIEM relevance:**

Endpoint and authentication logs can help identify suspicious behavior before or during an incident.

---

### 4.3 Vulnerability Exploitation

Attackers may exploit weaknesses in software, services, or systems to obtain unauthorized access or execute malicious actions.

**Potential indicators:**

- Exploit-related web requests
- Unexpected process execution
- Abnormal network connections
- Repeated requests against vulnerable services

**SIEM relevance:**

Web server, application, firewall, IDS/IPS, and endpoint logs can provide evidence for investigation.

---

### 4.4 Distributed Denial-of-Service (DDoS)

DDoS attacks attempt to overwhelm a service or network with a large volume of traffic or requests.

**Potential indicators:**

- Large traffic volumes
- Abnormal request rates
- Many source addresses
- Service availability degradation

**SIEM relevance:**

Network traffic and service logs can be analyzed to identify unusual traffic patterns.

---

### 4.5 Credential Attacks

Credential attacks target usernames, passwords, authentication mechanisms, or other credentials.

Examples include:

- Brute-force attempts
- Password spraying
- Credential theft
- Credential reuse

**Potential indicators:**

- Repeated failed logins
- Authentication attempts from unusual locations
- Multiple accounts targeted by the same source
- Abnormal successful login activity

**SIEM relevance:**

Authentication logs are particularly important for detecting credential-related attacks.

---

### 4.6 Malware

Malware is malicious software designed to perform unauthorized or harmful actions.

Examples include:

- Trojans
- Information stealers
- Remote access tools
- Botnet malware

**Potential indicators:**

- Suspicious processes
- Unexpected file creation
- Malicious hashes
- Suspicious network connections

**SIEM relevance:**

Endpoint, process, file, and network telemetry can support malware-related investigations.

---

### 4.7 Cyberespionage

Cyberespionage involves obtaining information or maintaining unauthorized access for intelligence-gathering purposes.

Potential targets include:

- Government organizations
- Research institutions
- Technology companies
- Critical infrastructure

**SIEM relevance:**

Long-term authentication, process, network, and data-access patterns may help identify suspicious activity.

---

### 4.8 Supply Chain and Dependency Attacks

Attackers may compromise software, services, third-party providers, or other dependencies in order to reach downstream targets.

**Potential indicators:**

- Unexpected software changes
- Compromised dependencies
- Suspicious package activity
- Unusual connections to third-party services

**SIEM relevance:**

Software, endpoint, network, and authentication telemetry can help investigate suspicious changes and activity.

---

## 5. Sources of Cyber Threats

Threat sources can be classified by the type of actor or origin responsible for malicious activity.

### 5.1 Cybercriminal Groups

Cybercriminals commonly conduct attacks for financial gain.

Potential activities include:

- Ransomware
- Credential theft
- Fraud
- Malware distribution
- Extortion

---

### 5.2 Hacktivists

Hacktivists use cyber operations to promote political, social, or ideological objectives.

Common activities may include:

- DDoS attacks
- Website disruption
- Data leaks
- Website defacement

---

### 5.3 State-Aligned or State-Sponsored Actors

State-aligned actors may conduct operations connected to national or geopolitical objectives.

Potential activities include:

- Cyberespionage
- Intelligence collection
- Long-term intrusion campaigns
- Targeted attacks against strategic organizations

---

### 5.4 Insider Threats

Insider threats originate from individuals who have legitimate access to an organization's systems or information.

They may involve:

- Malicious insiders
- Accidental actions
- Misuse of privileges
- Unauthorized data access

---

### 5.5 Opportunistic Attackers

Some attackers do not focus on a specific organization initially. Instead, they scan the Internet or other environments for vulnerable systems and services.

Potential activities include:

- Automated scanning
- Exploitation of exposed services
- Credential attacks
- Malware distribution

---

## 6. Threat Classification Matrix

| Threat Type | Typical Source | Example Activity | Useful Data for SIEM |
|---|---|---|---|
| Phishing | Cybercriminals, state-aligned actors | Credential harvesting | Email, DNS, proxy, authentication logs |
| Ransomware | Cybercriminal groups | Data encryption / extortion | Endpoint, file, process, authentication logs |
| Vulnerability Exploitation | Cybercriminals, state-aligned actors | Exploiting vulnerable services | Web, firewall, IDS/IPS, endpoint logs |
| DDoS | Hacktivists, cybercriminals | Service flooding | Network and service logs |
| Credential Attacks | Cybercriminals, opportunistic attackers | Brute force / password spraying | Authentication logs |
| Malware | Cybercriminals, state-aligned actors | Malicious execution | Endpoint and network logs |
| Cyberespionage | State-aligned actors | Information collection | Endpoint, network, authentication logs |
| Supply Chain Attack | Various threat actors | Compromising dependencies | Software, endpoint, network logs |
| Insider Threat | Malicious or compromised insiders | Unauthorized access | Authentication, file and access logs |

---

## 7. CTI and Threat Hunting

Cyber Threat Intelligence and threat hunting are closely connected.

CTI provides information and context about:

- Threat actors
- Indicators
- Adversary behavior
- Tactics
- Techniques
- Procedures
- Known campaigns

Threat hunting uses this information to develop hypotheses and search available security data for suspicious activity.

The relationship can be represented as:

```text
Cyber Threat Intelligence
            |
            v
     Threat Information
            |
            v
   Hunting Hypothesis
            |
            v
     SIEM / Security Logs
            |
            v
       Investigation
            |
            v
     Detection / Alert
            |
            v
   MITRE ATT&CK Mapping
```

## 8. Relevance to the Project

The Week 1 research establishes the foundation for the overall project.

The project will use Cyber Threat Intelligence (CTI) to:

1. Identify relevant threats.
2. Understand possible threat sources.
3. Identify useful indicators and behavioral patterns.
4. Develop threat hunting hypotheses.
5. Search security logs for suspicious activity.
6. Map observed behavior to MITRE ATT&CK.
7. Develop detection rules.

This creates a connection between Cyber Threat Intelligence and the project's SIEM-based detection workflow.

---

## 9. Preliminary MITRE ATT&CK Connection

MITRE ATT&CK provides a structured way to describe adversary behavior.

The framework distinguishes:

- **Tactics** — why an adversary performs an action.
- **Techniques** — how an adversary achieves a tactical goal.
- **Sub-techniques** — more specific descriptions of techniques.
- **Procedures** — specific implementations or observed uses of techniques.

This project will use ATT&CK later to map observed behavior from SIEM investigations to adversary techniques.

---

## 10. Sources

1. ENISA. *ENISA Threat Landscape 2025*.
2. SANS Institute. *Glossary of Cyber Security Terms*.
3. MITRE. *MITRE ATT&CK — Get Started*.
4. MITRE. *MITRE ATT&CK FAQ*.

The selected sources are related to the Week 1 topics specified in the course syllabus.

---

## 11. Week 1 Conclusion

Week 1 established the basic CTI foundation for the project.

The main outcomes are:

- A glossary of key CTI terms.
- A classification of major cyber threats.
- A classification of common threat sources.
- A preliminary connection between CTI, threat hunting, and SIEM.
- An initial connection between threat intelligence and MITRE ATT&CK.

The next stage of the project will focus on **Data Collection Process**, including the identification and mapping of relevant threat intelligence and security data sources.
