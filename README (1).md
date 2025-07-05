# AI Product Finder Telegram Bot 🚀

This bot lets you search and find the best laptops/products according to your requirements directly inside Telegram.

## ✨ Features
- Enter requirements and budget, e.g., "laptop Ryzen 7 16GB under 55000"
- Searches Amazon and Flipkart
- Filters and shows top deals with prices and links
- Works on your phone inside Telegram

## 🚀 Deployment Guide

### 1️⃣ Create a Bot
- Go to Telegram, search `@BotFather`, and create a new bot.
- Copy your `BOT_TOKEN`.

### 2️⃣ Deploy on Render
- Create a free [Render](https://render.com) account.
- Create a **Web Service**, connect your GitHub repository (`Ai-finder`).
- Add environment variable:
  - `BOT_TOKEN = your_bot_token`
- Build command:
  ```
  pip install -r requirements.txt
  ```
- Run command:
  ```
  python ai_product_finder_bot.py
  ```
- Deploy and your bot will run 24x7.

### 3️⃣ Start Using
- Open Telegram and send `/start` to your bot.
- Send your requirements and receive filtered product deals instantly.