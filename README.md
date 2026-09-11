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

## Project Structure
binance-parameters-monitor/
│
├── README.md               # Project documentation
├── binance_monitor.py      # Main script


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


