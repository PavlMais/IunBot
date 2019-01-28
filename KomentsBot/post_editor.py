from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Markup
from utils import add_entities
class PostEditor(object):

    def __init__(self, db):
        self.db = db
        
    def new_post(self,bot, msg):
        post = msg.channel_post

        post_id = self.db.new_post(chennel_id = post.chat.id, msg_id = post.message_id)
    
        standart_bts = [[Button('Написать коментарий', url='t.me/KomentsBot?start=' + str(post_id)),]]
        

        text_post = add_entities(post.text, post.entities)

        new_text = f'{text_post}\n<a href="Bot">&#65524;</a><b>Komments  0</b>\n'

        r = bot.edit_message_text(
            text = new_text,
            message_id = post.message_id,
            chat_id = post.chat.id,
            reply_markup = Markup(standart_bts),
            parse_mode = 'html'
        )

        print(r)

    def new_comment(self, bot, user_id, post_id, text):
        post = self.db.get_post(post_id)
        self.db.new_comment(user_id, post, text)
        self.update_post(bot, post.id)
        
        bot.send_message(user_id, 'You comments sended!\nThank you!')





    def update_post(self, bot, post_id = None, comment_id = None):
        post = self.db.get_post(post_id = post_id, comment_id = comment_id)

        msg = bot.forward_message(chat_id = '@gpalik', from_chat_id = post.channel_id, message_id = post.msg_id)

        text_post = msg.text.split('\ufff4')[0]
        text_post = add_entities(text_post, msg.entities)
        

        text = f'<a href="Bot">&#65524;</a><b>Коментарии  {post.all_comments}</b>'


        for comm in post.comments:
            time = comm.date_add
            name = bot.get_chat(comm.user_creator).first_name
            text += f'\n <b>{name}</b>️   ❤️ {comm.liked_count}   🕑 {time}\n      <i>{comm.text}</i>'


        standart_bts = [[Button('Открить коментарии', url='t.me/KomentsBot?start=' + str(post.id)),]]

        bot.edit_message_text(
            text = text_post + text,         
            message_id = post.msg_id,
            chat_id = post.channel_id,
            reply_markup = Markup(standart_bts),
            parse_mode = 'html'
        )
        
