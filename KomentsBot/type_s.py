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
        self.channel_id  = comment['channel_id'] #TODO: Add to DB
        self.text        = comment['text_main']
        self.date_add    = comment['date_add'].strftime('%H:%M') 
        self.user_creator= comment['user_creator_id']
        self.liked_count = comment['liked_count']
        self.users_liked = comment['users_liked']

    def __repr__(self):
        return f'<{self.text} {self.date_add} {self.liked_count}>'

    def get_user_name(self, bot):
        return bot.get_chat(self.user_creator).first_name
        

class Post(object):
    def __init__(self, data, comments):
        self.id        = data['id']
        self.msg_id    = data['msg_id']
        self.channel_id = data['channel_id']
        self.all_comments = data['all_comments']
        self.comments = []

        for comment in comments:
            self.comments.append(Comment(comment)) 


        def __repr__(self):
            return str(self.id)


        


