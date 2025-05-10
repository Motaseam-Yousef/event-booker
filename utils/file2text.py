from tika import parser

def clean_text(text):
    """
    Cleans the extracted text by removing extra spaces and newlines.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    if text:
        # Replace multiple spaces or newlines with a single space
        cleaned_text = ' '.join(text.split())
        return cleaned_text
    return ''

def extract_text_from_file(file_path):
    """
    Extracts text from a file using Tika and cleans it.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: Extracted and cleaned text from the file.
    """
    try:
        parsed = parser.from_file(file_path)
        text = parsed.get('content', '').strip()
        return clean_text(text)
    except Exception as e:
        return f"An error occurred: {e}"