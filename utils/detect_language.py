def detect_language(text):
    """
    Detects whether the given text is in Arabic, English, or neither.
    Priority is given to Arabic: if any Arabic letter is found, 
    the text is considered Arabic. If no Arabic letter is found,
    it checks for English letters.
    
    Args:
        text (str): The input string
    
    Returns:
        str: 'Arabic' if text is Arabic, 'English' if text is English, 
             or 'UNKNOWN' if neither.
    """
    # Define the Unicode range for Arabic characters
    arabic_start = 0x0600
    arabic_end = 0x06FF
    
    # Define the range for English letters
    english_letters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    has_arabic = False
    has_english = False

    # Check characters in the text
    for char in text:
        if arabic_start <= ord(char) <= arabic_end:
            has_arabic = True
        elif char in english_letters:
            has_english = True
    
    if has_arabic:
        return "Arabic"
    elif has_english:
        return "English"
    else:
        return "UNKNOWN"