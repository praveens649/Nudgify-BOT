import json
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import MessageHandler, Filters

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in .env file")

DATA_FILE = "assignments.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def unknown(update: Update, context: CallbackContext):
    name = update.message.from_user.first_name
    update.message.reply_text(
        f"Hey {name}, I didn't understand that command 🧠\n"
        "Use /help to see available commands."
    )
def start(update: Update, context: CallbackContext):
    name = update.message.from_user.first_name
    update.message.reply_text(
        f"Welcome {name}! 👋\n\n"
        "Commands:\n"
        "/add SUBJECT YYYY-MM-DD\n"
        "/list - Show your tasks\n"
        "/delete SUBJECT - Delete a task\n"
        "/help - Show this help message"
    )


def add(update: Update, context: CallbackContext):
    user_id = update.message.chat_id

    if len(context.args) != 2:
        update.message.reply_text("(Sample)Usage ==> /add <remainder_task_name> YYYY-MM-DD")
        return

    subject, due_date = context.args

    # Validate date
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        update.message.reply_text("Date must be in YYYY-MM-DD format.")
        return

    data = load_data()

    # Prevent duplicates
    for task in data:
        if task["user_id"] == user_id and task["subject"] == subject:
            update.message.reply_text("Task already exists.")
            return

    data.append({
        "user_id": user_id,
        "subject": subject,
        "due_date": due_date,
        "reminded": False
    })

    save_data(data)
    name = update.message.from_user.first_name
    update.message.reply_text(f"Got it {name}! ✅ Added {subject} due on {due_date}")

def delete(update: Update, context: CallbackContext):
    user_id = update.message.chat_id

    if len(context.args) != 1:
        update.message.reply_text("Usage: /delete SUBJECT")
        return

    subject = context.args[0]
    data = load_data()

    new_data = [t for t in data if not (t["user_id"] == user_id and t["subject"] == subject)]

    if len(new_data) == len(data):
        update.message.reply_text("Task not found.")
        return

    save_data(new_data)
    name = update.message.from_user.first_name
    update.message.reply_text(f"Done {name}! 🗑️ Deleted {subject}")

def list_tasks(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    name = update.message.from_user.first_name
    data = load_data()

    tasks = [t for t in data if t["user_id"] == user_id]

    if not tasks:
        update.message.reply_text(f"No tasks found for you, {name}.")
        return

    msg = f"📋 {name}'s Tasks:\n\n" + "\n".join([f"• {t['subject']} → {t['due_date']}" for t in tasks])
    update.message.reply_text(msg)
def help_cmd(update: Update, context: CallbackContext):
    name = update.message.from_user.first_name
    update.message.reply_text(
        f"Here you go {name}! 📖\n\n"
        "Commands:\n"
        "/add SUBJECT YYYY-MM-DD - Add a task\n"
        "/list - Show your tasks\n"
        "/delete SUBJECT - Remove a task"
    )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("list", list_tasks))
    dp.add_handler(CommandHandler("delete", delete))
    dp.add_handler(CommandHandler("help", help_cmd))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    print("Bot running...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
