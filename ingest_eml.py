import os
import email
from email import policy
import re
from email.utils import parsedate_to_datetime  

def strip_html_tags(html_content):
    """Safely strips HTML formatting to provide clean text for psycholinguistic analysis."""
    # Remove HTML tags using a regular expression
    clean_text = re.sub(r'<.*?>', ' ', html_content)
    # Collapse multiple spaces into a single space
    return re.sub(r'\s+', ' ', clean_text).strip()

def extract_forensic_data(file_path):
    """
    Parses a standard .eml file to extract core forensic data.
    Extracts Sender, Receiver, Timestamp, Subject, and clean Body Text.
    """
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return None
        
    try:
        with open(file_path, 'rb') as f:
            # The default policy handles modern email decoding automatically
            msg = email.message_from_binary_file(f, policy=policy.default)

        
 # --- NEW DATE PARSING LOGIC ---
        raw_date = msg.get('date', 'Unknown Date')
        try:
            # Converts "Thu, 30 Jul..." into "YYYY-MM-DD HH:MM:SS" format for SQL
            sql_ready_date = parsedate_to_datetime(raw_date).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            # Fallback date if the email header is corrupted
            sql_ready_date = '1970-01-01 00:00:00' 

        # 1. Extract Target Metadata (Ignoring routing headers)
        metadata = {
            'timestamp': sql_ready_date,
            'sender': msg.get('from', 'Unknown Sender'),
            'receiver': msg.get('to', 'Unknown Receiver'),
            'subject': msg.get('subject', 'No Subject'),
            'body': ''
        }
        
        # 2. Extract and Clean the Body Payload
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                
                # Skip attachments or complex multipart containers
                if part.get_filename():
                    continue
                    
                # Handle Plain Text
                if content_type == 'text/plain':
                    metadata['body'] += part.get_content() + "\n"
                    
                # Handle HTML Emails (common in corporate and phishing emails)
                elif content_type == 'text/html':
                    raw_html = part.get_content()
                    cleaned_text = strip_html_tags(raw_html)
                    metadata['body'] += cleaned_text + "\n"
        else:
            # Handle single-part emails
            content_type = msg.get_content_type()
            if content_type == 'text/plain':
                metadata['body'] = msg.get_content()
            elif content_type == 'text/html':
                metadata['body'] = strip_html_tags(msg.get_content())
                
        return metadata
        
    except Exception as e:
        print(f"[!] Forensic extraction failed for {file_path}: {e}")
        return None

# --- Example Execution ---
if __name__ == "__main__":
    # Replace with the path to a real evidence file in your lab
    sample_evidence = "phishing_attempt.eml" 
    
    # Create a dummy file for testing if one doesn't exist yet
    if not os.path.exists(sample_evidence):
        with open(sample_evidence, "w") as f:
            f.write("From: attacker@evil.com\n"
                    "To: victim@company.com\n"
                    "Date: Thu, 30 Jul 2026 15:00:00 +0800\n"
                    "Subject: URGENT: Password Reset\n"
                    "Content-Type: text/html\n\n"
                    "<html><body>Please click here <b>immediately</b>.</body></html>")
    
    extracted_evidence = extract_forensic_data(sample_evidence)
    
    if extracted_evidence:
        print("-" * 40)
        print("🔍 FORENSIC EXTRACTION COMPLETE")
        print("-" * 40)
        print(f"Timestamp : {extracted_evidence['timestamp']}")
        print(f"Sender    : {extracted_evidence['sender']}")
        print(f"Receiver  : {extracted_evidence['receiver']}")
        print(f"Subject   : {extracted_evidence['subject']}")
        print("-" * 40)
        print(f"Clean Text: {extracted_evidence['body']}")
        print("-" * 40)