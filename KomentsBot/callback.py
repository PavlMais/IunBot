

class CallbackHandler(object):
    def __init__(self, view, db, post_editor):
        self.view = view
        self.db = db
        self.post_editor = post_editor
        self.methods = {
            'main_menu' : view.main_menu,
            'ch_list'   : view.ch_list,
            'add_ch'    : view.add_ch,
            'ch_setting': view.ch_setting,
            'confirm_del':view.confirm_del,
            'comment'   : view.comment
        }

    def main(self, bot, update):
        print('DATA:  --> ',update.callback_query.data)
        
        data = update.callback_query.data
        msg  = update.callback_query.message


        data = data.split()

        if data[0] == 'open':
            if len(data) == 3:# for arg
                print('\n\n\t\tSEND ARG ID\n\n')
                self.methods[data[1]](msg, arg_id = data[2])
            else:
                self.methods[data[1]](msg)

        elif data[0] == 'comment':
            if data[1] =='delete':
                self.db.delete_comment(data[2])
                bot.delete_message(msg.chat.id, msg.message_id)
                self.post_editor.update_post(bot, comment_id = data[2])
                return
            elif data[1] == 'like':
                self.db.like_comment(data[2], msg.chat.id)

            elif data[1] == 'dislike':
                self.db.dislike_comment(data[2], msg.chat.id)

            self.view.comment(msg, arg_id = data[2])

            #TODO: update comments list for user and post for chennel
        elif data[0] == 'delete_this_msg':
            self.view.del_end_msg(msg)
