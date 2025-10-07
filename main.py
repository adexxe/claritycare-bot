import os
from flask import Flask, request, abort
import telebot
import openai

TELEGRAM_TOKEN = os.environ.get("7864931534:AAFVsxUEg1NrV5oLKwnC5YvOUFRFj2_N6ps")
OPENAI_API_KEY = os.environ.get("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")  # optional, leave blank if you don't want AI replies yet
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # e.g. https://your-service.onrender.com/webhook

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN environment variable is required")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# --- Handlers ---
@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    intro = (
        "Hey, I’m Claritycare — your Naija Gen-Z, mature-but-friendly AI buddy. "
        "How you dey feel today?"
    )
    bot.send_message(message.chat.id, intro)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = (message.text or "").strip()
    lowered = text.lower()

    # quick keyword routing for snappy replies
    if any(w in lowered for w in ["sad","down","depressed","unhappy","stressed","anxious"]):
        reply = "That sounds rough. Tell me about what’s been weighing you."
    elif any(w in lowered for w in ["happy","good","great","blessed","ok","fine"]):
        reply = "Nice one. What made today go well?"
    else:
        # if OPENAI_API_KEY exists, ask OpenAI for a friendly empathetic reply
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY
            try:
                system = (
                    "You are Claritycare, a warm, emotionally intelligent Naija Gen-Z friend. "
                    "Be empathetic, concise, sprinkle light slang only when natural, and never judge."
                )
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role":"system","content":system},
                        {"role":"user","content":text}
                    ],
                    temperature=0.8,
                    max_tokens=220
                )
                reply = resp['choices'][0]['message']['content'].strip()
            except Exception:
                reply = "I’m here and listening. Tell me more."
        else:
            reply = "I hear you. Tell me more — I’m listening."

    bot.send_message(message.chat.id, reply)

# --- Webhook endpoint for Telegram to POST updates to ---
@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "", 200
    else:
        abort(403)

@app.route("/", methods=["GET"])
def index():
    return "Claritycare is alive"

# --- start up ---
if __name__ == "__main__":
    if WEBHOOK_URL:
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
