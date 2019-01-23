from telegram import error
class PrivateHandler(object):

    def __init__(self, view, db, bot):
        self.view = view
        self.db   = db
        self.bot  = bot

    def main(self, bot, msg):
        msg = msg.message
        user = self.db.check_user(msg.chat.id)
        if user.mode_write == 'add_ch':
            rules, ch_name = self.check_ch(msg.text)

            if rules['can_edit_messages'] == True:
                self.db.add_channel(msg.chat.id, self.bot.get_chat(ch_name).id)


            self.view.add_ch_final(msg, edit_msg = True, rules = rules)
        else:
            self.view.welkom(msg, edit_msg=False)

    def check_ch(self, ch_name):
        print(ch_name)
        rules = {
            'exists': False,
            'admin': False,
            'can_edit_messages': False,
            'added': False
        }
        if len(ch_name.split('t.me/')) > 1:
            ch_name = ch_name.split('t.me/')[1]

        if not ch_name[0] =='@':
            ch_name = '@' + ch_name
        print(ch_name)
        try:
            admins = self.bot.get_chat_administrators(ch_name)
        except error.BadRequest as e:
            print(e)
            e = str(e)

            if e == 'Chat not found':
                return rules

            rules['exists'] = True

            if e == 'Supergroup members are unavailable':
                return rules
        print('ADMINS ===========================================')
        print(admins)
        rules['admin'] = True

        for admin in admins:
            if admin.user.id == 739272731:
                print(admin)
                
                rules['can_edit_messages'] = admin.can_edit_messages
        



        
        return (rules, ch_name)
        
        

        

    def command(self, bot, msg):
        msg = msg.message

        print(msg.text)
        msg_txt = msg.text.split()

        if len(msg_txt) == 2 and msg_txt[0] == '/start':
            self.view.comments(msg)
        elif msg.text == '/start':
            self.view.welkom(msg, edit_msg=False)


