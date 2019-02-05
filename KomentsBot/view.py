from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Markup
import time


import config


class View(object):
    def __init__(self, bot, db):
        self.bot = bot
        self.db  = db
        

    def send_msg(func):
        def wraper(self, msg, edit_msg = True, *args, **kwargs):
            print('ARGS: ', args)
            print(func.__name__, 'KWARGS docor: ',kwargs)

            user = self.db.check_user(user_id = msg.chat.id)
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
                    self.bot.edit_message_text(text, chat_id = msg.chat.id, message_id = msg.message_id,
                                               parse_mode = 'html', reply_markup = bts)
                except Exception as e:
                    print('Error send message: ', e)
                    self.bot.send_message(msg.chat.id, text, parse_mode = 'html', reply_markup = bts)
            else:
                self.bot.send_message(msg.chat.id, text, parse_mode = 'html', reply_markup = bts)
        return wraper

    @send_msg
    def ch_setting(self, ch_id):
        channel = self.db.get_ch_setting(int(ch_id))

        bts = [
            [
                Button('Назад', callback_data='open ch_list'),
                Button('Статус: ' + channel.status, callback_data='l'),
            ],
            [
                Button('Отображать коментариев к посту: ' + str(channel.show_comnts_post), callback_data='open show_comnts_post')
            ],
            [
                Button('Максимальная длина каментари: ' + str(channel.max_len_comnt), callback_data='d')
            ],
            [
                Button('Сортировать: ' + channel.sort_comnts_pots, callback_data='d')
            ],
            # [
            #     Button('Настроить кнопки', callback_data='d')
            # ],
            
        ]
        return 'Setting', bts

    def bts_setting(self, ch_id):
        #TODO
        return 'text', None

    def show_comnts_post(self, ch_id):
        bts = [
            [
                Button('Назад', callback_data='open ch_setting ' + ch_id)
            ],
            [
                Button('Не добавлять', callback_data='open ch_setting ' + ch_id)
            ],
            [
                Button('1', callback_data='open ch_setting ' + ch_id)
            ],
            [
                Button('2', callback_data='open ch_setting ' + ch_id)
            ],
            [
                Button('3', callback_data='open ch_setting ' + ch_id)
            ],
        ]
        return 'текст', bts

    def build_comment(self, comnt, is_admin):
        if comnt.user_creator == self.user_id:
            is_liked  = '♥️'
            call_data = 'show you_creator'
        elif comnt.users_liked and self.user_id in comnt.users_liked:
            is_liked  = '💖'
            call_data = 'comment dislike ?comment_id=' + str(comnt.id)
        else:
            is_liked  = '❤️'
            call_data = 'comment like ?comment_id=' + str(comnt.id)
        print('CALLDATA BTN: ', call_data)
        bts = [Button(is_liked + str(comnt.liked_count), callback_data=call_data)]
        
        if comnt.user_creator == self.user_id:
            bts.append(Button('🗑', 
             callback_data='open confirm_del ?comment_id=' + str(comnt.id) + '&post_id=' + str(comnt.post_id)))
            bts.append(Button('edit',callback_data='open edit_comment ?comment_id=' + str(comnt.id)))
        elif is_admin:
            bts.append(Button('🗑', callback_data='open confirm_del ?comment_id=' + str(comnt.id)))

        text = f'<b>{comnt.get_user_name(self.bot)}</b>     {comnt.date_add}\n<i>{comnt.text}</i>'
        return text, [bts]


    # @send_msg
    # def comments(self, post_id, sort = 'top', offset = 0):
        
        
    #     post = self.db.get_post(post_id, sort_comnts = sort, limit_comnts = config.COMMENTS_OF_PARTY + 1, offset = offset)
    #     offset = str(int(offset) + config.COMMENTS_OF_PARTY)
    #     is_admin = post.channel_id in self.db.get_all_ch(self.user_id) 
    #     bts = []

    #     if post.comments:
    #         for comment in post.comments[:-1]:
    #             text_comment, bts_comment = self.build_comment(comment, is_admin)
    #             self.bot.send_message(self.user_id, text_comment, reply_markup = Markup(bts_comment), parse_mode = 'html')

    #         if len(post.comments) > config.COMMENTS_OF_PARTY:
    #             data_new = 'reopen comments ?post_id=' + post_id + '&sort=new&offset=' + offset
    #             data_top = 'reopen comments ?post_id=' + post_id + '&sort=top&offset=' + offset
    #             bts.append([
    #                 Button('Еще лучих',     callback_data = data_top ),
    #                 Button('Еще последних', callback_data = data_new ),
    #             ])
    #             tx = 'лучшие' if sort == 'top' else 'последние'
    #             text = f'Вот {tx} коментарии'
    #         else:
    #             text = 'Это все коментарии'

    #     else:
    #         text = 'Нету комментариев'
        
            
        bts.append([Button('Написать комментарий', callback_data='open write_comment ?post_id=' + str(post_id)), ])

        self.bot.send_message(self.user_id, text, reply_markup =  Markup(bts))
        return False, None

    @send_msg
    def write_comment(self, post_id):
        self.db.set_user_param(self.user_id, 'mode_write', 'write_comment '+ str(post_id))
        bts = [[Button('Отмена', callback_data = 'remove_yourself')]]
        self.bot.send_message(
            self.user_id,
            'Отправь мне текст комментария:',
            reply_markup = Markup(bts)
             )

        return False, None


    @send_msg
    def comment(self, comment_id):
        comment = self.db.get_comment(comment_id)
        is_admin = comment.channel_id in self.db.get_all_ch(self.user_id) 
        
        return self.build_comment(comment, is_admin)


    @send_msg
    def confirm_del(self, comment_id, post_id):
        data_yes = f'comment delete ?comment_id={comment_id}&post_id={str(post_id)}'

        bts = [[
            Button('Yes', callback_data = data_yes),
            Button('No',  callback_data = "open comment ?comment_id=" + comment_id)
            ]]
        return 'Delete this comment?', bts


    @send_msg
    def edit_comment(self, comment_id):
        comment = self.db.get_comment(comment_id)
        btn = [[Button('Cancel', callback_data = "remove_yourself")]]
        self.bot.send_message(self.user_id, 'ok send me new text for', reply_markup = btn)
        return False, None


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
                    ch_name = ' | No admin'
                bts.append([Button(ch_name, callback_data='open ch_setting ?ch_id=' + str(ch)),])
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

    


        










