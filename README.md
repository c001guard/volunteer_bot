# 🤖 Volunteer Duty Tracking Bot
 
Telegram bot for tracking volunteer shift hours at the School 21 campus in Tashkent.
 
Built to solve a real coordination problem: with 20+ active volunteers, manually tracking attendance during selection intensives was unreliable and time-consuming.
 
**Current status:** v1 was deployed and tested in production with real volunteers. After identifying a critical UX issue (see [Lessons Learned](#-lessons-learned-v1--v2)), the bot is being redesigned for v2.
 
---
 
## 🛠 Tech Stack
 
| Layer | Technology |
|-------|-----------|
| **Language** | Python 3 |
| **Bot Framework** | aiogram (async Telegram bot framework) |
| **Database** | PostgreSQL on [Neon](https://neon.tech/) (serverless cloud DB) |
| **ORM** | SQLAlchemy |
| **Spreadsheets** | Google Sheets API via `gspread` (real-time sync) |
| **Deployment** | Docker + Docker Compose |
| **Hosting** | Linux server (School 21 campus) |
 
---
 
## 📋 Key Features
 
- **Automated shift tracking** — volunteers check in/out through the bot, replacing manual attendance logs
- **Database-backed persistence** — all shift records stored in PostgreSQL (Neon cloud)
- **Google Sheets sync** — shift data automatically pushed to a shared spreadsheet for the team lead and campus staff
- **Volunteer identification** — each volunteer linked to their Telegram account
- **Modular architecture** — separated business logic, database operations, and handlers
- **Containerized deployment** — runs via Docker Compose
---
 
## 🏗 Architecture
 
The project follows a modular architecture with separation of concerns:
 
```
volunteer_bot/
├── bot/                    # Core bot logic
│   ├── handlers/           # Telegram command and callback handlers
│   ├── db/                 # Database models and queries (SQLAlchemy)
│   ├── services/           # Google Sheets sync, business logic
│   └── config.py           # Environment variables and settings
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Service orchestration
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```
 
**Core principles:**
- Separation of concerns between handlers, DB layer, and external services
- Minimal coupling between modules
- Extensible structure for adding new features (reminders, metrics, dashboards)
---
 
## 🚀 Installation
 
### Prerequisites
 
- Python 3.10+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- PostgreSQL database (or free [Neon](https://neon.tech/) account)
- Google Service Account credentials (for Sheets API)
### Running with Docker (recommended)
 
```bash
git clone https://github.com/c001guard/volunteer_bot.git
cd volunteer_bot
```
 
Create a `.env` file in the project root:
 
```env
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql://user:pass@host/dbname
```
 
Run:
 
```bash
docker compose up --build
```
 
### Local Run (without Docker)
 
```bash
pip install -r requirements.txt
python main.py
```
 
---
 
## 🔐 Google API Credentials Setup
 
The bot uses Google Sheets API for real-time shift data sync. Authentication is via a service account.
 
**Steps:**
 
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or use an existing one)
3. Enable **Google Sheets API**
4. Go to **IAM & Admin → Service Accounts**
5. Create a service account and generate a JSON key
6. Rename the file to `creds.json`
7. Place it in the project root
8. Share your target Google Sheet with the service account email
⚠️ **Never commit `creds.json` to the repository.** It is already in `.gitignore`.
 
If the file is exposed, immediately revoke the key in Google Cloud Console and generate a new one.
 
---
 
## 💡 Use Case
 
During School 21 selection intensives, managing volunteer attendance manually becomes inefficient and error-prone.
 
This bot automates the process by:
- Recording shift check-in/check-out times
- Syncing data to Google Sheets for real-time visibility
- Providing a single source of truth for organizers
- Reducing coordination overhead for the team lead
---
 
## 📖 Lessons Learned: v1 → v2
 
### v1 — What Worked ✅
 
The first version was fully functional and deployed on a campus server:
 
- Bot correctly handled shift check-in/check-out commands
- Data was reliably stored in Neon PostgreSQL
- Google Sheets integration worked — the team lead could monitor shifts in real time
- Ran stably on Linux with Docker
### v1 — What Failed ❌
 
After several weeks in production, a critical UX problem emerged: **volunteers consistently forgot to check in**.
 
The bot required a proactive action (sending a command) at the start of each shift — but in practice, people were busy, distracted, or simply forgot.
 
The check-in completion rate dropped significantly, and the bot was paused.
 
### Key Takeaway
 
> A technically correct solution fails if it doesn't fit the user's natural workflow.
 
The check-in action needed to be **pushed to the user** (reminders, notifications), not **pulled from the user** (manual commands). This is a well-known UX principle — but learning it firsthand on a real product with real users was invaluable.
 
---
 
## 🔧 v2 Roadmap
 
Based on the v1 post-mortem, v2 will focus on **reducing friction** for volunteers:
 
| Feature | Purpose | Status |
|---------|---------|--------|
| **Auto-reminders** | Bot sends a message 1h and 15min before each shift | 📋 Planned |
| **One-click check-in** | Inline button in the reminder — tap once to confirm | 📋 Planned |
| **Escalation to team lead** | Notification if a volunteer misses check-in by 15min | 📋 Planned |
| **Weekly shift report** | Automated summary: attendance rate, missed shifts | 📋 Planned |
| **Prometheus metrics** | Expose check-in rate and active user count | 📋 Planned |
| **CI/CD pipeline** | Automated deploy via GitHub Actions | 📋 Planned |
 
v2 will be deployed as part of the [shek-dev](https://github.com/c001guard/shek-dev) infrastructure project — containerized with Docker, monitored with Prometheus + Grafana, deployed via CI/CD.
 
---
 
## 🤝 Contributing
 
Contributions are welcome. Please open an issue to discuss proposed changes before submitting a pull request.
 
---
 
## 👤 About the Author
 
**Valerii Shek** — volunteer team lead at School 21 Tashkent campus (20+ volunteers).
 
I built this bot to solve my own coordination problem. The v1 experience taught me that shipping code is only half the job — understanding how users actually interact with your tool is the other half.
 
- 🔗 Portfolio: [shek-dev](https://github.com/c001guard/shek-dev)
- 💬 Telegram: [@c001ermsc](https://t.me/c001ermsc)
- 📧 Email: val_shek@mail.ru
- 🐙 GitHub: [@c001guard](https://github.com/c001guard)
---
 
## 📄 License
 
MIT
 
