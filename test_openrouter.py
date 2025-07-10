#!/usr/bin/env python3
"""Test script for OpenRouter integration"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("Error: OPENROUTER_API_KEY not found in environment variables")
    print("Please set it in your .env file or export it")
    exit(1)

# Create OpenRouter client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Test with a simple prompt
try:
    print("Testing OpenRouter integration...")
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say 'Hello from OpenRouter!' if you're working correctly."}
        ]
    )
    
    print("✓ Success! Response:", response.choices[0].message.content)
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    print("\nMake sure:")
    print("1. Your OPENROUTER_API_KEY is valid")
    print("2. You have credits in your OpenRouter account")
    print("3. The model 'openai/gpt-3.5-turbo' is available")