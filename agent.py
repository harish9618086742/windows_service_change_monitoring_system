from src.process_monitor import ProcessMonitor
from src.service_monitor import ServiceMonitor
from src.persistence_monitor import PersistenceMonitor
from src.alert_manager import AlertManager
import time

def main():
    alert_manager = AlertManager()
    pm = ProcessMonitor(alert_manager)
    sm = ServiceMonitor(alert_manager)
    pers = PersistenceMonitor(alert_manager)

    while True:
        print("[+] monitoring tick")
        pm.run()
        sm.run()
        pers.run()
        time.sleep(5)

if __name__ == "__main__":
    main()
