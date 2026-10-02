# Week 4 Report — Cyber Kill Chain Analysis

## 1. Objective

The objective of Week 4 is to analyze a real-world cyberattack using the seven-stage Cyber Kill Chain model and connect the observed attacker behaviors to relevant MITRE ATT&CK techniques.

## 2. Selected Incident

The selected case is the **SolarWinds Compromise (C0024)**.

The campaign involved a compromise of the SolarWinds Orion software build environment. Malicious code was inserted into Orion software and distributed through legitimate software updates. Selected victims were then targeted for additional post-compromise activity.

## 3. Cyber Kill Chain Analysis

### 3.1 Reconnaissance

The adversary identified suitable organizations and environments for follow-on activity. Public reporting and MITRE ATT&CK describe subsequent discovery and targeting activity during the campaign.

**Analysis:** Reconnaissance represents the information-gathering stage before or around the initial compromise.

### 3.2 Weaponization

The attackers prepared malicious components that could operate within the SolarWinds Orion software environment. SUNSPOT was used to insert SUNBURST into the Orion build process.

**Analysis:** The important characteristic is the preparation of malicious capability for delivery through a trusted software channel.

### 3.3 Delivery

The malicious SUNBURST code was incorporated into legitimate SolarWinds Orion software updates. Victims received the trojanized software through the normal update mechanism.

**MITRE ATT&CK:** T1195.002 — Supply Chain Compromise: Compromise Software Supply Chain.

### 3.4 Exploitation

The compromised update was installed and executed by affected organizations. The case does not require inventing a separate software vulnerability exploitation step; the trusted update mechanism itself was abused.

**Analysis:** In this case, the Cyber Kill Chain stage is best understood as the point where the delivered malicious component became active on the victim environment.

### 3.5 Installation

SUNBURST operated as a trojanized SolarWinds Orion DLL. After execution, the malware established the conditions needed for later communication and follow-on activity.

Related ATT&CK evidence includes execution and persistence-related behaviors documented for the campaign and its associated software.

### 3.6 Command and Control

SUNBURST communicated with attacker-controlled infrastructure using application-layer protocols. MITRE documents HTTP/HTTPS-style web communication and DNS-based command and control behavior.

Relevant techniques include:

- T1071.001 — Application Layer Protocol: Web Protocols
- T1071.004 — Application Layer Protocol: DNS
- T1132.001 — Data Encoding: Standard Encoding
- T1568 — Dynamic Resolution

### 3.7 Actions on Objectives

After initial compromise, the attackers selectively targeted victims and performed additional discovery, credential-related, lateral, and data-access activities.

Examples documented by MITRE and Microsoft include account discovery, access to local data, remote execution, and deployment of additional tooling.

Relevant techniques include:

- T1005 — Data from Local System
- T1087.002 — Account Discovery: Domain Account
- T1059.001 — Command and Scripting Interpreter: PowerShell

## 4. SIEM and Threat Hunting Relevance

The Cyber Kill Chain provides a high-level sequence, while MITRE ATT&CK provides more granular descriptions of adversary behavior.

For a SIEM-based threat hunting workflow, each stage can be translated into:

1. A threat hypothesis
2. Required telemetry
3. Observable indicators
4. Search or detection logic
5. MITRE ATT&CK mapping
6. Investigation and response actions

Example hunting questions include:

- Did a SolarWinds-related process make unusual external connections?
- Did a host communicate with unusual DNS infrastructure?
- Were PowerShell or other scripting interpreters executed unexpectedly?
- Were new or unusual domain accounts queried?
- Did remote execution or lateral movement occur after the suspected initial compromise?

## 5. Conclusion

The SolarWinds Compromise demonstrates how a trusted software supply chain can be abused to move from initial delivery to command and control and post-compromise activity.

The Cyber Kill Chain helps organize the incident into a sequence of attacker objectives. MITRE ATT&CK complements this model by describing specific adversary techniques that can be translated into SIEM hunting hypotheses and detection opportunities.
