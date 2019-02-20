import json
        

class User(object):
    def __init__(self, data):
        self.id = data.id
        self.mode_write = data.mode_write

class Comment(object):
    def __init__(self, comment):
        self.id          = comment.id
        self.post_id     = comment.post_id
        self.user_name   = comment.user_name
        self.channel_id  = comment.channel_id
        self.text        = comment.text_main
        self.date_add    = comment.date_add.strftime('%H:%M') 
        self.user_creator= comment.user_creator_id
        self.liked_count = comment.liked_count
        self.users_liked = comment.users_liked
        self.count_subcomnt = comment.count_subcomments

    def __repr__(self):
        return f'<{self.text} {self.date_add} {self.liked_count}>'



class Post(object):
    def __init__(self, user_id = None, type = None,
                 text = None,data = None, photo = None, photo_url = None, from_db = False):
        if from_db:
            self.id = data.id
            self.channel_id = data.channel_id
            self.msg_id = data.msg_id
            self.buttons = data.buttons
            self.all_comments = data.all_comments
            self.telegraph_path_top = data.telegraph_path_top
            self.telegraph_path_new = data.telegraph_path_new
        else:
            self.user_id = user_id
            self.text = text
            self.chennel_id = None
            self.photo = photo
            self.buttons = []
            self.comments_on = False
            self.type = type
            self.photo_url = '&#8203;'
        
    

    def __repr__(self):
        return str(self.id)






        


