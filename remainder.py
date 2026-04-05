import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Bot

# Load token
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in .env file")

DATA_FILE = "assignments.json"
bot = Bot(token=TOKEN)

today = datetime.today().date()
tomorrow = today + timedelta(days=1)

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()
updated = False

for task in data:
    try:
        due = datetime.strptime(task["asgn_due_date"], "%Y-%m-%d").date()
        prg_due = datetime.strptime(task["prg_due_date"], "%Y-%m-%d").date()
    except ValueError:
        print(f"Skipping invalid date format: {task}")
        continue

    if due == tomorrow and not task.get("asgn_reminded", False):
        try:
            chat = bot.get_chat(chat_id=task["user_id"])
            name = chat.first_name or "friend"
            
            bot.send_message(
                chat_id=task["user_id"],
                text=f"hey {name} 🌸\njust a little reminder that your Final assignment {task['subject']}  is due tomorrow\ndo it calmly, no stress. i'm rooting for you 💪"
            )
            task["asgn_reminded"] = True
            updated = True
            print(f"Reminder sent to {name} ({task['user_id']}) for {task['subject']}")
        except Exception as e:
            print(f"Failed to send message: {e}")
    if prg_due == tomorrow and not task.get("prg_reminded", False):
        try:
            chat = bot.get_chat(chat_id=task["user_id"])
            name = chat.first_name or "friend"
            
            bot.send_message(
                chat_id=task["user_id"],
                text=f"hey {name} baby just a little reminder to check if the Google apprentice program is open yet don’t miss it this time 😘 bye babe 😘😘"
            )
            task["prg_reminded"] = True
            updated = True
            print(f"Reminder sent to {name} ({task['user_id']}) for {task['program']}")
        except Exception as e:
            print(f"Failed to send message: {e}")

if updated:
    save_data(data)
    print("files updated.")
else:
    print("No reminders to send today.")
