import json
from pprint import pprint

from telegram import error
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Markup

from tgphEditor import tgph_editor
from type_s import Post
from buffer import buffer
from utils import get_method_args, upload_media_tgph, parse_buttons, check_markup_bts
from data_base import db
from view import view


class PrivateHandler(object):
    def __init__(self):
        
        self.map = {
            'add_channel':     self.add_channel,
            'add_post':        self.add_post,
            'add_addition':    self.add_addition,
            'select_type_btn': view.select_type_btn,
            'create_button':   self.create_button,
            'write_comment':   self.write_comment,
            'add_btn_url':     view.add_btn_url,
            'add_btn_name':    view.add_btn_name,
            'sort_buttons': self.sort_buttons
        }
    def sort_buttons(self, msg, ch_id):
        buttons, comments_on = db.get_buttons_channel(ch_id)
         

        bts = {}

        for line in buttons:
            for btn in line:
                bts[btn['id']] = btn


        pprint(bts)

        count_btn = len(bts)

        num_markup = check_markup_bts(msg.text, count_btn)
        print(num_markup)

        sort_btn = []
        for indx, line in enumerate(num_markup):
            sort_btn.append([])
            for num in line:
                print(indx, num)
                sort_btn[indx].append(bts[int(num) - 1])


        pprint(sort_btn)

        db.set_buttons_channel(ch_id, sort_btn, comments_on)
        view.config_btn(msg, ch_id = ch_id)







    def write_comment(self, msg, post_id):
        post = db.get_post(post_id)

        db.new_comment(
            text = msg.text,
            channel_id = post.channel_id,
            user_id = msg.chat.id,
            user_name = msg.chat.first_name,
            post_id = post_id
        )

        tgph_editor.update_comments(post_id, db)

        bts = parse_buttons(post.buttons)

        
        print('>>>> ', bts)
        print('COUNT: ', post.all_comments)
        

        post_bts = []
    
        for inx, line in enumerate(json.loads(post.buttons)):
            post_bts.append([])
            
            for btn in line:
                if btn['type'] == 'url':  
                    post_bts[inx].append(Button(btn['text'], url = btn['url']))

                elif btn['type'] == 'reaction':
                    btn_id = btn['id']
                    post_bts[inx].append(Button(btn['text'].format(count = 0),
                                    callback_data = f'upcount ?post_id={post_id}&btn_id={btn_id}'))

                elif btn['type'] == 'comments':
                    print('BUTTON >>> ', btn['text'])
                    post_bts[inx].append(Button(btn['text'].format(count = post.all_comments), url = 'telegra.ph/' + post.telegraph_path_top))







        
        print(post.channel_id,post.msg_id)
        print(post_bts)
        self.bot.edit_message_reply_markup(
            chat_id = int(post.channel_id),
            message_id = int(post.msg_id),
            reply_markup = Markup(post_bts)
        )
        view.comments_sended(msg)
    

    def create_button(self, msg, type_btn, url = None, ch_id = None):
        print('CHANNEL ID: ', ch_id)
        if ch_id:
            buttons, comments_on = db.get_buttons_channel(ch_id = ch_id)
        else:    
            buttons = buffer.get_arg_post(msg.chat.id, 'buttons')
        
        pprint(buttons)
        id = 0
        for line in buttons:
            print(line)
            print(type(line))
            id += len(line)



        buttons.append([
            {
            'id': id,
            'type': type_btn,
            'text': msg.text,
            'data': 'upcount btn ?btn_id=' + str(id),
            'users_liked': [],
            'url': url,
            'count':0
            }
        ])
        
        if not comments_on:
            comments_on = (type_btn == 'comments')

        print("SET COMMENTS ON: ", comments_on)
        if ch_id:
            db.set_buttons_channel(ch_id, buttons, comments_on)
            view.config_btn(msg, ch_id = ch_id)
        else:
            buffer.set_arg_post(msg.chat.id, 'buttons', buttons)

            view.bild_post(msg)

    def main(self, bot, msg):
        self.bot = bot
        msg = msg.message
        user_id = msg.chat.id

        user = db.check_user(user_id = user_id)
        method, action, args = get_method_args(user.mode_write)
        print('PRIVATE: ', method, action, args)
        
        
        if method == 'open':
            self.map[action](msg = msg, **args)

        else:
            view.main_menu(msg, edit_msg=False)


    def add_channel(self, msg):
        ch_name = msg.text
        

        if len(ch_name.split('t.me/')) > 1:
            ch_name = ch_name.split('t.me/')[1]

        if not ch_name[0] =='@':
            ch_name = '@' + ch_name

        print(ch_name)
        
        try:
            admins = self.bot.get_chat_administrators(ch_name)
    
            ch_id  = self.bot.get_chat(ch_name).id

            if ch_id in db.get_all_ch(msg.chat.id):
                result = 'ChannelExists'
            else:
                result = 'Added'

        except error.BadRequest as e:
            print('ERROR: ', e)
            e = str(e)

            if e == 'Chat not found':
                result = 'NotFound'
            elif e == 'Supergroup members are unavailable':
                result = 'NoAdmin'
            else:
                result = 'Added'

        if result == 'Added':
            db.add_channel(msg.chat.id, ch_id)
        else:
            ch_id = None

        view.add_ch_final(msg, edit_msg = True, result = result, ch_id = ch_id)

    def add_addition(self, msg):

        post = buffer.get_bildpost(msg.chat.id)

        if msg.text:
            post.text = msg.text
        elif msg.photo:
            post.photo = msg.photo[-1]
            post.photo_url = upload_media_tgph(self.bot, msg.photo[-1])
        else:
            print('TODO 223')

        buffer.add_bildpost(msg.chat.id, post)
        view.bild_post(msg)

    def add_post(self, msg):

        if msg.photo:
            photo = msg.photo[-1]
            photo_url = upload_media_tgph(self.bot, msg.photo[-1])
        elif msg.text:
            photo = None
            photo_url = None
        else:
            print('TODO 222')

        type_post = 'text' if msg.text else 'photo'    


        post = Post(msg.chat.id, text = msg.text, photo = photo,
                    photo_url = photo_url, type = type_post)
        buffer.add_bildpost(msg.chat.id, post)

        view.bild_post(msg)

    def command(self, bot, msg):
        msg = msg.message
        print(msg.text)
        msg_txt = msg.text.split()
        if len(msg_txt) == 2 and msg_txt[0] == '/start':
            code = msg_txt[1]
            print(msg_txt, code)
            if code[0] == '0': # for new comments
                print(111111111111)
                view.write_comment(msg, post_id = code[1:])
            elif code[0] == '1': # for open comment
                print(222222222222)
                view.comment(msg, comment_id = code[1:])
            
        elif msg.text == '/start':
           

            if db.get_all_ch(msg.chat.id):
                view.main_menu(msg, edit_msg=False)
            else:
                view.welkom(msg, edit_msg=False)



private_handler = PrivateHandler()