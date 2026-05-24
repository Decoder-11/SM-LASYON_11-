import os
import requests
import json

api_key = "AIzaSyDuLoWDmUjD4CytMv1-IRRRR1Oin3sXlog"

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
r = requests.get(url)
if r.status_code == 200:
    data = r.json()
    valid_models = []
    for m in data.get("models", []):
        if "generateContent" in m.get("supportedGenerationMethods", []):
            valid_models.append(m["name"])
    print("VALID GENERATIVE MODELS:")
    for vm in valid_models:
        print(vm)
else:
    print("API GET ERROR:", r.status_code, r.text)

