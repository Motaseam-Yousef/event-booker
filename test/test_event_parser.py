from models.event_parser import event_parser

# Test 1: Using session_id (from stored file)
print("=== Test 1: File-Based Event (English) ===")
try:
    result_file = event_parser(session_id="3a56d2e6-3852-479a-acb5-ccc1b9557c32", model="gpt-4o")
    print(result_file)
    print("✅ Parsed JSON (from session_id):")
    print(result_file["response"])
    print("Tokens used (in/out):", result_file["input_token"], "/", result_file["output_token"])
except Exception as e:
    print("❌ File-Based Test Failed:", e)


# Test 2: Using direct user_text input
print("\n=== Test 2: Direct Text Input ===")
try:
    text_input = (
        "Join our hybrid workshop 'Startup Strategies 2025' on July 20 from 9AM–5PM Dubai time, "
        "held both at Dubai Expo Center and online. Topics: startup funding, marketing, scaling. "
        "Early Bird ticket: 300 AED. VIP ticket: 800 AED with private mentoring. Banner: https://events.com/img.jpg"
    )
    result_direct = event_parser(user_text=text_input, model="gpt-4o")
    print("✅ Parsed JSON (from user_text):")
    print(result_direct["response"])
    print("Tokens used (in/out):", result_direct["input_token"], "/", result_direct["output_token"])
except Exception as e:
    print("❌ Direct Input Test Failed:", e)
