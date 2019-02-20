from config import TGPH_TOKEN
from telegraph import Telegraph


class TelegraphEditor(object):
    def __init__(self):
        self.tgph = Telegraph(TGPH_TOKEN)

    def new_comments(self):
        path_top = self.tgph.create_page(
            title = 'Komments | 0', html_content = '-'
        )['path']
        path_new = self.tgph.create_page(
            title = 'Komments | 0', html_content = '-'
        )['path']
        print('CREATED NEW COMMENTS: ', path_top)
        return path_new, path_top

    def update_comments(self, post_id, db):
        post = db.get_post_info_comments(post_id)
        print(post)
        print(type(post))
        print(post.telegraph_path_new)
        comments_new = db.get_comments(post_id, sort_comnts = 'new', limit_comnts = 25) 
        comments_top = db.get_comments(post_id, sort_comnts = 'top', limit_comnts = 25) 


        base = ' <a href="http://t.me/KomentsBot?start=0' + str(post_id) + '"> Add comments</a><br/>'
        path_new = post[0]
        path_top = post[1]
        body_new = f'Sort <b>New</b> <a href="https://telegra.ph/{path_top}">Top</a> ' + base
        body_top = f'Sort <a href="https://telegra.ph/{path_new}">New</a> <b>Top</b> ' + base


        b_com = '<h4>{}</h4>{}<br><a href="http://t.me/KomentsBot?start=1{}"> ✉️ {}  |  ❤️ {}  |  {}</a><br/>'



        for com in comments_new:

            body_new += b_com.format(com.user_name, com.text, com.id, com.count_subcomnt, com.liked_count, com.date_add)
            print(com.count_subcomnt)

            if com.count_subcomnt > 0:
                subcomnts = self.db.get_subcomments(com.id)
                print(subcomnts)

                for subcomnt in subcomnts:
                    body_new += f' |    <a href="/"><u><b>{subcomnt.user_name}</b>  |  ❤️ {subcomnt.liked_count}  |  {subcomnt.date_add}</u></a><br/> |     <aside>{subcomnt.text}</aside>  <br/>'
        




        for com in comments_top:
            body_top += b_com.format(com.user_name, com.text, com.id, com.count_subcomnt, com.liked_count, com.date_add)

        


        title = 'Komments | ' + str(post[3])

        print(post[0], post[1])

        r =self.tgph.edit_page(
            path = post[0],
            title = title,
            html_content = body_new
        )
        self.tgph.edit_page(
            path = post[1],
            title = title,
            html_content = body_top
        )

        print(r)


tgph_editor = TelegraphEditor()