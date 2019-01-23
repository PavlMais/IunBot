import psycopg2
import psycopg2.extras
from type_s import User, ChSetting

try:
    import local_config as config
except:
    import config


class DB(object):
    def __init__(self):
        self.conn = psycopg2.connect(config.DB_URL)
    

    def check_user(self, user_id):
        with self.conn:
            with self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
                cur.execute(""" INSERT INTO Users (id)
                                SELECT %s WHERE 
                                    NOT EXISTS (
                                        SELECT 1 FROM Users WHERE id = %s 
                                        );
                                SELECT * FROM Users WHERE id = %s;
                                    """, (user_id, user_id, user_id,))
                        
                data = cur.fetchone()

        return User(dict(data))


    def set_user_param(self, user_id, set, arg):   
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("UPDATE Users SET {} = %s WHERE id = %s;".format(set), (arg, user_id,))


    def user_get(self, user_id, get):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT {} FROM Users WHERE id = %s;".format(get),(user_id,))
                get = cur.fetchone()[0]
        return get



    def add_channel(self, user_id, ch_id):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("""insert into chsetting (id, user_id) VALUES (%s, %s)""",(ch_id, user_id,))
            

    def get_all_ch(self, user_id):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("""SELECT id FROM chsetting WHERE user_id = %s""",(user_id,))
                channels = cur.fetchall()
                print(channels, type(channels))

        return channels

    def get_ch_setting(self, ch_id):
        with self.conn:
            with self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
            
                cur.execute("""SELECT * FROM chsetting WHERE id = %s""",(user_id,))
                channel = cur.fetchall()
        return ChSetting(dict(channel))
