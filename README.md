# Kornofuli — Coaching Center Management System

একটি সম্পূর্ণ **Coaching Center Management System**, যা একটি কোচিং সেন্টারের
যাবতীয় কাজ — শিক্ষার্থী ব্যবস্থাপনা, উপস্থিতি (attendance), বেতন (payment),
পরীক্ষা ও ফলাফল, PDF রিপোর্ট এবং ওয়েবসাইট কনটেন্ট ম্যানেজমেন্ট — এক জায়গায়
সমাধান করে। Django 6 + PostgreSQL + Supabase দিয়ে তৈরি।

---

## Features

### 1. Public Website (home)
- Hero / stats / course / teacher / result / notice / gallery / FAQ / batch schedule
- PWA (manifest.json, sw.js)
- Notice add/edit/delete
- `manage/settings/` ও `manage/<model>/` দিয়ে সাইট কনটেন্ট সহজে আপডেট করা যায়

### 2. Accounts & Student Management (accounts)
- Custom `User` model (`role`: Teacher / Student)
- Login / Logout
- Class (ClassRoom) add / list
- Student add / list, guardian phone, school name
- Student approval flow (`is_approved`)
- Monthly payment tracking (`Payment`)
- Daily attendance (`Attendance`: present / absent / late)

### 3. Exam & Result (exams)
- Exam create (Weekly / Monthly / Mid Term / Final)
- Subject add per exam (full marks, pass marks, optional/4th subject)
- Mark entry per student
- Automatic GPA + letter grade calculation (Bangladesh board rule)
- Result summary + **PDF download** (reportlab)

### 4. Reports (reports)
- Per-student report (teacher view)

---

## Tech Stack

- Python 3.12
- Django 6.0
- PostgreSQL (Supabase)
- psycopg2-binary, dj-database-url, python-decouple
- reportlab (PDF), Pillow (images)
- requests (SMS API: BulkSMS)
- Docker (dev & prod)

---

## Project Structure

```
kornofuli/
├── kornofuli/          # Project config (settings, urls)
├── accounts/           # User, Student, ClassRoom, Payment, Attendance
├── exams/              # Exam, Subject, Result, MarkEntry + PDF
├── reports/            # Student report
├── home/               # Public website + content management
├── static/             # Static files (CSS/JS/PWA)
├── media/              # Uploaded files (teacher photos, gallery, notices)
├── templates/          # Shared templates
├── manage.py
├── .env                # Environment variables (NOT committed)
├── docker-compose.yml
├── Dockerfile.dev
├── Dockerfile.prod
└── requirements.txt
```

---

## Setup (Local Development)

### Prerequisites
- Python 3.12+
- PostgreSQL (অথবা Supabase account)

### 1. Virtual environment & install

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
```

### 2. .env file

`.env.example` থেকে কপি করে `.env` বানান (`.env` git-এ যাবে না):

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

# Supabase / PostgreSQL connection
DATABASE_URL=postgresql://postgres:PASSWORD@db.<your-ref>.supabase.co:5432/postgres

# BulkSMS
BULKSMS_API_KEY=your-key
BULKSMS_SENDER_ID=your-sender-id
```

### 3. Migrate & run

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`http://127.0.0.1:8000/` এ সাইট, `http://127.0.0.1:8000/admin/` এ admin.

### SQLite (optional, local dev)

`kornofuli/settings.py` এ `DATABASES` কমেন্ট-আউট করা sqlite ব্লকটি ব্যবহার করুন।

---

## Docker

### Development
```bash
docker compose up --build
```

### Production
```bash
docker build -f Dockerfile.prod -t kornofuli .
docker run -p 8000:8000 --env-file .env kornofuli
```

---

## Supabase Setup

1. [supabase.com/dashboard](https://supabase.com/dashboard) এ project তৈরি করুন।
2. **Project Settings → Database → Connection string** থেকে `DATABASE_URL` নিন
   (password URL-encode করুন, যেমন `@` হলে `%40`)।
3. `.env` এ বসিয়ে `python manage.py migrate` চালান।

> **Note:** Free-tier project কিছুদিন inactive থাকলে **pause** হয়ে যায়,
> তখন connection fail করে (`could not translate host name ... to address`)।
> Dashboard থেকে project **Restore** করলেই আবার চলবে।

---

## Deployment (Railway / Render / VPS)

- `ALLOWED_HOSTS` ও `CSRF_TRUSTED_ORIGINS` আপনার ডোমেইন অনুযায়ী আপডেট করুন
  (`kornofuli/settings.py`)।
- `DEBUG=False` রাখুন।
- `DATABASE_URL` production database-তে দিন।
- Static/media ফাইল production-এ nginx/caddy দিয়ে serve করুন
  (`kornofuli/urls.py`-এর media/static serve ব্লকটি তখন মুছে ফেলুন)।

---

## Useful Commands

```bash
python manage.py check            # Config check
python manage.py showmigrations   # Migration status
python manage.py migrate          # Apply migrations
python manage.py makemigrations   # New migrations
python manage.py test             # Run tests
```

---

## License

Private project.
