# core/risk_engine.py
RISK_WEIGHTS = {
    "ParentChild": 40,
    "Masquerading": 50,
    "SuspiciousPath": 30,
    "UnsignedBinary": 25,
    "StartupPersistence": 30,
    "SuspiciousService": 35,
    "RapidRespawn": 20
}

def score(events):
    score = 0
    for e in events:
        score += RISK_WEIGHTS.get(e["type"], 0)
    return score
