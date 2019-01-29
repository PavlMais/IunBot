from telegram import error
class PrivateHandler(object):

    def __init__(self, view, db, bot, post_editor):
        self.view = view
        self.db   = db
        self.bot  = bot
        self.post_editor = post_editor

    def main(self, bot, msg):
        msg = msg.message
        user = self.db.check_user(msg.chat.id)
        if user.mode_write == 'add_ch':
            result = self.check_ch(msg.chat.id, msg.text)

            self.view.add_ch_final(msg, edit_msg = True, result = result)
            
        elif user.mode_write.split()[0] == 'write_comment':
            
            self.post_editor.new_comment(bot, msg.chat.id, user.mode_write.split()[1], msg.text)

        else:
            self.view.main_menu(msg, edit_msg=False)

    def check_ch(self, user_id, ch_name):
        print(ch_name)

        if len(ch_name.split('t.me/')) > 1:
            ch_name = ch_name.split('t.me/')[1]

        if not ch_name[0] =='@':
            ch_name = '@' + ch_name
        print(ch_name)
        try:
            admins = self.bot.get_chat_administrators(ch_name)
        except error.BadRequest as e:
            print('ERROR: ', e)
            e = str(e)

            if not e == 'Chat not found':
                return 'NotFound'
            if not e == 'Supergroup members are unavailable':
                return 'NoAdmin'

        print('ADMINS ===========================================')
        print(admins)
       

        for admin in admins:
            if admin.user.id == 739272731:
                print(admin)
                if admin.can_edit_messages == False:
                    return 'CantEditMsg'
        
        ch_id  = self.bot.get_chat(ch_name).id

        if ch_id in self.db.get_all_ch(user_id):
            return 'ChannelExists'

        
        self.db.add_channel(user_id, ch_id)
        return 'Added'
        

    def command(self, bot, msg):
        msg = msg.message

        print(msg.text)
        msg_txt = msg.text.split()

        if len(msg_txt) == 2 and msg_txt[0] == '/start':
            self.view.first_menu_comments(msg, post_id = msg_txt[1])
        elif msg.text == '/start':
            self.view.welkom(msg, edit_msg=False)


