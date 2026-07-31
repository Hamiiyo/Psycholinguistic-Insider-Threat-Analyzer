# Psycholinguistic-Insider-Threat-Analyzer

## Overview 

The goals of the architecture is to: 

•	Psycholinguistic Analysis: Instead of looking for malicious code or suspicious IP addresses, it analyzes the language used in communications. Your NLP engine scores text for things like artificial urgency or unusual certainty, which are hallmark indicators of phishing.

•	Baseline Deviation: For internal threats, it doesn't just look for a single bad action. It builds a historical profile of how a subject normally communicates. If their communication style suddenly spikes or deviates from that baseline, the tool flags it as an anomaly—which is crucial for catching compromised accounts or disgruntled employees attempting to exfiltrate assets.

•	Automated Evidence Preservation: When it detects a threat, it doesn't just flash a notification and move on. It extracts the exact sentences that triggered the anomaly and securely serializes them into SentinelDB.

Here is a complete, well-structured `README.md` file tailored specifically to your project's architecture, including the dependencies, database setup, and pipeline phases we just finalized. You can copy and paste this directly into your repository.

---

## Architecture & Workflow

The engine operates in distinct phases to ensure data integrity and accurate threat scoring:

* **Phase 1: Ingestion (`ingest_eml.py`)**
Parses `.eml` files, extracts routing metadata, safely strips HTML tags for clean text extraction, and standardizes RFC 2822 timestamps into SQL-compliant `DATETIME` formats.
* **Phase 2: Psycholinguistic Analysis (`psych_engine.py`)**
Utilizes the Natural Language Toolkit (NLTK) to tokenize sentences and words. It compares the extracted email body against custom threat lexicons (e.g., time pressure, certainty) to generate normalized threat scores.
* **Phase 3: Threat Evaluation (`threat_evaluator.py`)**
Compares the generated psycholinguistic scores against baseline thresholds to determine if the communication constitutes a phishing anomaly or insider threat.
* **Phase 4: Archival Storage (`main.py` & `database.py`)**
Logs the extracted evidence and threat scores securely into `SentinelDB` using `pyodbc` for persistent forensic tracking.

---

## Prerequisites

Ensure you have the following installed before running the engine:

* **Python 3.11+**
* **SQL Server Express** (`.\SQLEXPRESS`)
* **SQL Server Management Studio (SSMS)**
* **ODBC Driver for SQL Server**

---

## Installation & Setup

### 1. Python Dependencies

Install the required external Python libraries using `pip`:

```powershell
pip install pyodbc nltk

```

### 2. Database Creation

Open SQL Server Management Studio (SSMS) and execute the following query to create the necessary database container and seed an initial dummy subject to satisfy foreign key constraints during testing:

```sql
CREATE DATABASE SentinelDB;
GO

USE SentinelDB;
GO

-- Seed an initial subject to prevent Foreign Key constraint violations on first run
INSERT INTO Subjects (EmailAddress, Department)
VALUES ('attacker@evil.com', 'External Threat');
GO

```

### 3. Build the Schema

Run the database builder script to generate the required relational tables (`Subjects`, `CommunicationsLog`, `PsycholinguisticScores`):

```powershell
python database.py

```

---

## Usage

### 1. Provide Evidence

Place the target `.eml` files into your project directory. If no file is present, the script is configured to automatically generate a dummy `phishing_attempt.eml` file for baseline testing.

### 2. Execute the Engine

Run the main orchestrator script to process the evidence:

```powershell
python main.py

```

### Expected Output

Upon successful execution, the terminal will display the initialization sequence, confirm database connection, log the assigned Evidence ID, output the calculated psycholinguistic scores, and trigger an alert if the threat thresholds are exceeded.

---

## Troubleshooting

* **Conversion failed when converting date/time:** Ensure `ingest_eml.py` is using `email.utils.parsedate_to_datetime` to convert standard email headers into the `YYYY-MM-DD HH:MM:SS` format required by SQL Server.
* **Foreign Key Constraint Violation:** The `Subjects` table is likely empty. Ensure you have seeded at least one user (e.g., `SenderID = 1`) into the database using SSMS before attempting to log communication evidence.
* **LookupError: resource_not_found (punkt/punkt_tab):** The NLTK library requires specific tokenization datasets. Ensure your script runs `nltk.download('punkt')` and `nltk.download('punkt_tab')` prior to calling the `sent_tokenize` function.

