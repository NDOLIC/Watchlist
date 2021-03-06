from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    comment = db.relationship("Comments", backref="user", lazy ="dynamic")
    

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):

    __tablename__='roles'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_posted = db.Column(db.DateTime)


    def save_post(self):
        '''
        Function to save a new post.
        '''
        db.session.add(self)
        db.session.commit()
    @classmethod
    def clear_post(cls):
        '''
        function that clears all the posts in the form after submission
        '''
        Post.all_posts.clear()

    @classmethod
    def get_post(cls):
        '''
        function that gets particular posts when requested by date posted
        '''
        posts = Post.query.all()
        return posts

class Comments(db.Model):
    '''
    comment class that create instance of comment
    '''
    __tablename__ = 'comment'

    #add columns
    id = db.Column(db. Integer, primary_key=True)
    comment_name = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    def save_comment(self):
        '''
        save the comment per post
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comment = Comments.query.order_by (Comments.date_posted.desc()).all()
        return comment 

    @classmethod
    def delete_comment(cls,id):
        comment = Comments.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()

class Subscriber(UserMixin, db.Model):
    __tablename__="subscribers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    title = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_subscribers(cls,id):
        return Subscriber.query.all()

    def __repr__(self):
       return f'User {self.email}'
