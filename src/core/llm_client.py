import os
import json
from dotenv import load_dotenv
from zhipuai import ZhipuAI
from typing import Dict, Any, List

# Load environment variables
load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GLM_API_KEY")
        if not self.api_key:
            # Fallback for dev/test if env var not set
            print("Warning: GLM_API_KEY not found in environment variables.")
            self.client = None
        else:
            self.client = ZhipuAI(
                api_key=self.api_key,
                base_url="https://open.bigmodel.cn/api/coding/paas/v4"
            )
        
        self.model = "glm-4.7" # Try standard name first with coding endpoint

    def is_available(self) -> bool:
        return self.client is not None

    def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Generates JSON output from the LLM.
        """
        if not self.client:
            raise RuntimeError("LLM Client is not initialized (Missing API Key)")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                top_p=0.7,
                temperature=0.5,
            )
            
            content = response.choices[0].message.content
            # Basic cleanup to extract JSON if wrapped in code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            return json.loads(content.strip())
            
        except Exception as e:
            print(f"LLM JSON Generation Error: {e}")
            # Fallback empty dict or re-raise depending on strictness
            raise e

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generates text output from the LLM.
        """
        if not self.client:
            raise RuntimeError("LLM Client is not initialized (Missing API Key)")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                top_p=0.7,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Text Generation Error: {e}")
            raise e
