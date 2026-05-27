# Nudgify BOT

A small Telegram reminder bot that stores assignments and program deadlines, and sends reminder messages the day before a due date.

## What this project does

The project has two main parts:

1. **Bot app (`app.py`)**
   - Starts a Flask web server.
   - Receives Telegram updates on the `/webhook` route.
   - Handles Telegram commands such as:
     - `/start`
     - `/help`
     - `/add SUBJECT YYYY-MM-DD PROGRAM YYYY-MM-DD`
     - `/list`
     - `/delete SUBJECT`

2. **Reminder script (`remainder.py`)**
   - Reads the saved task data from `assignments.json`.
   - Checks which tasks are due tomorrow.
   - Sends reminder messages to Telegram users.
   - Marks reminder flags as sent so the same reminder is not repeated.

---

## Variables and values you can change

### 1. Telegram bot token
- Variable: `TELEGRAM_TOKEN`
- Where it is used:
  - `app.py`
  - `remainder.py`
- Purpose:
  - Authenticates the bot with Telegram.
- How to set it:
  - Put it in a `.env` file in the project root.

Example:
```env
TELEGRAM_TOKEN=your_bot_token_here
```

### 2. Data file location
- Variable: `DATA_FILE = "assignments.json"`
- Where it is used:
  - `app.py`
  - `remainder.py`
- Purpose:
  - Stores all user tasks and reminder status.
- You can change it if you want to use another JSON file.

### 3. Task fields stored in each entry
Each task in `assignments.json` contains:

- `user_id`: Telegram chat ID of the user
- `subject`: assignment subject name
- `asgn_due_date`: due date for the assignment (`YYYY-MM-DD`)
- `asgn_reminded`: whether the assignment reminder was already sent
- `program`: program name
- `prg_due_date`: due date for the program reminder (`YYYY-MM-DD`)
- `prg_reminded`: whether the program reminder was already sent

You can change these values by editing the JSON file or by adding new tasks with `/add`.

### 4. Reminder timing
The reminder script checks whether a task is due on `tomorrow`:

```python
today = datetime.today().date()
tomorrow = today + timedelta(days=1)
```

This means the bot sends reminders for tasks due the next day.
If you want reminders earlier or later, you can change this logic in `remainder.py`.

### 5. Bot message text
The reminder messages are hardcoded in `remainder.py`.
You can change the text to make the reminders sound more formal, friendly, or personalized.

---

## How the project works

### Flow 1: Starting the bot
- The Flask app starts with `app.run(port=8080)` in `app.py`.
- Telegram sends updates to the `/webhook` route.
- The bot processes the incoming message and runs the matching command handler.

### Flow 2: Adding a task
When a user sends:

```text
/add blockchain 2026-04-15 application 2026-05-01
```

the bot:
1. Validates the dates.
2. Reads the current JSON data.
3. Appends a new task entry.
4. Saves it back to `assignments.json`.

### Flow 3: Listing tasks
The `/list` command reads the JSON file and shows only the tasks belonging to the current Telegram user.

### Flow 4: Deleting a task
The `/delete SUBJECT` command removes one task for the current user.

### Flow 5: Sending reminders
The `remainder.py` script:
1. Loads `assignments.json`
2. Finds tasks whose due dates are tomorrow
3. Sends Telegram messages to the relevant users
4. Updates the reminder flags in the JSON file

---

## Project files

- `app.py` – main Telegram bot and webhook server
- `remainder.py` – reminder sender script
- `assignments.json` – task storage file
- `requirements.txt` – Python dependencies
- `Dockerfile` – container setup for deployment

---

## Setup notes

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your bot token:
   ```env
   TELEGRAM_TOKEN=your_token_here
   ```

3. Run the bot locally:
   ```bash
   python app.py
   ```

4. Run the reminder script when needed:
   ```bash
   python remainder.py
   ```

---

## Quick summary

The main configurable parts are:
- `TELEGRAM_TOKEN`
- `assignments.json`
- task dates (`YYYY-MM-DD`)
- reminder flags (`asgn_reminded`, `prg_reminded`)
- reminder message text in `remainder.py`
