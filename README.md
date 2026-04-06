# 🛒 Telegram Shop Order Bot — Run Guide

## ✅ Requirements
- Python 3.10 or higher
- A Telegram bot token (from @BotFather)
- Your Telegram numeric user ID (from @userinfobot)

---

## 🔧 Step 1 — Get a Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow the prompts (set a name and username)
4. Copy the token you receive — looks like:
   ```
   7123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 🔧 Step 2 — Get Your Admin ID

1. Open Telegram and search for **@userinfobot**
2. Send `/start`
3. Copy your numeric **Id** — looks like: `123456789`

---

## 🔧 Step 3 — Edit bot.py

Open `bot.py` and fill in these three lines at the top:

```python
BOT_TOKEN      = "YOUR_BOT_TOKEN_HERE"   # ← paste token here
ADMIN_ID       = 123456789               # ← paste your numeric ID here
ADMIN_USERNAME = "@yourusername"         # ← paste your @username here
```

---

## 🔧 Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 Step 5 — Run the Bot

```bash
python bot.py
```

You should see:
```
Bot ishga tushmoqda... 🚀
```

---

## 🧪 Step 6 — Test It

1. Open Telegram and find your bot by its username
2. Send `/start`
3. Tap **🛍 Mahsulotlar** → select a product → tap **✅ Buyurtma berish**
4. Follow the order flow (name → phone → address)
5. Check your Telegram — you should receive the full order details

---

## 📦 How to Customize

| What to change         | Where                          |
|------------------------|--------------------------------|
| Products               | `PRODUCTS` dict in `bot.py`    |
| Welcome message        | `cmd_start` handler            |
| Contact info           | `ADMIN_USERNAME` constant      |
| Add more menu buttons  | `main_menu_keyboard()` function|

---

## 🚀 Deploy to a Server (optional)

To keep the bot running 24/7, deploy it to a VPS and use `systemd` or `screen`:

```bash
# Using screen
screen -S shopbot
python bot.py
# Press Ctrl+A then D to detach
```

Or use a free hosting service like **Railway.app** or **Render.com**.

---

## 📁 File Structure

```
├── bot.py            ← Main bot code (everything in one file)
├── requirements.txt  ← Python dependencies
└── README.md         ← This guide
```
