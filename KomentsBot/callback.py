from utils import get_method_args
from buffer import buffer
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Markup



class CallbackHandler(object):
    def __init__(self, view, db, post_editor):
        self.view = view
        self.db = db
        self.post_editor = post_editor
        self.methods = {
            'main_menu'  : view.main_menu,
            'ch_list'    : view.ch_list,
            'add_ch'     : view.add_ch,
            'add_post'   : view.add_post,
            'ch_setting' : view.ch_setting,
            'confirm_del': view.confirm_del,
            'comment'    : view.comment,
            'bild_post'  : view.bild_post,
            'config_btn' : view.config_btn,
            'complete_post': view.complete_post,
            'select_type_btn': view.select_type_btn,
            'add_btn_name'   : view.add_btn_name,
            'add_btn_url': view.add_btn_url,
            'show_comnts_post': view.show_comnts_post,
            'write_subcomment': view.write_subcomment,
            'write_comment': view.write_comment,
            'edit_comment': view.edit_comment,
            #'comments'   : view.comments,
        }

    def main(self, bot, update):
        msg  = update.callback_query.message
        
        method, action, kwargs = get_method_args(update.callback_query.data)
        
        print('CALLBACK: ', method, action, kwargs)

        if method == 'open':
            self.methods[action](msg, **kwargs)

        elif method == 'send':
            if action == 'send_post':


                post = buffer.get_bildpost(msg.chat.id)
                
                if 'ch_id' in kwargs:
                    post.publish_in.append(kwargs['ch_id'])

                for ch_id in post.publish_in:

                    if post.type == 'text':
                        bot.send_message(ch_id, post.text, reply_markup = Markup(post.buttons))
                    elif post.type == 'photo':
                        pass
                
                self.view.send_post_complete(msg)


        elif method == 'ch_enable':

            ch_ids = buffer.get_arg_post(msg.chat.id, 'publish_in')

            if action == 'add':
                ch_ids.append(kwargs['ch_id'])

            elif action == 'del':
                ch_ids.remove(kwargs['ch_id'])

            buffer.set_arg_post(msg.chat.id, 'publish_in', ch_ids)
            
            self.view.complete_post(msg)


        elif method == 'reopen':
            bot.delete_message(msg.chat.id, msg.message_id)
            self.methods[action](msg, **kwargs)


        elif method == 'comment':

            if action =='delete':
                bot.delete_message(msg.chat.id, msg.message_id)
                self.db.delete_comment(**kwargs)
                self.post_editor.update_post(bot, **kwargs)  # not optimized 
                return

            elif action == 'like':
                self.db.like_comment(user_id = msg.chat.id, **kwargs)

            elif action == 'dislike':
                self.db.dislike_comment(user_id = msg.chat.id, **kwargs)

            self.view.comment(msg, **kwargs)
            self.post_editor.update_post(bot, **kwargs)  # not optimized 

     
        elif method == 'remove_yourself':
            bot.delete_message(msg.chat.id, msg.message_id)
        elif method == 'show':
            if action == 'you_creator':
                bot.answer_callback_query(update.callback_query.id, 'Ти не можешь лайкать свой коментарий')
