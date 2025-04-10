from telegram import Update, request
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
import os
import configparser
import logging
import redis
logging.basicConfig(level=logging.INFO)
import telebot
bot = telebot.TeleBot(os.getenv('7945850444:AAEuld73YYsKSi3Cn_1LCGOyWNMyiqz1l68'))
bot.set_webhook(url="https://comp7940-lab-leiwuw2.fly.dev/webhook")

@app.route('/webhook', methods=['POST'])
def webhook():
    logging.info("Received update: %s", request.json)
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        bot.process_new_updates([update])
    return 'ok', 200


global redis1
def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']),use_context=True)
    dispatcher =updater.dispatcher
    global redis1
    redis1 = redis.Redis(host=(config['REDIS']['HOST']), 
                         password=(config['REDIS']['PASSWORD']), 
                         port=(config['REDIS']['REDISPORT']),
                         decode_responses=(config['REDIS']['DECODE_RESPONSE']),
                         username=(config['REDIS']['USER_NAME']))
    # You can set this logging module,
    # so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)
    # register a dispatcher to handle message:
    # here we register an echo dispatcher
    #echo_handler=MessageHandler(Filters.text & (~Filters.command), echo)
    #dispatcher.add_handler(echo_handler)

    # dispatcher for chatgpt
    global chatgpt
    chatgpt = HKBU_ChatGPT(config)
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), 
                        equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    
    dispatcher.add_handler(CommandHandler("hello", hello_command))

    # To start the bot:
    updater.start_polling()
    updater.idle()

def echo(update,context):
    reply_message = update.message.text.upper()
    logging.info("Update:"+ str(update))
    logging.info("context:"+ str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')

def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        
        update.message.reply_text('You have said ' + msg +  ' for ' + redis1.get(msg) + ' times.')
    
    except (IndexError, ValueError):
        update.message.reply_text('Usage:/add <keyword>')

def hello_command(update: Update, context: CallbackContext) -> None:
    """Send a greeting message when the command /hello is issued."""
    try:
        name = context.args[0]
        update.message.reply_text(f'Good day, {name}!')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hello <name>')

from ChatGPT_HKBU import HKBU_ChatGPT
def equiped_chatgpt(update, context): 
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

if __name__=='__main__':
    main()