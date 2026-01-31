# src/persistence_monitor.py
import winreg

RUN_KEYS = [
    (winreg.HKEY_LOCAL_MACHINE,
     r"Software\Microsoft\Windows\CurrentVersion\Run"),
    (winreg.HKEY_CURRENT_USER,
     r"Software\Microsoft\Windows\CurrentVersion\Run")
]

class PersistenceMonitor:
    def __init__(self, alert_manager):
        self.alert_manager = alert_manager

    def run(self):
        for hive, path in RUN_KEYS:
            try:
                key = winreg.OpenKey(hive, path)
                i = 0
                while True:
                    name, value, _ = winreg.EnumValue(key, i)
                    if "AppData" in value or "Temp" in value:
                        self.alert_manager.raise_alert({
                            "type": "StartupPersistence",
                            "entry": name,
                            "value": value
                        })
                    i += 1
            except:
                pass
