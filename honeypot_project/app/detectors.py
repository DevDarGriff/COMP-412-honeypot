from collections import Counter
from app.config import SUSPICIOUS_PATHS, SUSPICIOUS_USER_AGENTS, REPEAT_ATTEMPT_THRESHOLD

source_counter = Counter()

def classify_event(service: str, source_ip: str, path: str, user_agent: str, event_type: str) -> list[str]:
    labels = []

    source_counter[source_ip] += 1

    if path in SUSPICIOUS_PATHS:
        labels.append("recon")

    ua_lower = (user_agent or "").lower()
    if any(token in ua_lower for token in SUSPICIOUS_USER_AGENTS):
        labels.append("scanner")

    if event_type == "login_attempt":
        labels.append("credential_attack")
    
    if source_counter[source_ip] >= REPEAT_ATTEMPT_THRESHOLD:
        labels.append("repeat_source")
    
    if not labels:
        labels.append("generic_activity")

    return labels
