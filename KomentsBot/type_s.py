class ChSetting(object):
    def __init__(self, id, user_id):
        self.id = id
        self.user_id = user_id

class User(object):
    def __init__(self, data):
        self.id = data['id']
        self.mode_write = data['mode_write']