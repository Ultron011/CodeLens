import json
import os

class ChatMemory:
    def __init__(self, file_path=".codelens_db/history.json"):
        self.file_path = file_path

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return []

    def save(self, question, answer):
        history = self.load()
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        
        # Keep only the last 10 messages to save tokens
        with open(self.file_path, "w") as f:
            json.dump(history[-10:], f)
            
    def clear(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)