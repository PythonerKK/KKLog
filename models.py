from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from extensions import whooshee
class Admin(db.Model,UserMixin):
    __tablename__='admin'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100))
    password_hash=db.Column(db.String(128))
    blog_title=db.Column(db.String(100))
    blog_sub_title=db.Column(db.String(100))
    name=db.Column(db.String(100))
    about=db.Column(db.Text)

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)
class Category(db.Model):
    __tablename__='category'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),unique=True)
    posts=db.relationship('Post',back_populates='category')

    def delete(self):
        default_category=Category.query.get(1)
        posts=self.posts[:]
        for post in posts:
            post.category=default_category
        db.session.delete(self)
        db.session.commit()

@whooshee.register_model('title','body')
class Post(db.Model):
    __tablename__='post'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    body=db.Column(db.Text)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id',ondelete='CASCADE',onupdate='CASCADE'))
    category=db.relationship('Category',back_populates='posts')
    comments=db.relationship('Comment',back_populates='post',cascade='all')

class Comment(db.Model):
    __tablename__='comment'
    id=db.Column(db.Integer,primary_key=True)
    author=db.Column(db.String(100))
    email=db.Column(db.String(254))
    site=db.Column(db.String(255))
    body=db.Column(db.Text)
    from_admin=db.Column(db.Boolean,default=False)
    reviewed=db.Column(db.Boolean,default=False)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow,index=True)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id',ondelete='CASCADE',onupdate='CASCADE'))
    post=db.relationship('Post',back_populates='comments')

    replied_id=db.Column(db.Integer,db.ForeignKey('comment.id'))
    replied=db.relationship('Comment',back_populates='replies',remote_side=[id])
    replies=db.relationship('Comment',back_populates='replied',cascade='all')
