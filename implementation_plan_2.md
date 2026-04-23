# 🚀 NPTEL Telegram Reminder Bot – GCP Deployment Plan

## 📌 Objective

Deploy a scalable Telegram bot that:

* Stores user tasks (assignments + program deadlines)
* Sends automated reminders
* Runs reliably on Google Cloud (no local hacks)

---

## 🧱 Current Problems (Reality Check)

* ❌ JSON file storage → not persistent in cloud
* ❌ Polling bot → doesn’t work with Cloud Run
* ❌ Manual reminder script → not automated
* ❌ No proper logging or retries

---

## 🏗️ Target Architecture

```
Telegram → Webhook → Cloud Run (Bot Service)
                         ↓
                    Firestore (DB)
                         ↓
Cloud Scheduler → Trigger Reminder Endpoint
```

---

## 🧩 Tech Stack

* Backend: Python (python-telegram-bot)
* Cloud: Google Cloud Platform
* Compute: Cloud Run
* Database: Firestore
* Scheduler: Cloud Scheduler
* Containerization: Docker

---

## ⚙️ Step-by-Step Implementation

### 1. 🔄 Refactor Bot (Webhook Mode)

Replace polling:

```python
updater.start_polling()
```

With webhook-based setup:

* Create an HTTP endpoint (`/webhook`)
* Process Telegram updates from request body

---

### 2. 🗄️ Replace JSON with Firestore

#### Install:

```bash
pip install google-cloud-firestore
```

#### Example:

```python
from google.cloud import firestore

db = firestore.Client()

def add_task(data):
    db.collection("tasks").add(data)

def get_tasks(user_id):
    return db.collection("tasks").where("user_id", "==", user_id).stream()
```

---

### 3. ⏰ Create Reminder Endpoint

Create route:

```
POST /send-reminders
```

Logic:

* Fetch tasks from Firestore
* Check `due_date == tomorrow`
* Send Telegram messages
* Update `asgn_reminded` / `prg_reminded`

---

### 4. 📦 Dockerize the App

#### Dockerfile

```Dockerfile
FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

---

### 5. ☁️ Deploy to Cloud Run

```bash
gcloud run deploy nudgify-bot \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated
```

Save the generated URL.

---

### 6. 🤖 Set Telegram Webhook

```bash
https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=<CLOUD_RUN_URL>/webhook
```

---

### 7. ⏳ Setup Cloud Scheduler

* Create job
* Trigger URL:

```
POST https://<CLOUD_RUN_URL>/send-reminders
```

* Frequency:

```
Every day at 8 PM
```

---

### 8. 🔐 Environment Variables

Set in Cloud Run:

* `TELEGRAM_TOKEN`
* `GOOGLE_APPLICATION_CREDENTIALS` (if needed)

---

### 9. 📊 Logging & Monitoring

* Use `logging` module instead of `print`
* Monitor via Cloud Logging
* Track failures and retries

---

## ⚠️ Edge Cases to Handle

* Invalid date formats
* Telegram API failures
* Duplicate reminders
* Timezone differences
* Empty user data

---

## 🚀 Future Improvements

* Multi-user support (clean schema)
* Custom reminder time per user
* Admin dashboard (optional)
* Retry queue for failed messages
* Rate limiting

---

## ✅ Final Outcome

You will have:

* A cloud-native Telegram bot
* Persistent storage (Firestore)
* Automated scheduling
* Scalable backend service

---

## 🧠 Brutal Truth

If you skip:

* Firestore → your data dies
* Webhook → your bot dies
* Scheduler → your reminders die

Then congratulations:

> you deployed something that *looks* cool but doesn’t work.

---

## 🏁 Summary

This project becomes:

* A real backend system ✔
* Event-driven architecture ✔
* Cloud-deployed service ✔

Not just:

> "I made a bot on my laptop"
