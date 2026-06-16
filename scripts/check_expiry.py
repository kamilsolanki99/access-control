import json
from datetime import datetime, date

USERS_FILE = "users.json"
TODAY = date.today()

with open(USERS_FILE, "r") as f:
    data = json.load(f)

changed = False
for username, user in data.get("users", {}).items():
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
    print("no expired users found")
