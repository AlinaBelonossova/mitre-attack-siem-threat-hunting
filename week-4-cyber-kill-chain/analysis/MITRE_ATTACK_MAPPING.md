# Week 4 — MITRE ATT&CK Mapping

## SolarWinds Compromise

The mapping below connects the Cyber Kill Chain stages with documented SolarWinds behaviors. The models are complementary; they are not a one-to-one replacement for each other.

| Cyber Kill Chain Stage | SolarWinds Activity | MITRE ATT&CK Technique | ID |
|---|---|---|---|
| Reconnaissance | Target and environment information gathering | Account Discovery: Domain Account | T1087.002 |
| Weaponization | SUNSPOT inserted SUNBURST into the Orion build process | Supply Chain Compromise: Compromise Software Supply Chain | T1195.002 |
| Delivery | Trojanized Orion update distributed through legitimate software updates | Supply Chain Compromise: Compromise Software Supply Chain | T1195.002 |
| Exploitation | Victim installs and executes the compromised trusted update | No separate exploit technique is asserted here | — |
| Installation | SUNBURST operates as a trojanized Orion DLL | Data Manipulation: Stored Data Manipulation | T1565.001 |
| Command & Control | Web-based C2 communication | Application Layer Protocol: Web Protocols | T1071.001 |
| Command & Control | DNS-based C2 and dynamic resolution | Application Layer Protocol: DNS / Dynamic Resolution | T1071.004 / T1568 |
| Command & Control | Encoded C2 information | Data Encoding: Standard Encoding | T1132.001 |
| Actions on Objectives | Collection of information from local systems | Data from Local System | T1005 |
| Actions on Objectives | Domain account discovery | Account Discovery: Domain Account | T1087.002 |
| Actions on Objectives | PowerShell activity documented in campaign activity | Command and Scripting Interpreter: PowerShell | T1059.001 |

## Mapping Notes

- The Cyber Kill Chain is a seven-stage high-level model.
- MITRE ATT&CK is a detailed knowledge base of adversary tactics and techniques.
- A single ATT&CK technique can be relevant to more than one Kill Chain stage.
- Not every Kill Chain stage has to correspond to a unique ATT&CK technique.
- The Exploitation stage is intentionally not assigned an invented technique.
