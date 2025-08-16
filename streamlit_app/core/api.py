import requests
from typing import List, Dict, Any

class BackendClient:
    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")

    # --- Auth ---
    def login(self, username: str, password: str) -> Dict[str, Any]:
        url = f"{self.base}/api/v1/auth/login"
        payload = {"username": username, "password": password}
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()

    # --- Chat ---
    def chat(self, message: str, persona: str, history: List[Dict[str, str]], temperature: float, token: str) -> Dict[str, Any]:
        url = f"{self.base}/api/v1/chat/"
        payload = {"message": message, "persona": persona, "history": history, "temperature": temperature}
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        r.raise_for_status()
        return r.json()

    # --- History ---
    def get_history(self, persona: str, token: str) -> List[Dict[str, str]]:
        url = f"{self.base}/api/v1/chat/history/{persona}"
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200:
            return r.json().get("history", [])
        return []

    def clear_history(self, persona: str, token: str) -> None:
        url = f"{self.base}/api/v1/chat/history/{persona}"
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.delete(url, headers=headers, timeout=30)
        r.raise_for_status()

    def get_analytics(self, token: str):
        """Fetch analytics (total chats, most used persona, top prompts) from backend"""
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{self.base}/api/v1/analytics/summary", headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()
