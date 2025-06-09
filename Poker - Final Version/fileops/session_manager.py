import os
import json
from datetime import datetime

class SessionManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def save_session(self, session: dict) -> None:
        game_id = session.get("game_id")
        if not game_id:
            raise ValueError("Brakuje game_id w sesji.")

        file_path = os.path.join(self.data_dir, f"session_{game_id}.json")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(session, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Błąd zapisu sesji: {e}")

    def load_session(self, game_id: str) -> dict:
        file_path = os.path.join(self.data_dir, f"session_{game_id}.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Nie znaleziono pliku sesji.")
            return {}
        except json.JSONDecodeError:
            print("Błąd odczytu pliku sesji (niepoprawny JSON).")
            return {}
