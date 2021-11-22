from datetime import datetime
from app import db, login_manager  
from time import time
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
import jwt

ACCESS = {'user': 0,'admin': 1}

class UserModel(UserMixin, db.Model):

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    hashed_password = db.Column(db.String(60), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=True)
    access = db.Column(db.Integer, default=1)

    def __init__(self, id, username, email, text_password, access=ACCESS['user']):
        
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = generate_password_hash(text_password)
        self.registered_on = datetime.now()
        self.access = access

    def is_admin(self):
        return self.access == ACCESS['admin']
    
    def allowed(self, access_level):
        return self.access >= access_level


    def check_password(self, text_password:str):
        return check_password_hash(self.hashed_password, text_password)


    def set_password(self, text_password, commit=False):
        self.hashed_password = generate_password_hash(text_password)
        if commit:
            db.session.commit()

    def get_reset_token(self, expires=500):
        return jwt.encode({'reset_password': self.username, 'exp': time() + expires},
                           key=os.getenv('SECRET_KEY'))

    def __repr__(self):
        return 'User {}'.format(self.username)

    @staticmethod
    def admin_exist():
        user_exists = UserModel.query.filter_by(username='admin')
        #print(user_exists)
        if user_exists:
            return True
        return False

    @staticmethod
    def verify_reset_token(token):
        try:
            username = jwt.decode(token, key=os.getenv('SECRET_KEY'), algorithms=["HS256"])['reset_password']
            print(username)
        except Exception as e:
            print(e)
            return
        return UserModel.query.filter_by(username=username).first()

    @staticmethod
    def create_user(username, plaintext_password, email):
        user_exists = UserModel.query.filter_by(email=email).first()
        if user_exists:
            return False

        user = UserModel()

        user.username = username
        user.hashed_password = user.set_password(plaintext_password)
        user.email = email

        db.session.add(user)
        db.session.commit()

        return True

    @staticmethod
    def login_user(email, text_password):
        user = UserModel.query.filter_by(email=email).first()

        if user:
            if user.check_password(text_password):
                return True
        return False

    @staticmethod
    def verify_email(email):
        user = UserModel.query.filter_by(email=email).first()
        return user

    @property
    def is_authenticated(self):
        """Return True if the user has been successfully registered."""
        return True

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)

