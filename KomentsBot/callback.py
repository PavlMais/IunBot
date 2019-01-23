

class CallbackHandler(object):
    def __init__(self, view, db):
        self.view = view
        self.db = db
        self.methods = {
            'main_menu': view.main_menu,
            'ch_list'  : view.ch_list,
            'add_ch'   : view.add_ch
        }

    def main(self, bot, update):
      
        print(update.callback_query.data)
        
        data = update.callback_query.data

        data = data.split()

        if data[0] == 'open':
            self.methods[data[1]](update.callback_query.message)
