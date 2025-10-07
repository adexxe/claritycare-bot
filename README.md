Claritycare — Naija Gen-Z empathetic Telegram bot

Required environment variables (set on Render):
- TELEGRAM_TOKEN   (your BotFather token)
- OPENAI_API_KEY   (optional, for AI replies)
- WEBHOOK_URL      (set after deployment, format: https://<your-service>.onrender.com/webhook)

Deploy notes:
- Build command: pip install -r requirements.txt
- Start command: gunicorn main:app
- After deploy, set TELEGRAM_TOKEN and OPENAI_API_KEY in Render dashboard, then set WEBHOOK_URL to your Render service URL + /webhook
- Or set webhook manually with Telegram API: https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=<WEBHOOK_URL>
