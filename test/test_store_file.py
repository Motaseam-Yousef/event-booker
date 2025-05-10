import os
from models.file_store import upload_file, get_file, has_file

print("=== Test: Upload & Retrieve file ===")

test_file_path = "path"
with open(test_file_path, "w", encoding="utf-8") as f:
    f.write("This is a sample file written in English.")

try:
    session_id = upload_file(test_file_path)
    print(f"✅ file uploaded. Session ID: {session_id}")
except Exception as e:
    print(f"❌ Upload failed: {e}")
    exit()


if has_file(session_id):
    print("✅ file exists for session.")
else:
    print("❌ file does NOT exist for session.")

try:
    file_data = get_file(session_id)
    print("✅ file retrieved successfully:")
    print("Text:", file_data['text'])
    print("Language:", file_data['language'])
except Exception as e:
    print("❌ Retrieval failed:", e)


# os.remove(test_file_path)
# os.remove(os.path.join("temp_files", f"{session_id}.txt"))
