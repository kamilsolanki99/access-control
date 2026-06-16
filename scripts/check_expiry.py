import json
from datetime import datetime, date, timedelta
import calendar

USERS_FILE = "users.json"
TODAY = date.today()

with open(USERS_FILE, "r") as f:
    data = json.load(f)

changed = False
for username, user in data.get("users", {}).items():
    paid_until = user.get("paid_until")

    if paid_until:
        paid = datetime.strptime(paid_until, "%d-%m-%y").date()
        # expiry = paid + 1 month - 1 day
        month = paid.month + 1
        year = paid.year
        if month > 12:
            month = 1
            year += 1
        last_day = calendar.monthrange(year, month)[1]
        day = min(paid.day, last_day)
        calculated_expiry = date(year, month, day) - timedelta(days=1)

        if user.get("expiry") != calculated_expiry.strftime("%d-%m-%y"):
            user["expiry"] = calculated_expiry.strftime("%d-%m-%y")
            changed = True
            print(f"{username}: expiry recalculated to {user['expiry']}")

    expiry_str = user.get("expiry")
    if expiry_str and user.get("status") == "on":
        try:
            expiry = datetime.strptime(expiry_str, "%d-%m-%y").date()
            if TODAY > expiry:
                user["status"] = "off"
                changed = True
                print(f"{username}: expired {expiry_str}, set to off")
        except ValueError as e:
            print(f"{username}: invalid expiry format '{expiry_str}' - {e}")

if changed:
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print("users.json updated")
else:
    print("no changes needed")
