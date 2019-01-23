from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackQueryHandler
import logging
try:
    import local_config as config
except ImportError:
    import config
from private import PrivateHandler
from view import View
from data_base import DB
from callback import CallbackHandler
from post_editor import PostEditor

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(config.TOKEN)

dispatcher = updater.dispatcher

db = DB()
view = View(updater.bot, db )
PH = PrivateHandler(view, db, updater.bot)
CBH = CallbackHandler(view , db)
post_editor = PostEditor(db)

dispatcher.add_handler(MessageHandler(Filters.text, PH.main, channel_post_updates = False))
dispatcher.add_handler(CommandHandler('start', PH.command))
dispatcher.add_handler(CallbackQueryHandler(CBH.main))
dispatcher.add_handler(MessageHandler(Filters.text, post_editor.new_post, message_updates = False))

updater.start_polling()
updater.idle()

