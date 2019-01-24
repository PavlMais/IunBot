from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Markup

class PostEditor(object):

    def __init__(self, db):
        self.db = db
        
    def new_post(self,bot, msg):
        post = msg.channel_post
        print(post)

        post_id = self.db.new_post(chennel_id = post.chat.id, msg_id = post.message_id)
        

        standart_bts = [[Button('Написать коментарий',
         url='t.me/KomentsBot?start=' + str(post_id)),]]
         
        new_text = f"""{post.text}
*Коментарии 0*
  _Ти можеш первий добавить коментарий
  (без регестрации)_
        """

        r = bot.edit_message_text(
            text = new_text,
            message_id = post.message_id,
            chat_id = post.chat.id,
            reply_markup = Markup(standart_bts),
            parse_mode = 'markdown'
        )

        print(r)

    def new_comment(self, bot, user_id, post_id, text):
        self.db.new_comment(user_id, post_id, text)
        post = self.db.get_post(post_id)
        

        standart_bts = [[Button('Написать коментарий',
         url='t.me/KomentsBot?start=' + str(post.id)),]]

        bot.edit_message_text(
            text = '',         #       <<     TODO
            message_id = post.msg_id,
            chat_id = post.channel_id,
            reply_markup = Markup(standart_bts),
            parse_mode = 'markdown'
        )
        
    def update_post(post_id):
        pass
