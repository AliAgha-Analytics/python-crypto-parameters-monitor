# Binance Parameters Monitor

A Python script that monitors Binance Futures contract parameters for a watchlist of coins and sends alerts to Telegram every 30 minutes.  
It also saves a CSV snapshot of parameters locally, updating on each run so you can track changes over time.

--

## Features
- Monitors contract specifications for a chosen watchlist.
- Compares the latest snapshot with the previous one to detect changes.
- Sends alerts to Telegram where scheduler runs automatically every 30 minutes.
- Immediate run at startup so you see results right away.
- Saves a `binance_snapshot.csv` file that updates every run, providing a historical record of parameters.

--

## Install Dependencies
pip install requests pandas schedule

--

## Configure Telegram
If you want Telegram alerts:
Create a bot via BotFather in Telegram → get your bot token.

Get your chat ID by sending a message to the bot, then visiting: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates

Look for "chat":{"id":...}

Replace placeholders in the script:
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

## Notes on Real-World Usage
- **API Keys**: In production, store sensitive values (Telegram tokens, Binance API keys) in environment variables or a `.env` file. Never commit them to GitHub.
- **Regional Differences**: Public endpoints return global defaults. For real trading, authenticated API calls reflect your account’s actual limits, which may vary by region, regulation or VIP tier etc..
- **CSV Snapshots**: The script overwrites `binance_snapshot.csv` each run. If you want historical tracking, archive snapshots manually or extend the script to timestamp files.
- **Error Handling**: You can add retry logic and exception handling for API downtime or rate limits.
- **Deployment**: For continuous monitoring, deploy on a cloud service (PythonAnywhere, Heroku, VPS) instead of running locally.
- **Extensibility**: The design can be extended to multiple exchanges for cross-exchange monitoring.


