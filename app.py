import os
import threading
from flask import Flask
import telebot
from telebot import types

# Flask-приложение для здоровья сервиса
app = Flask(__name__)

# Токен из переменной окружения Render
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Твой код бота (кнопки, обработчики) — вставь сюда
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🎁 Промокоды', '⏰ Ивенты', '📖 Гайды', '❓ Помощь')
    bot.send_message(message.chat.id, "Привет! Выбери раздел:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text
    if text == '🎁 Промокоды':
        bot.send_message(message.chat.id, "Актуальные коды (пример):\n`BR2026` — 50k$", parse_mode='Markdown')
    elif text == '⏰ Ивенты':
        bot.send_message(message.chat.id, "Ближайшие ивенты:\n• 20:00 — Гонка")
    elif text == '📖 Гайды':
        bot.send_message(message.chat.id, "Гайд для новичка: работай курьером.")
    elif text == '❓ Помощь':
        bot.send_message(message.chat.id, "Бот работает!")
    else:
        bot.send_message(message.chat.id, "Нажми на кнопки ниже.")

# Запуск бота в фоновом потоке, чтобы Flask мог слушать порт
def run_bot():
    bot.infinity_polling()

# Роуты для Render (проверка, что сервис жив)
@app.route('/')
def index():
    return "Bot is running"

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    # Запускаем бота в отдельном потоке
    threading.Thread(target=run_bot, daemon=True).start()
    # Flask слушает порт, который даёт Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)