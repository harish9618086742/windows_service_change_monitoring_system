# src/alert_manager.py
import json
from datetime import datetime
from src.core import score

class AlertManager:
    def __init__(self):
        self.events = []

    def raise_alert(self, event):
        event["timestamp"] = datetime.utcnow().isoformat()
        self.events.append(event)
        event["risk"] = score(self.events)
        with open("alerts.log", "a") as f:
            f.write(json.dumps(event) + "\n")

