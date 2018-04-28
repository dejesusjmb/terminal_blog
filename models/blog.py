import datetime
import uuid

from database import Database
from models.post import Post

__author__ = 'dejesusjmb'

class Blog(object):
    def __init__(self, author, title, description, id=None):
        self.author = author
        self.title = title
        self.description = description
        self.id = uuid.uuid4().hex if id is None else id

    def new_post(self):
        title = input('Enter post title: ')
        content = input('Enter post content: ')
        date = input('Enter post date, or leave blank for today (in format DDMMYYYY): ')
        date = datetime.datetime.utcnow() if date == '' else datetime.datetime.strptime(date, '%d%m%Y')
        post = Post(blog_id=self.id,
                    title=title,
                    content=content,
                    author=self.author,
                    date=date)
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self.id)

    def save_to_mongo(self):
        Database.insert(collection='blog',
                        data=self.json())

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description
        }

    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blog',
                                      query={'id': id})
        return cls(author=blog_data['author'],
                    title=blog_data['title'],
                    description=blog_data['description'],
                    id=blog_data['id'])
