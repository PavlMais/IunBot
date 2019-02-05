

class CallbackHandler(object):
    def __init__(self, view, db, post_editor):
        self.view = view
        self.db = db
        self.post_editor = post_editor
        self.methods = {
            'main_menu'  : view.main_menu,
            'ch_list'    : view.ch_list,
            'add_ch'     : view.add_ch,
            'ch_setting' : view.ch_setting,
            'confirm_del': view.confirm_del,
            'comment'    : view.comment,
            #'comments'   : view.comments,
            'show_comnts_post': view.show_comnts_post,
            'write_comment': view.write_comment,
            'edit_comment': view.edit_comment,
        }

    def main(self, bot, update):
        data = update.callback_query.data
        msg  = update.callback_query.message
        print('DATA:  --> ', data)

        if '?' in data:
            args = data.split('?')[1]
            kwargs = dict([n.split('=') for n in args.split('&')])
        else:
            kwargs = {}
        data = data.split()
        
       
        if data[0] == 'open':
            
            self.methods[data[1]](msg, **kwargs)

        elif data[0] == 'reopen':
            bot.delete_message(msg.chat.id, msg.message_id)
            self.methods[data[1]](msg, **kwargs)


        elif data[0] == 'comment':

            if data[1] =='delete':
                bot.delete_message(msg.chat.id, msg.message_id)
                self.db.delete_comment(**kwargs)
                self.post_editor.update_post(bot, **kwargs)  # not optimized 
                return

            elif data[1] == 'like':
                self.db.like_comment(msg.chat.id, **kwargs)

            elif data[1] == 'dislike':
                self.db.dislike_comment(msg.chat.id, **kwargs)

            self.view.comment(msg, **kwargs)
            self.post_editor.update_post(bot, **kwargs)  # not optimized 

     
        elif data[0] == 'remove_yourself':
            bot.delete_message(msg.chat.id, msg.message_id)
        elif data[0] == 'show':
            if data[1] == 'you_creator':
                bot.answer_callback_query(update.callback_query.id, 'Ти не можешь лайкать свой коментарий')
