import pyodbc
from ingest_eml import extract_forensic_data
from psych_engine import analyze_and_preserve_evidence
from threat_evaluator import evaluate_threat, update_evidence_in_db

def main():
    print("=" * 50)
    print("🛡️  SENTINEL FORENSICS ENGINE INITIALIZING")
    print("=" * 50)

    # 1. Connect to Database
    # Note: Ensure your ServerName is correct for your local SQL Server instance
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=.\SQLEXPRESS;'
                              'Database=SentinelDB;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        print("[+] Connected to SentinelDB.")
    except Exception as e:
        print(f"[!] Database connection failed: {e}")
        return

    # 2. Ingest Evidence
    evidence_path = "phishing_attempt.eml"
    print(f"\n[*] Phase 1: Ingesting file -> {evidence_path}")
    email_data = extract_forensic_data(evidence_path)

    if not email_data or not email_data['body'].strip():
        print("[!] No readable text found. Exiting.")
        return

    # Log the email into SentinelDB to generate a LogID
    # (Using a dummy SenderID of '1' for testing purposes)
    try:
        insert_log_query = """
            INSERT INTO CommunicationsLog (SenderID, ReceiverEmail, CommunicationDate, SubjectLine, ExtractedBody)
            OUTPUT INSERTED.LogID
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(insert_log_query, (1, email_data['receiver'], email_data['timestamp'], email_data['subject'], email_data['body']))
        log_id = cursor.fetchone()[0]
        conn.commit()
        print(f"[+] Evidence logged. Assigned LogID: {log_id}")
    except Exception as e:
        print(f"[!] Database insert failed: {e}")
        return

    # 3. Psycholinguistic Analysis
    print("\n[*] Phase 2: Running NLP Psycholinguistic Engine...")
    results = analyze_and_preserve_evidence(email_data['body'])
    
    if not results:
        print("[!] Analysis failed.")
        return

    print(f"    Threat Scores Calculated: {results['normalized_scores']}")

    # 4. Threat Evaluation & Evidence Preservation
    print("\n[*] Phase 3: Evaluating Threat Baselines...")
    # Setting is_internal=False to simulate an external phishing attempt
    is_anomaly, reasons = evaluate_threat(cursor, log_id, sender_id=1, is_internal=False, current_scores=results["normalized_scores"])

    if is_anomaly:
        print("\n🚨 ANOMALY DETECTED 🚨")
        for reason in reasons:
            print(f"  -> {reason}")
        
        print("\n[*] Preserving Contextual Evidence...")
        update_evidence_in_db(cursor, log_id, results["extracted_evidence"])
    else:
        print("\n[+] No significant threats detected.")

    # Cleanup
    cursor.close()
    conn.close()
    print("-" * 50)
    print("✅ ANALYSIS COMPLETE")
    print("-" * 50)

if __name__ == "__main__":
    main()