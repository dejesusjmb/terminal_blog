from database import Database
from models.blog import Blog

__author__ = 'dejesusjmb'


class Menu(object):
    def __init__(self):
        self.user = input('Input author name: ')
        self.user_blog = None
        if self._user_has_account():
            print('Welcome back {}'.format(self.user))
        else:
            print('Hello, {}! Please create an account.'.format(self.user))
            self._create_an_account()

    def _user_has_account(self):
        blog = Database.find_one('blog', {'author': self.user})
        if blog is not None:
            self.user_blog = Blog.from_mongo(blog['id'])
            return True
        return False

    def _create_an_account(self):
        title = input('Input blog title: ')
        description = input('Input blog description: ')
        blog = Blog(author=self.user,
                    title=title,
                    description=description)
        blog.save_to_mongo()
        self.user_blog = blog

    def run_menu(self):
        user_action = input('Do you like to read (R) or write (W) blogs? ')
        if user_action == 'R':
            self._list_blogs()
            self._view_blog()
        elif user_action == 'W':
            self.user_blog.new_post()
        else:
            print('Thank you for blogging!')

    @staticmethod
    def _list_blogs():
        blogs = Database.find(collection='blog',
                              query={})
        for blog in blogs:
            print('ID: {}\nAuthor: {}\nTitle: {}\nDescription:{}'.format(blog['id'],
                                                                         blog['author'],
                                                                         blog['title'],
                                                                         blog['description']))

    @staticmethod
    def _view_blog():
        blog_id = input('Input blog id you want to read: ')
        blog = Blog.from_mongo(blog_id)
        posts = blog.get_posts()
        for post in posts:
            print('Date:{}\nTitle: {}\nContent:{}\n\n'.format(post['created_date'],
                                                              post['title'],
                                                              post['content']))
