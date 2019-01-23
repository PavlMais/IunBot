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

        if post in self.db.get_all_ch(self.user_id)# admin
            pass



            # Continue here  <=========



        else: # no admin
            pass


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

        return result, None

        
    @send_msg
    def ch_setting(self, ch_id):

        channel = self.db.get_ch_setting(int(ch_id))
        print(channel)

        # status
        
        return 'Setting'










