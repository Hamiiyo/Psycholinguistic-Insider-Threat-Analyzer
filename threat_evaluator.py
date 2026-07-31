import pyodbc
import json

# --- CONFIGURATION THRESHOLDS ---
PHISHING_URGENCY_THRESHOLD = 4.0  
PHISHING_CERTAINTY_THRESHOLD = 3.0 
INSIDER_SPIKE_MULTIPLIER = 1.40  
MINIMUM_BASELINE_EMAILS = 5 

def get_historical_baseline(cursor, sender_id):
    # ... (Keep your existing baseline logic here) ...
    pass

def evaluate_threat(cursor, log_id, sender_id, is_internal, current_scores):
    is_anomaly = False
    reasons = []

    # If it is an external email, check against the hardcoded phishing thresholds
    if not is_internal:
        if current_scores.get('time_pressure', 0) >= PHISHING_URGENCY_THRESHOLD:
            is_anomaly = True
            reasons.append(f"Urgency score ({current_scores.get('time_pressure')}%) exceeded threshold.")
            
        if current_scores.get('certainty', 0) >= PHISHING_CERTAINTY_THRESHOLD:
            is_anomaly = True
            reasons.append(f"Certainty score ({current_scores.get('certainty')}%) exceeded threshold.")
            
    # You MUST return these two values so main.py can unpack them
    return is_anomaly, reasons

# --- NEW DATABASE INSERTION LOGIC ---
def update_evidence_in_db(cursor, log_id, extracted_evidence):
    """
    Formats the extracted evidence sentences and updates the CommunicationsLog table.
    """
    # Combine both phishing and insider threat sentences into a single dictionary
    combined_evidence = {
        "phishing": extracted_evidence.get("phishing", []),
        "insider_threat": extracted_evidence.get("insider_threat", [])
    }
    
    # Check if there is actually any evidence to store
    if not combined_evidence["phishing"] and not combined_evidence["insider_threat"]:
        return
        
    # Convert the evidence dictionary into a clean JSON string for SQL storage
    evidence_json = json.dumps(combined_evidence)
    
    try:
        update_query = """
            UPDATE CommunicationsLog 
            SET ExtractedEvidence = ? 
            WHERE LogID = ?
        """
        cursor.execute(update_query, (evidence_json, log_id))
        cursor.connection.commit()
        print(f"[+] Contextual evidence successfully preserved in SentinelDB for LogID {log_id}.")
        
    except Exception as e:
        print(f"[!] Error updating evidence in database: {e}")
