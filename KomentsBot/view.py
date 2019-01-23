from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Markup


class View(object):
    def __init__(self, bot, db):
        self.bot = bot
        self.db  = db
        

    def send_msg(func):
        def wraper(self, msg, edit_msg = True, *args, **kwargs):
            print(edit_msg)
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
                    print(e)
                    self.bot.send_message(msg.chat.id, text, reply_markup = bts)
            else:
                self.bot.send_message(msg.chat.id, text, reply_markup = bts)




        return wraper


    def comments(is_admin):
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
        bts = [[Button(' Назад', callback_data='open main_menu'), 
        Button(' Добавить', callback_data='open add_ch')]]
        for ch in channels:
            try:
                ch_name = self.bot.get_chat(ch[0])
            except:
                ch_name = 'No admin'
            bts.append([Button(ch_name, callback_data='open ch_sett' + str(ch[0])),])

        return 'List channel: ', bts

    @send_msg
    def add_ch(self):
        self.db.set_user_param(self.user_id, 'mode_write', 'add_ch')
        return 'Enter username your channel:', [[Button('Назад ', callback_data='open ch_list')]]

    @send_msg
    def add_ch_final(self, rules):
        self.db.set_user_param(self.user_id, 'mode_write', 'off')

        
        print(rules)

        return str(rules), None

        
    @send_msg
    def ch_setting(self, ch_id):

        channel = self.db.get_ch_setting(ch_id)











