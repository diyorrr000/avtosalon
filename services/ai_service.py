import requests
import json

class AIService:
    def __init__(self, model="1"):
        self.url = "https://zecora0.serv00.net/deepseek.php"
        self.model = model
        self.conversation_id = None

    def get_response(self, message):
        payload = {
            "model": self.model,
            "message": message
        }
        if self.conversation_id:
            payload["conversation_id"] = self.conversation_id

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=60)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.conversation_id = data.get("conversation_id")
                    return data.get("response", "No response content.")
                else:
                    return f"API Error: {data.get('response', 'Unknown error')}"
            else:
                return f"HTTP Error: {response.status_code}"
        except Exception as e:
            return f"Exception: {str(e)}"

    def reset_conversation(self):
        self.conversation_id = None
