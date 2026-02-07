import sys
import os
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

try:
    from src.core.llm_client import LLMClient
except ImportError:
    # Fallback if running directly without package structure
    sys.path.append(str(project_root / "src"))
    from core.llm_client import LLMClient

def main():
    print("Initializing LLMClient...")
    try:
        client = LLMClient()
    except Exception as e:
        print(f"Failed to initialize LLMClient: {e}")
        return

    if not client.is_available():
        print("Error: GLM_API_KEY is missing or invalid.")
        return

    print("Sending test request to GLM-4...")
    system_prompt = "You are a helpful assistant."
    user_prompt = "Hello! Please reply with 'Connection Successful!' if you can read this."

    try:
        response = client.generate_text(system_prompt, user_prompt)
        print("\n--- Response from GLM ---")
        print(response)
        print("-------------------------")
        print("Test passed!")
    except Exception as e:
        print(f"\nTest failed with error: {e}")

if __name__ == "__main__":
    main()
