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
            print(func.__name__, 'KWARGS docor: ',kwargs)

            user = self.db.check_user(msg.chat.id)
            self.user_id = msg.chat.id

            text, buttons = func(self, *args, **kwargs)

            if text is False:
                return
            if buttons is None:
                bts = None
            else:
                bts = Markup(buttons)
            print(bts)
            if edit_msg:
                try:
                    self.bot.edit_message_text(text, chat_id = msg.chat.id, message_id = msg.message_id,
                                               parse_mode = 'html', reply_markup = bts)
                except Exception as e:
                    print('Error send message: ', e)
                    self.bot.send_message(msg.chat.id, text, parse_mode = 'html', reply_markup = bts)
            else:
                self.bot.send_message(msg.chat.id, text, parse_mode = 'html', reply_markup = bts)
        return wraper

    @send_msg
    def ch_setting(self, arg_id):
        channel = self.db.get_ch_setting(int(arg_id))

        bts = [
            [
                Button('Назад', callback_data='open ch_list'),
                Button('Статус', callback_data='l'),
            ],
            [
                Button('Добивить коментариев к посту', callback_data='d')
            ],
            [
                Button('Максимальная длина каментария', callback_data='d')
            ],
            [
                Button('Сортировать коментарии', callback_data='d')
            ],
            
            [
                Button('Кто сожет писать комментарии', callback_data='d')
            ],
            [
                Button('Настроить кнопки', callback_data='d')
            ],
            
        ]
        return 'Setting', bts


    def build_comment(self, comnt, is_admin):
        if comnt.user_creator == self.user_id:
            is_liked  = '♥️'
            call_data = 'None'
        elif comnt.users_liked and self.user_id in comnt.users_liked:
            is_liked  = '💖'
            call_data = 'comment dislike ' + str(comnt.id)
        else:
            is_liked  = '❤️'
            call_data = 'comment like ' + str(comnt.id)

        bts = [Button(is_liked + str(comnt.liked_count), callback_data=call_data)]
        
        if comnt.user_creator == self.user_id:
            bts.append(Button('🗑',   callback_data='open confirm_del '  + str(comnt.id)))
            bts.append(Button('edit',callback_data='open edit_comment ' + str(comnt.id)))
        elif is_admin:
            bts.append(Button('🗑', callback_data='open confirm_del ' + str(comnt.id)))

        text = f'<b>{comnt.get_user_name(self.bot)}</b>  🕑 {comnt.date_add}\n<i>{comnt.text}</i>'
        return text, [bts]





    @send_msg
    def comments(self, post_id):
        post = self.db.get_post(post_id)

        is_admin = post.channel_id in self.db.get_all_ch(self.user_id) 

        for comment in post.comments:
            time.sleep(0.5)
            
            text, bts = self.build_comment(comment, is_admin)
            
            self.bot.send_message(self.user_id, text, reply_markup = Markup(bts), parse_mode = 'html')

        self.bot.send_message(self.user_id, 'Write your comments: ')
        self.db.set_user_param(self.user_id, 'mode_write', 'write_comment '+ str(post.id))
            
        return False, None

    @send_msg
    def comment(self, arg_id):
        comment = self.db.get_comment(arg_id)
        is_admin = comment.channel_id in self.db.get_all_ch(self.user_id) 
        
        return self.build_comment(comment, is_admin)





    @send_msg
    def confirm_del(self, arg_id):
        bts = [[Button('Yes', callback_data = "comment delete " + arg_id),
                Button('No', callback_data  = "open comment " + arg_id )]]
        return f'Delete this comment?', bts


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
    def del_end_msg(self):
        self.bot.delete_message(chat_id) #TODO:  <======
        return False, None


        










