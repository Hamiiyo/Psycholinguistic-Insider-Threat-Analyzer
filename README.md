# Psycholinguistic-Insider-Threat-Analyzer
The goals of the architecture is to: 

•	Psycholinguistic Analysis: Instead of looking for malicious code or suspicious IP addresses, it analyzes the language used in communications. Your NLP engine scores text for things like artificial urgency or unusual certainty, which are hallmark indicators of phishing.
•	Baseline Deviation: For internal threats, it doesn't just look for a single bad action. It builds a historical profile of how a subject normally communicates. If their communication style suddenly spikes or deviates from that baseline, the tool flags it as an anomaly—which is crucial for catching compromised accounts or disgruntled employees attempting to exfiltrate assets.
•	Automated Evidence Preservation: When it detects a threat, it doesn't just flash a notification and move on. It extracts the exact sentences that triggered the anomaly and securely serializes them into SentinelDB.

