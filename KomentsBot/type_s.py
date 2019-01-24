class ChSetting(object):
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.status  = 'on'


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
        self.date_add    = comment['date_add']
        self.user_creator= comment['user_creator_id']
        self.liked_count = comment['liked_count']

    def __repr__(self):
        return self.text

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


        


