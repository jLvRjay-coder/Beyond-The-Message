import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
resp = client.models.list()

print([m.id for m in resp.data if "gpt" in m.id][:5])

