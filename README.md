# Volunteer Duty Tracking Bot

## Overview

The Volunteer Duty Tracking Bot is a Python-based automation system developed to track and record volunteer shift hours during the School 21 selection intensives.

The system replaces manual attendance tracking with a reliable and structured workflow, reducing human error while improving operational visibility for organizers.

Designed with scalability and maintainability in mind, the bot provides a solid foundation for expanding volunteer management capabilities in high-load environments.

The bot integrates with Google APIs using secure service account authentication.

---

## Key Features

- Automated tracking of volunteer duty hours  
- Centralized shift logging  
- Modular architecture for easier maintenance  
- Lightweight deployment  
- Database-backed persistence  
- Designed for future scalability  

---

## Architecture

The project follows a modular architecture that separates business logic, database operations, and request handlers.

This approach provides:

- improved readability  
- easier testing  
- simplified debugging  
- better long-term scalability  

**Core architectural principles:**

- Separation of concerns  
- Minimal coupling  
- Extensible module structure  

---

## Tech Stack

**Language:** Python  

**Libraries / Frameworks:**  
- aiogram (Telegram bot framework)  
- SQLAlchemy / SQLite (depending on your implementation)

**Infrastructure:**  
- Docker  
- Docker Compose  

---

## Installation

### Clone the repository

`git clone https://github.com/c001guard/volunteer_bot.git
cd volunteer_bot`

### Running with Docker (Recommended)

`docker compose up --build`
This is the preferred way to run the bot in both development and production environments.

### Local Run (Optional)
If you prefer running the bot without Docker, install the required dependencies globally:
`pip install -r requirements.txt`
Then start the bot:
`python main.py`

## Configuration

Create a .env file in the project root and specify the required environment variables:
`BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=your_database_url`
Never commit the .env file to version control.

## Google API Credentials Setup

The bot uses Google APIs to access external services.  
Authentication is performed via a service account using a `creds.json` file.

### Steps to obtain credentials:

1. Go to the Google Cloud Console.
2. Create a new project (or use an existing one).
3. Enable the required Google APIs.
4. Navigate to **IAM & Admin → Service Accounts**.
5. Create a service account.
6. Generate a JSON key and download it.
7. Rename the file to:
   `creds.json`
8. Place it in the project root directory.
⚠️ **Important:**  
Never commit `creds.json` to the repository.

Add it to `.gitignore`:
`creds.json`

If the file is exposed, immediately revoke the key in Google Cloud and generate a new one.

## Use Case

During selection intensives, managing volunteer attendance manually becomes inefficient and error-prone.

This bot automates the process by:

recording shift participation

simplifying coordination

providing a reliable source of truth for organizers

## Future Improvements

Admin dashboard for shift monitoring

Analytics for volunteer participation

Role-based access control

Integration with scheduling platforms

Cloud deployment support

## Contributing

Contributions are welcome.
Please open an issue to discuss proposed changes before submitting a pull request.
