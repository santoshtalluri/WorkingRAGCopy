import os
from dotenv import load_dotenv

# Load environment variables
try:
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f'✅ API Key Loaded: {api_key[:5]}**********')
    else:
        print('❌ OPENAI_API_KEY not found in .env file or not set')
except Exception as e:
    print(f'❌ Error loading environment variables: {e}')
