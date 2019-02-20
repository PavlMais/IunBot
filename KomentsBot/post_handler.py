import json

import telegram
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Markup

from tgphEditor import tgph_editor
from data_base import db

class PostHandler(object):
    def __init__(self):
        pass

    def post_handl(self, bot, msg):
        msg = msg.channel_post

        channel = db.get_ch_setting(msg.chat.id)

        # if channel.status == 'off':
        #     print('Channel status OFF')
        #     return
        print(channel.comments_on)
        if channel.comments_on:
            page_top, page_new = tgph_editor.new_comments()
        else:
            page_top = page_new = None

        print('PAGE TOP: ', page_top)

        post_id = db.new_post(
            channel_id = msg.chat.id,
            comments_on = channel.comments_on,
            buttons = channel.default_btn_markup,
            telegraph_path_new = page_new,
            telegraph_path_top = page_top
        )
        db.set_msg_id_post(post_id, msg.message_id)

        bts = []
    
        for inx, line in enumerate(json.loads(channel.default_btn_markup)):
            bts.append([])
            
            for btn in line:
                if btn['type'] == 'url':  
                    bts[inx].append(Button(btn['text'], url = btn['url']))

                elif btn['type'] == 'reaction':
                    bts[inx].append(Button(btn['text'].format(count = 0),
                                    callback_data = btn['data']))

                elif btn['type'] == 'comments':
            
                    bts[inx].append(Button(btn['text'].format(count = 0), url = f't.me/KomentsBot?start=0{post_id}'))

       

        
        bot.edit_message_text(msg.text, chat_id = msg.chat.id, message_id = msg.message_id,
                              parse_mode = 'html', reply_markup = Markup(bts))

            
        





     



post_handler = PostHandler()