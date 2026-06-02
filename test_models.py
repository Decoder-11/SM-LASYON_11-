import google.generativeai as genai
from sirlar import GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)
models = genai.list_models()
for m in models:
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
