import json
import nltk
import string

# Download sentence tokenizer
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
from nltk.tokenize import word_tokenize, sent_tokenize

# 1. Custom Lexicons (Same as before)
LEXICONS = {
    "phishing": {
        "time_pressure": ["immediate", "immediately", "urgent", "asap", "quickly", "now", "deadline", "expire", "24 hours"],
        "certainty": ["guaranteed", "mandatory", "must", "require", "required", "ensure", "absolutely", "definitely"]
    },
    "insider_threat": {
        "self_focused": ["i", "me", "my", "mine", "myself"],
        "negative_affect": ["unfair", "angry", "quit", "hate", "stupid", "worst", "resign", "frustrated", "tired", "ignored"],
        "cognitive_process": ["rethink", "should", "always", "never", "because", "know", "think", "understand"]
    }
}

def analyze_and_preserve_evidence(text):
    """
    Tokenizes text to calculate scores while simultaneously extracting 
    the exact sentences that triggered the psycholinguistic flags.
    """
    if not text or not text.strip():
        return None

    # Break the raw text into a list of full sentences to preserve context
    sentences = sent_tokenize(text)
    
    total_words = 0
    counts = {key: 0 for key in ["time_pressure", "certainty", "self_focused", "negative_affect", "cognitive_process"]}
    
    # Storage for the exact sentences that trigger flags
    evidence = {
        "phishing_sentences": set(),
        "insider_sentences": set()
    }

    # Analyze sentence by sentence
    for sentence in sentences:
        sentence_lower = sentence.lower()
        tokens = word_tokenize(sentence_lower)
        valid_words = [token for token in tokens if token not in string.punctuation]
        total_words += len(valid_words)

        # Check Phishing Lexicons
        phish_triggered = False
        for word in LEXICONS["phishing"]["time_pressure"]:
            if (" " in word and word in sentence_lower) or (word in valid_words):
                counts["time_pressure"] += 1
                phish_triggered = True
                
        for word in LEXICONS["phishing"]["certainty"]:
            if word in valid_words:
                counts["certainty"] += 1
                phish_triggered = True

        if phish_triggered:
            evidence["phishing_sentences"].add(sentence.strip())

        # Check Insider Threat Lexicons
        insider_triggered = False
        for word in LEXICONS["insider_threat"]["self_focused"]:
            if word in valid_words:
                counts["self_focused"] += 1
                insider_triggered = True
                
        for word in LEXICONS["insider_threat"]["negative_affect"]:
            if word in valid_words:
                counts["negative_affect"] += 1
                insider_triggered = True
                
        for word in LEXICONS["insider_threat"]["cognitive_process"]:
            if word in valid_words:
                counts["cognitive_process"] += 1
                insider_triggered = True

        if insider_triggered:
            evidence["insider_sentences"].add(sentence.strip())

    if total_words == 0:
        return None

    # Calculate Normalized Scores
    scores = {category: round((count / total_words) * 100, 2) for category, count in counts.items()}

    return {
        "total_words": total_words,
        "normalized_scores": scores,
        "extracted_evidence": {
            "phishing": list(evidence["phishing_sentences"]),
            "insider_threat": list(evidence["insider_sentences"])
        }
    }

def generate_actionable_report(log_id, analysis_results, output_file="forensic_report.json"):
    """
    Exports the normalized scores and the extracted evidence sentences 
    into a structured JSON file for investigator review.
    """
    report_data = {
        "LogID": log_id,
        "ThreatScores": analysis_results["normalized_scores"],
        "ContextualEvidence": analysis_results["extracted_evidence"]
    }
    
    with open(output_file, 'w') as f:
        json.dump(report_data, f, indent=4)
    print(f"[+] Actionable summary exported to {output_file}")

# --- Example Execution ---
if __name__ == "__main__":
    insider_text = """
    I am so frustrated with this unfair treatment. I always do my best, but my ideas are ignored. 
    I should rethink my future here. I hate this stupid process, and I might just resign.
    """
    
    results = analyze_and_preserve_evidence(insider_text)
    
    print("-" * 40)
    print("🚨 EVIDENCE EXTRACTED")
    print("-" * 40)
    for sentence in results['extracted_evidence']['insider_threat']:
        print(f"> \"{sentence}\"")
        
    generate_actionable_report(log_id=105, analysis_results=results)