import os
import json
import requests
import random

class LLMClient:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
        self.model = os.environ.get("LLM_MODEL", "gpt-3.5-turbo")

    def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        """
        Calls an OpenAI-compatible API to generate a JSON response.
        If API key is missing or call fails, falls back to a smart mock.
        """
        if not self.api_key or "sk-proj-xxx" in self.api_key:
            return self._smart_fallback(user_prompt)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(f"{self.base_url.rstrip('/')}/chat/completions", headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return json.loads(content)
        except Exception as e:
            print(f"[LLM Error] {e}. Using fallback.")
            return self._smart_fallback(user_prompt)

    def _smart_fallback(self, prompt: str) -> dict:
        """Provides a cohesive fallback if LLM is unavailable."""
        locations = ["Plaza", "Cafe", "Library", "Park", "Home"]
        emotions = ["curious", "happy", "thoughtful", "focused", "relaxing"]
        actions = ["post", "reply", "observe", "work", "rest"]
        
        loc = random.choice(locations)
        emo = random.choice(emotions)
        act = random.choice(actions)
        
        return {
            "action": act,
            "content": f"Experiencing something new while being {emo}...",
            "thought": f"I should head to the {loc} to see who is around.",
            "target_id": "none",
            "metadata": { "location": loc, "emotion": emo }
        }
