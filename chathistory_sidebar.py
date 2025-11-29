from datetime import datetime, timedelta

def group_chats_by_time(chats):
    """
    chats: list of (id, name, created_at) from get_chats()
    returns dict: { "Today": [...], "This week": [...], "This month": [...], "Older": [...] }
    """
    buckets = {
        "Today": [],
        "This week": [],
        "This month": [],
        "Older": [],
    }

    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)
    week_start = today_start - timedelta(days=today_start.weekday())  # Monday as start
    month_start = datetime(now.year, now.month, 1)

    for chat_id, name, created_at in chats:
        # created_at is "YYYY-MM-DD HH:MM:SS" from SQLite's CURRENT_TIMESTAMP
        try:
            created_dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Fallback if you ever change format to ISO
            created_dt = datetime.fromisoformat(created_at)

        if created_dt >= today_start:
            buckets["Today"].append((chat_id, name, created_dt))
        elif created_dt >= week_start:
            buckets["This week"].append((chat_id, name, created_dt))
        elif created_dt >= month_start:
            buckets["This month"].append((chat_id, name, created_at))
        else:
            buckets["Older"].append((chat_id, name, created_dt))

    return buckets
