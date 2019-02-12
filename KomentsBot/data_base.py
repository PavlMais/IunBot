import psycopg2
import psycopg2.extras


from type_s import User, ChSetting, Post, Comment
import config


class DB(object):
    def __init__(self):
        self.conn = psycopg2.connect(config.DB_URL)
    
    def connect(func):
        def decorator(self, *args, **kwargs):
            with self.conn:
                with self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as self.cur:

                    data = func(self, *args, **kwargs)

            return data
        return decorator

    @connect
    def check_user(self, user_id):
        self.cur.execute(""" INSERT INTO Users (id)
                        SELECT %s WHERE 
                            NOT EXISTS (
                                SELECT 1 FROM Users WHERE id = %s 
                                );
                        SELECT * FROM Users WHERE id = %s;
                            """, (user_id, user_id, user_id,))
                
        return User(dict(self.cur.fetchone()))

    @connect
    def set_user_param(self, user_id, set, arg):   
        self.cur.execute("UPDATE Users SET {} = %s WHERE id = %s;".format(set), (arg, user_id,))

    @connect
    def user_get(self, user_id, get):
        self.cur.execute("SELECT {} FROM Users WHERE id = %s;".format(get),(user_id,))
        return self.cur.fetchone()[0]
        


    @connect
    def add_channel(self, user_id, ch_id):
        self.cur.execute("""INSERT into chsetting (id, user_id)
                        VALUES (%s, %s)""",(ch_id, user_id,))
            
    @connect
    def get_all_ch(self, user_id):
        self.cur.execute(""" SELECT id FROM chsetting
                        WHERE user_id = %s""",(user_id,))
    
        return list(map(lambda x: x['id'], self.cur.fetchall()))

    @connect
    def get_ch_setting(self, ch_id):
       
        self.cur.execute("""SELECT * FROM chsetting
                        WHERE id = %s""",(ch_id,))
        
        return ChSetting(dict(self.cur.fetchone()))
    @connect
    def get_arg_channel(self, ch_id, args):
        self.cur.execute("select {} from chsetting where id = %s;".format(', '.join(args)), (ch_id,))
        data = self.cur.fetchone()
        return data[args[0]]

    @connect
    def set_btn_markup(self, ch_id, button_name, index, url = None):
        self.cur.execute("select default_btn_markup from chsetting where id = %s",(ch_id,))
        data = self.cur.fetchone()['default_btn_markup']
        print('>>>>> ', data)

        data[index[0]].insert(index[1], {'text':button_name, 'url': url})

        self.cur.execute(
            "updata chsetting set default_btn_markup = %s where id = %s;",
            (data, ch_id,)
        )
        





    @connect
    def new_post(self, chennel_id,  msg_id, telegraph_path_new, telegraph_path_top):
        self.cur.execute("""insert into posts (msg_id, channel_id, telegraph_path_new, telegraph_path_top)
                 VALUES (%s, %s, %s, %s) RETURNING id;""",(msg_id, chennel_id, telegraph_path_new, telegraph_path_top,))
                
        return self.cur.fetchone()['id']
    @connect
    def get_post(self, post_id = None, comment_id = None,  comments = True):
        
        if post_id is None:
            print(comment_id)
            self.cur.execute("select post_id from coments where id = %s",(comment_id,))
            post_id = self.cur.fetchone()['post_id']

        self.cur.execute("""select * from posts where id = %s;""",(post_id,))
   
        return Post(self.cur.fetchone())

    @connect
    def get_comments(self, post_id, sort_comnts = 'new', limit_comnts = 3, offset = 0):
        if sort_comnts == 'new':
            self.cur.execute("""
                select * from coments
                where post_id = %s and type_comment = 'comment'
                order by date_add desc      
                limit %s offset %s;
            """,(post_id, limit_comnts, offset,))

        elif sort_comnts == 'top':
            self.cur.execute("""
                select * from coments
                where post_id = %s and type_comment = 'comment'
                order by liked_count desc
                limit %s offset %s;
            """,(post_id, limit_comnts, offset,))

        comments = self.cur.fetchall()
        return list(map(lambda comment: Comment(comment), comments))
    
    @connect
    def get_subcomments(self, root_comment_id):
        self.cur.execute("""
            select * from coments
            where type_comment = 'subcomment' and root_comment_id = %s;
        """, (root_comment_id,))
        comments = self.cur.fetchall()
        print(comments)
        return list(map(lambda comment: Comment(comment), comments))

   

    @connect
    def new_comment(self, user_id, text, user_name, post_id):
        self.cur.execute("""
            select channel_id from posts where id = %s;
        """,(post_id,))

        channel_id = self.cur.fetchone()['channel_id']

        self.cur.execute("""
            insert into coments (text_main, post_id, user_creator_id, channel_id, user_name, type_comment)
            values (%s, %s, %s, %s, %s, 'comment'   );

            update posts set all_comments = all_comments + 1 where id = %s;""",
            (text, post_id, user_id, channel_id, user_name, post_id,)
        )
        return post_id


    @connect
    def new_subcomment(self, user_id, text, user_name, root_comnt_id):
        self.cur.execute("""
            select post_id, channel_id from coments where id = %s;
        """, (root_comnt_id,))

        ids = self.cur.fetchone()
        post_id = ids['post_id']
        channel_id = ids['channel_id']

        self.cur.execute("""
            insert into coments (text_main, post_id, user_creator_id, channel_id, user_name, type_comment, root_comment_id)
            values (%s, %s, %s, %s, %s, 'subcomment', %s);

            update posts set all_comments = all_comments + 1 where id = %s;
            update coments set count_subcomments = count_subcomments + 1 where id = %s;""",
            (text, post_id, user_id, channel_id, user_name, root_comnt_id, post_id, root_comnt_id,)
        )       
        return post_id 

    @connect
    def like_comment(self, user_id, comment_id):
        self.cur.execute("""UPDATE coments SET 
                    liked_count = liked_count + 1,
                    users_liked = ARRAY_APPEND(users_liked, %s)
                    WHERE id = %s;""", (user_id, comment_id,))

    @connect
    def dislike_comment(self, user_id, comment_id):
        
        self.cur.execute("""update coments set
                    liked_count = liked_count - 1,
                    users_liked = ARRAY_REMOVE(users_liked, %s) 
                    WHERE id = %s;""", (user_id, comment_id,))

    @connect
    def delete_comment(self, comment_id, post_id):
        
        self.cur.execute("""update posts set all_comments = all_comments - 1
                        where id = %s;
                    delete from coments where id = %s;
                    """, (post_id, comment_id,))
                    
    @connect
    def get_comment(self, comment_id):
        
        self.cur.execute("""
                    select * from coments where id = %s
                    """,(comment_id,))
        
        return Comment(self.cur.fetchone())
