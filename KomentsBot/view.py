from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Markup
import time

class View(object):
    def __init__(self, bot, db):
        self.bot = bot
        self.db  = db
        

    def send_msg(func):
        def wraper(self, msg, edit_msg = True, *args, **kwargs):
            print(args)
            print(kwargs)

            user = self.db.check_user(msg.chat.id)
            self.user_id = msg.chat.id
            text, buttons = func(self, *args, **kwargs)

            if text is False:
                return
            if buttons is None:
                bts = None
            else:
                bts = Markup(buttons)

            if edit_msg:
                try:
                    self.bot.edit_message_text(text, chat_id = msg.chat.id, message_id = msg.message_id, reply_markup = bts)
                except Exception as e:
                    print('Error send message: ', e)
                    self.bot.send_message(msg.chat.id, text, reply_markup = bts)
            else:
                self.bot.send_message(msg.chat.id, text, reply_markup = bts)
        return wraper

    @send_msg
    def comments(self, post_id):
        post = self.db.get_post(post_id)
        if post.channel_id in self.db.get_all_ch(self.user_id):
            is_admin = True
        else:
            is_admin = False


        for com in post.comments:
            time.sleep(0.5)
            name_user = self.bot.get_chat(com.user_creator).first_name
            bts = [[Button('❤️' + str(com.liked_count) ,callback_data="comment like " + str(com.id))]]

            if is_admin: bts[0].append(Button('🗑', callback_data='open confirm_del ' + str(com.id)))

            text = f'**{name_user}:**❤️ {com.liked_count} **|** 🕑 {com.date_add}\n__{com.text}__'
            print(bts)
            self.bot.send_message(self.user_id, text, reply_markup = Markup(bts) )

        self.bot.send_message(self.user_id, 'Write your comments: ')
        self.db.set_user_param(self.user_id, 'mode_write', 'write_comment '+ str(post.id))
            

        return False, None

    @swnd_msg
    def confirm_del(self, arg_id):
        comment = self.db.get_comment(arg_id)

        bts = [[Button('Yes', callback_data = "commit delete " + arg_id),
                Button('No', callback_data  = "delete_this_msg" )]]#TODO: <<<<< EDIT IT

        name_user = self.bot.get_chat(com.user_creator).first_name
        return f'You realy delete:\n**{name_user}**\n__{comment.text}__', bts


    @send_msg
    def edit_comment(self, arg_id):
        comment = self.db.get_comment(arg_id)
        bts = [[Button('Cancel', callback_data = "delete_this_msg")]]
        return 'ok send me new text for', btn


    @send_msg
    def welkom(self):
        return 'Welkom to bot', [[Button("GO", callback_data='open main_menu'),]]
        
    @send_msg
    def main_menu(self):
        return 'Main menu', [[Button("Список каналов", callback_data='open ch_list'),]]

    @send_msg
    def ch_list(self):
        self.db.set_user_param(self.user_id, 'mode_write', 'off')
        
        channels = self.db.get_all_ch(self.user_id)
        bts = [[Button(' Назад', callback_data='open main_menu')]]

        if channels:
            bts[0].append(Button(' Добавить', callback_data='open add_ch'))
            for ch in channels:
                try:
                    ch_name = self.bot.get_chat(ch).title
                except:
                    ch_name = 'No admin'
                bts.append([Button(str(ch_name), callback_data='open ch_setting ' + str(ch)),])
        else:
            bts.append([Button(' Добавить', callback_data='open add_ch')])
        return 'List channel: ', bts

    @send_msg
    def add_ch(self):
        self.db.set_user_param(self.user_id, 'mode_write', 'add_ch')
        return 'Enter username your channel:', [[Button('Назад ', callback_data='open ch_list')]]

    @send_msg
    def add_ch_final(self, result):
        if result == 'Added':
            self.db.set_user_param(self.user_id, 'mode_write', 'off')
            time.sleep(2)
        
        print(result)

        #TODO:

        return result, None

        
    @send_msg
    def ch_setting(self, arg_id):

        channel = self.db.get_ch_setting(int(ch_id))
        print(channel)

        #TODO:
        
        return 'Setting'
        

    @send_msg
    def del_end_msg(self):
        self.bot.delete_message(chat_id) #TODO:  <======
        return False, None


        










