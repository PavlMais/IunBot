import logging


import telegram
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackQueryHandler


import config
from private import private_handler
from callback import callback
from post_editor import post_editor
from post_handler import post_handler


logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s')

updater = Updater(config.TOKEN)

dispatcher = updater.dispatcher




dispatcher.add_handler(
    MessageHandler(Filters.text | Filters.photo , private_handler.main, channel_post_updates = False)
)
dispatcher.add_handler(CommandHandler('start', private_handler.command))
dispatcher.add_handler(CallbackQueryHandler(callback.main))
dispatcher.add_handler(
    MessageHandler(Filters.text | Filters.photo | Filters.audio, post_handler.post_handl, message_updates = False)
)

updater.start_polling()
updater.idle()



