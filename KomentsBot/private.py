from telegram import error
from telegram import InlineKeyboardButton as Button


from type_s import Post
from buffer import buffer
from utils import get_method_args, upload_media_tgph


class PrivateHandler(object):
    def __init__(self, view, db, bot, post_editor):
        self.view = view
        self.db   = db
        self.bot  = bot
        self.post_editor = post_editor
        self.map = {
            'add_channel': self.add_channel,
            'add_post': self.add_post,
            'add_addition':self.add_addition,
            'select_type_btn':self.view.select_type_btn,
            'create_button':self.create_button,
            'add_btn_url': self.view.add_btn_url,
            'add_btn_name': self.view.add_btn_name
        }

    def create_button(self, msg, type_btn, url = None):
        post = buffer.get_bildpost(msg.chat.id)
        if type_btn == 'url':
            post.buttons.append([Button(msg.text, url = url)])
        elif type_btn == 'reaction':
            post.buttons.append([Button(msg.text.format(count = 0), callback_data='pres btn')])
        elif type_btn == 'komments':
            post.buttons.append([Button(msg.text.format(count = 0), url = 'http://komments.com')])


        buffer.add_bildpost(msg.chat.id, post)
        self.view.bild_post(msg)

    def main(self, bot, msg):
        msg = msg.message
        user_id = msg.chat.id

        user = self.db.check_user(user_id = user_id)
        method, action, args = get_method_args(user.mode_write)
        print('PRIVATE: ', method, action, args)
        
        
        if method == 'open':
            self.map[action](msg = msg, **args)

        else:
            self.view.main_menu(msg, edit_msg=False)


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

            if ch_id in self.db.get_all_ch(msg.chat.id):
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
            self.db.add_channel(msg.chat.id, ch_id)
        else:
            ch_id = None

        self.view.add_ch_final(msg, edit_msg = True, result = result, ch_id = ch_id)

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
        self.view.bild_post(msg)

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


        post = Post(msg.chat.id, text = msg.text, photo = photo, photo_url = photo_url, type = type_post)
        buffer.add_bildpost(msg.chat.id, post)

        self.view.bild_post(msg)

    def command(self, bot, msg):
        msg = msg.message
        print(msg.text)
        msg_txt = msg.text.split()
        if len(msg_txt) == 2 and msg_txt[0] == '/start':
            code = msg_txt[1]
            print(msg_txt, code)
            if code[0] == '0': # for new comments
                print(111111111111)
                self.view.write_comment(msg, post_id = code[1:])
            elif code[0] == '1': # for open comment
                print(222222222222)
                self.view.comment(msg, comment_id = code[1:])
            
        elif msg.text == '/start':
           

            if self.db.get_all_ch(msg.chat.id):
                self.view.main_menu(msg, edit_msg=False)
            else:
                self.view.welkom(msg, edit_msg=False)



