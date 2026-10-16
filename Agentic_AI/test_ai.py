import os
from openai import OpenAI

key = os.getenv("OPENAI_API_KEY", "")

print("Key found:", bool(key))
print("Placeholder still set:", "PASTE_YOUR_API_KEY_HERE" in key)

if not key or "PASTE_YOUR_API_KEY_HERE" in key:
    print('Set your real key using: set "OPENAI_API_KEY=YOUR_REAL_KEY"')
    raise SystemExit

client = OpenAI(api_key=key)

response = client.responses.create(
    model="gpt-5.1",
    input="Say hello"
)

print(response.output_text)
