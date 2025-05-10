from utils.file2text import clean_text, extract_text_from_file

# Replace with real file path if needed
file_path = "/home/motaseam/Downloads/a.txt"
text = extract_text_from_file(file_path)
print("Extracted Text:", clean_text(text))
