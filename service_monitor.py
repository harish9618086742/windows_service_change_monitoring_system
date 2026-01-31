# src/service_monitor.py
import wmi
from src.detection import is_path_suspicious

class ServiceMonitor:
    def __init__(self, alert_manager):
        self.alert_manager = alert_manager

    def run(self):
        c = wmi.WMI()
        for s in c.Win32_Service():
            if s.StartMode == "Auto" and s.PathName:
                if is_path_suspicious(s.PathName):
                    self.alert_manager.raise_alert({
                        "type": "SuspiciousService",
                        "service": s.Name,
                        "path": s.PathName,
                        "account": s.StartName
                    })


