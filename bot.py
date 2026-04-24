import telebot
import time
import os
from flask import Flask
from threading import Thread

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask('')

BAD_WORDS =[كسمك', 'يبن البوه', 'ي شرموطه', 'ي ابن المتناكه', 'ي عرص', 'هنيكك', 'ي ابن الزنيه', 'ي ابن الفجره' , ', ']
warnings = {}

@app.route('/')
def home():
    return "بوت سايكو المصري شغال 24/7 🌚"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for user in message.new_chat_members:
        bot.send_message(message.chat.id, f"نورت الجروب يا {user.first_name} 🌚\nممنوع الشتيمة والروابط يا وحش")

@bot.message_handler(content_types=['text'])
def handle_messages(message):
    if message.from_user.is_bot: return
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['administrator', 'creator']: return
    
    text = message.text.lower()
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if any(x in text for x in ['http', 't.me/', 'bit.ly', 'www.', 'https://']):
        try:
            bot.delete_message(chat_id, message.message_id)
            warn_user(message, "ارسال روابط")
        except: pass
        return

    for word in BAD_WORDS:
        if word in text:
            try:
                bot.delete_message(chat_id, message.message_id)
                warn_user(message, f"كلمة محظورة")
            except: pass
