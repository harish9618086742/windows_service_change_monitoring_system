# detection/rapid_respawn.py
import time
from collections import defaultdict

RESPAWN_WINDOW = 10
RESPAWN_THRESHOLD = 3
_cache = defaultdict(list)

def detect_rapid_respawn(proc):
    now = time.time()
    name = proc["name"]
    _cache[name].append(now)
    _cache[name] = [t for t in _cache[name] if now - t <= RESPAWN_WINDOW]
    return len(_cache[name]) >= RESPAWN_THRESHOLD
SUSPICIOUS_DIRS = ["\\users\\","\\temp\\","\\appdata\\"]

def is_path_suspicious(path):
    if not path:
        return False
    p = path.lower()
    return any(d in p for d in SUSPICIOUS_DIRS)

def detect_suspicious_path(proc):
    return is_path_suspicious(proc.get("exe",""))
SYSTEM = ["svchost.exe","lsass.exe","csrss.exe"]

def detect_masquerading(proc):
    if not proc.get("exe"):
        return False
    if proc['name'].lower() in SYSTEM:
        return "system32" not in proc['exe'].lower()
    return False
SUSPICIOUS = {
    "winword.exe": ["powershell.exe","cmd.exe"],
    "excel.exe": ["powershell.exe"]
}

def detect_parent_child(processes):
    alerts = []
    pid_map = {p['pid']:p for p in processes}
    for p in processes:
        parent = pid_map.get(p['ppid'])
        if parent:
            if parent['name'].lower() in SUSPICIOUS:
                if p['name'].lower() in SUSPICIOUS[parent['name'].lower()]:
                    alerts.append({
                        "type":"ParentChild",
                        "parent":parent['name'],
                        "child":p['name'],
                        "pid":p['pid']
                    })
    return alerts
