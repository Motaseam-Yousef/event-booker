import os
from utils.llm_utils import generate_response
from dotenv import load_dotenv
load_dotenv()
# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
print("=== Test: Chat Completion with Only 'user' Role ===")
messages = [
    {"role": "user", "content": "Tell me a joke"}
]
try:
    res = generate_response(messages=messages)
    print("Response:", res["response"])
    print("Tokens (in/out):", res["input_token"], "/", res["output_token"])
except Exception as e:
    print("Error:", e)


print("\n=== Test: Chat Completion with 'system' and 'user' ===")
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Summarize World War II in one sentence."}
]
try:
    res = generate_response(messages=messages)
    print("Response:", res["response"])
    print("Tokens (in/out):", res["input_token"], "/", res["output_token"])
except Exception as e:
    print("Error:", e)


print("\n=== Test: Chat Completion with Temperature and JSON Output ===")
messages = [
    {"role": "user", "content": "Give me a JSON with your name and version."}
]
try:
    res = generate_response(messages=messages, temperature=0.7, json_response=True)
    print("Response:", res["response"])
    print("Tokens (in/out):", res["input_token"], "/", res["output_token"])
except Exception as e:
    print("Error:", e)
