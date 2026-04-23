import os
import json
from datetime import datetime
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found")

bot = Bot(token=TOKEN)
app = Flask(__name__)

DATA_FILE = "assignments.json"

# -------- DATA --------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# -------- HANDLERS --------
def start(update: Update, context: CallbackContext):
    name = update.message.from_user.first_name
    update.message.reply_text(f"Welcome {name}! 👋 Use /help")

def help_cmd(update: Update, context: CallbackContext):
    update.message.reply_text(
        "/add SUBJECT ASGN_DATE PROGRAM PRG_DATE\n"
        "/list\n"
        "/delete SUBJECT"
    )

def add(update: Update, context: CallbackContext):
    user_id = update.message.chat_id

    if len(context.args) != 4:
        update.message.reply_text("Usage: /add SUBJECT YYYY-MM-DD PROGRAM YYYY-MM-DD")
        return

    subject, asgn_due_date, program, prg_due_date = context.args

    try:
        datetime.strptime(asgn_due_date, "%Y-%m-%d")
        datetime.strptime(prg_due_date, "%Y-%m-%d")
    except ValueError:
        update.message.reply_text("Dates must be YYYY-MM-DD")
        return

    data = load_data()

    data.append({
        "user_id": user_id,
        "subject": subject,
        "asgn_due_date": asgn_due_date,
        "asgn_reminded": False,
        "program": program,
        "prg_due_date": prg_due_date,
        "prg_reminded": False
    })

    save_data(data)
    update.message.reply_text(f"Added {subject} ✅")

def list_tasks(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    data = load_data()

    tasks = [t for t in data if t["user_id"] == user_id]

    if not tasks:
        update.message.reply_text("No tasks found.")
        return

    msg = ""
    for t in tasks:
        msg += f"{t['subject']} → {t['asgn_due_date']}\n"

    update.message.reply_text(msg)

def delete(update: Update, context: CallbackContext):
    user_id = update.message.chat_id

    if len(context.args) != 1:
        update.message.reply_text("Usage: /delete SUBJECT")
        return

    subject = context.args[0]
    data = load_data()

    new_data = [t for t in data if not (t["user_id"] == user_id and t["subject"] == subject)]

    save_data(new_data)
    update.message.reply_text(f"Deleted {subject}")

# -------- DISPATCHER --------
dispatcher = Dispatcher(bot, None, workers=4)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_cmd))
dispatcher.add_handler(CommandHandler("add", add))
dispatcher.add_handler(CommandHandler("list", list_tasks))
dispatcher.add_handler(CommandHandler("delete", delete))
dispatcher.add_handler(MessageHandler(Filters.command, lambda u, c: u.message.reply_text("Unknown command")))

# -------- WEBHOOK --------
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# -------- HEALTH CHECK --------
@app.route("/")
def home():
    return "Bot is running"

# -------- RUN --------
if __name__ == "__main__":
    app.run(port=8080)