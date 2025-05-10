import os
import uuid
from utils.file2text import extract_text_from_file
from utils.detect_language import detect_language

# Create temp directory if it doesn't exist
TEMP_DIR = "temp_events"
os.makedirs(TEMP_DIR, exist_ok=True)

def upload_file(file_path):
    """
    Extract text from event file and store it with a generated session ID.
    
    Args:
        file_path (str): Path to the event file
        
    Returns:
        str: Session ID for the uploaded event
    """
    event_text = extract_text_from_file(file_path)
    if len(event_text) <= 1:
        raise Exception("The file does not contain valid contract text.")

    session_id = str(uuid.uuid4())

    # Save to a temp file
    temp_path = os.path.join(TEMP_DIR, f"{session_id}.txt")
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(f"{event_text}")

    return session_id

def get_file(session_id):
    """
    Retrieve event data for a specific session from temp storage.
    
    Args:
        session_id (str): The session ID for the event
        
    Returns:
        dict: event data including text and language
    """
    temp_path = os.path.join(TEMP_DIR, f"{session_id}.txt")
    if not os.path.exists(temp_path):
        raise Exception("No event uploaded for this session.")
        
    with open(temp_path, 'r', encoding='utf-8') as f:
        content = f.read()
        language = detect_language(content)
        text = content
        
    return {
        "text": text,
        "language": language
    }

def has_file(session_id):
    """
    Check if a event event for a specific session.
    
    Args:
        session_id (str): The session ID to check
        
    Returns:
        bool: True if event exists, False otherwise
    """
    temp_path = os.path.join(TEMP_DIR, f"{session_id}.txt")
    return os.path.exists(temp_path)