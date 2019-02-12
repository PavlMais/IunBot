import json
class ChSetting(object):
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']


        #TODO add on db
        self.status  = 'on'
        self.show_comnts_post = 2 # 0 - 3~ int
        self.max_len_comnt = 20 # 10 - 50~ int
        self.sort_comnts_pots = 'new' # new hot~ str
        self.can_write_comnt = 'all' # all only_fellowers str
        

class User(object):
    def __init__(self, data):
        self.id = data['id']
        self.mode_write = data['mode_write']

class Comment(object):
    def __init__(self, comment):
        self.id          = comment['id']
        self.post_id     = comment['post_id']
        self.user_name   = comment['user_name']
        self.channel_id  = comment['channel_id']
        self.text        = comment['text_main']
        self.date_add    = comment['date_add'].strftime('%H:%M') 
        self.user_creator= comment['user_creator_id']
        self.liked_count = comment['liked_count']
        self.users_liked = comment['users_liked']
        self.count_subcomnt = comment['count_subcomments']

    def __repr__(self):
        return f'<{self.text} {self.date_add} {self.liked_count}>'


class Post(object):
    def __init__(self, data):
        
        self.id        = data['id']
        self.msg_id    = data['msg_id']
        self.channel_id = data['channel_id']
        self.all_comments = data['all_comments']
        self.telegraph_path_new = data['telegraph_path_new']
        self.telegraph_path_top = data['telegraph_path_top']
        

        def __repr__(self):
            return str(self.id)



class Post(object):
    def __init__(self, user_id, type, text = None, photo = None, photo_url = None):
        self.user_id = user_id
        self.text = text
        self.photo = photo
        self.buttons = []
        self.published = False
        self.is_comments = False
        self.type = type
        self.photo_url = '&#8203;'
        self.publish_in = []
        self.date_publis = None
        self.date_delete = None
        


    def on_db(self, data):
        
        self.id        = data['id']
        self.msg_id    = data['msg_id']
        self.channel_id = data['channel_id']
        self.all_comments = data['all_comments']
        self.telegraph_path_new = data['telegraph_path_new']
        self.telegraph_path_top = data['telegraph_path_top']
        



        def __repr__(self):
            return str(self.id)






        


