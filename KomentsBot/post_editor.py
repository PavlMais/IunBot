from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Markup
from telegraph import Telegraph


from utils import add_entities
from config import TGPH_TOKEN


class PostEditor(object):

    def __init__(self, db):
        self.db = db
        self.tgph = Telegraph(TGPH_TOKEN)
        
        
    def new_post(self,bot, msg):
        post = msg.channel_post

        page_top = self.tgph.create_page(title = 'Komments | 0', html_content = '-')
        page_new = self.tgph.create_page(title = 'Komments | 0', html_content = '-')

        if post.photo:
            type_msg = 'photo' 
            text_msg = post.caption
        else:
            type_msg = 'text'
            text_msg = post.text


        post_id = self.db.new_post(
            chennel_id = post.chat.id,
            msg_id = post.message_id,
            telegraph_path_new = page_new['path'],
            telegraph_path_top = page_top['path']
        )
    
        standart_bts = [[Button('Написать коментарий', url='t.me/KomentsBot?start=0' + str(post_id)),]]
        

        text_post = add_entities(text_msg, post.entities)

        page_url = page_top['url']
        new_text = f'{text_post}\n<a href="">&#65524;</a><a href="{page_url}">Комментарии  0</a>\n'

        self.edit_msg(bot, post.chat.id, post.message_id, new_text, standart_bts)


    def edit_msg(self, bot, chat_id, msg_id, text, bts):
        try:
            bot.edit_message_caption(
                chat_id = chat_id,
                message_id = msg_id,
                caption = text,
                reply_markup = Markup(bts),
                parse_mode = 'html'

            )
        except Exception as e:
            print('Error edit msg in channel: ', e)
            bot.edit_message_text(
                chat_id = chat_id,
                message_id = msg_id,
                text = text,
                reply_markup = Markup(bts),
                parse_mode = 'html'
            )

    def new_comment(self, bot, user_id, post_id, text, user_name):
        post = self.db.get_post(post_id)
        self.db.new_comment(user_id, post, text, user_name)
        self.update_post(bot, post.id)
        bot.send_message(user_id, 'You comments sended!\nThank you!')



    def update_post(self, bot, post_id = None, comment_id = None):
        post = self.db.get_post(post_id = post_id, comment_id = comment_id)
        self.db.get_comments(post_id = post_id)
        msg = bot.forward_message(chat_id = '@gpalik', from_chat_id = post.channel_id, message_id = post.msg_id)

        

        text_post = msg.text.split('\ufff4')[0]
        text_post = add_entities(text_post, msg.entities)
        
        text = f'<a href="Bot">&#65524;</a><b>Коментарии  {post.all_comments}</b>'


        #============= EDIT PAGE IN TELEGRAPH =================
        comments_new = self.db.get_comments(post_id = post.id, sort_comnts = 'new', limit_comnts = 25) 
        comments_top = self.db.get_comments(post_id = post.id, sort_comnts = 'top', limit_comnts = 25) 




        base = '<h4>{}</h4>{}<br><a href="http://t.me/KomentsBot?start=1{}">Like {} {}</a><br>'


        write_com = '<br><a href="http://t.me/KomentsBot?start=0' + str(post.id) + '> Add comments</a> <br>'

        body_new = f'Sort <b>New</b> <a href="https://telegra.ph/{post.telegraph_path_top}">Top</a><br>' + write_com
        body_top = f'Sort <a href="https://telegra.ph/{post.telegraph_path_new}">New</a> <b>Top</b><br>' + write_com


        for com in comments_new:
            body_new += base.format(com.user_name, com.text, com.id, com.liked_count, com.date_add)
        

        for com in comments_top:
            body_top += base.format(com.user_name, com.text, com.id, com.liked_count, com.date_add)


        title = 'Komments | '+ str(post.all_comments)
        
        self.tgph.edit_page(
            path = post.telegraph_path_new,
            title = title,
            html_content = body_new
        )
        self.tgph.edit_page(
            path = post.telegraph_path_top,
            title = title,
            html_content = body_top
        )
        #=======================================================


        print(post.telegraph_path_top, post.telegraph_path_new)

        for comm in comments_new[:-3]:

            text += f'\n <b>{comm.user_name}</b>\n  <i>{comm.text}</i>\n ❤️ {comm.liked_count}  |  {comm.date_add}'

        
        standart_bts = [[Button('Открить коментарии', url="https://telegra.ph/" + post.telegraph_path_top)]]

        self.edit_msg(bot, post.channel_id, post.msg_id, text_post + text , standart_bts)
        
