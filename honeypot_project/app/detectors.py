from collections import Counter
from app.config import (
    SUSPICIOUS_PATHS, 
    SUSPICIOUS_USER_AGENTS, 
    REPEAT_ATTEMPT_THRESHOLD,
    COMMON_ATTACK_USERNAMES,
)

source_counter = Counter()

def classify_event(
    service: str, 
    source_ip: str, 
    path: str = "", 
    user_agent: str = "", 
    event_type: str = "",
    username: str = "",
) -> list[str]:
    labels = []

    source_counter[source_ip] += 1

    if service == "http" and path in SUSPICIOUS_PATHS:
        labels.append("recon")

    ua_lower = (user_agent or "").lower()
    if any(token in ua_lower for token in SUSPICIOUS_USER_AGENTS):
        labels.append("scanner")

    if event_type in {"login_attempt", "ssh_auth_attempt", "telnet_auth_attempt"}:
        labels.append("credential_attack")
    
    if username and username.lower() in COMMON_ATTACK_USERNAMES:
        labels.append("common_username")

    if service in {"ssh", "telnet"}:
        labels.append("remote_access_probe")
    
    if source_counter[source_ip] >= REPEAT_ATTEMPT_THRESHOLD:
        labels.append("repeat_source")
    
    if not labels:
        labels.append("generic_activity")

    return labels
