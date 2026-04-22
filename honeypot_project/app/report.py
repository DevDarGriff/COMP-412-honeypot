import json
from collections import Counter
from app.config import LOG_FILE


def load_events():
    events = []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
    except FileNotFoundError:
        pass
    return events


def main():
    events = load_events()

    if not events:
        print("No events found.")
        return
    
    total_events = len(events)
    services = Counter(e.get("service", "") for e in events)
    event_types = Counter(e.get("event_type", "") for e in events)
    usernames = Counter(
        e.get("username", "") for e in events if e.get("username")
    )
    paths = Counter(e.get("path", "") for e in events if e.get("path"))
    sources = Counter(e.get("source_ip", "") for e in events)
    labels = Counter(label for e in events for label in e.get("labels", []))

    print("=" * 50)
    print("HONEYPOT SUMMARY REPORT")
    print("=" * 50)
    print(f"Total events: {total_events}")
    print()

    print("Service breakdown:")
    for service, count in services.most_common():
        print(f"  {service}: {count}")

    print()
    print("Event types:")
    for event_type, count in event_types.most_common():
        print(f"  {event_type}: {count}")

    if paths:
        print()
        print("Top requested paths:")
        for path, count in paths.most_common(10):
            print(f"  {path}: {count}")

    if usernames:
        print()
        print("Top usernames:")
        for username, count in usernames.most_common(10):
            print(f"  {username}: {count}")

    print()
    print("Top source IPs:")
    for source, count in sources.most_common(10):
        print(f"  {source}: {count}")

    print()
    print("Labels:")
    for label, count in labels.most_common():
        print(f"  {label}: {count}")

if __name__ == "__main__":
    main()
