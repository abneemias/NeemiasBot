#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import atexit

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def photo_handler(update: Update, context: CallbackContext) -> None:
    newFile = update.message.effective_attachment[-1].get_file()
    newFile.download("Fotos/"+str(update.update_id)+'.jpg')
    
def video_handler(update: Update, context: CallbackContext) -> None:
    newFile = update.message.effective_attachment.get_file()
    newFile.download("Videos/"+str(update.update_id)+'.mp4')

   
def echo(update: Update, context: CallbackContext) -> None:  
    if(update.message.text == "senhasenha"):
        if(update.update_id in permitidos):
            update.message.reply_text("J? autorizado")
        else:
            permitidos.append(str(update.effective_user.id))
            update.message.reply_text("Senha Correta")
    else:
        if(str(update.effective_user.id) in permitidos):
            update.message.reply_text("Voce ? chavoso")
        else:
            update.message.reply_text("Sai daqui, esquisito")
        

def savequit(nomes):
    arquivo = open("permitidos.txt","w");
    for i in nomes:
        arquivo.write(str(i)+"\n")

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    ref_arquivo = open("token.txt","r")
    updater = Updater(ref_arquivo.readlines()[0])
    ref_arquivo.close()
    leitura_arquivo = open("permitidos.txt","r");
    global permitidos
    permitidos = leitura_arquivo.read().splitlines()
    leitura_arquivo.close()
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
    dispatcher.add_handler(MessageHandler(Filters.video, video_handler))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    atexit.register(savequit,permitidos)


if __name__ == '__main__':
    main()