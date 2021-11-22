from app.forms import LoginForm, RegisterForm, ResetPasswordForm, NewPasswordForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,  jsonify, request, render_template, redirect, url_for
logging.basicConfig(filename='demo.log')
logging.debug('This message should go to the log file')
from app import app2, db, bcrypt
from app.models import UserModel

app2 = Flask(__name__)

@app2.route('/', methods=["GET", "POST"])

def index():
    return render_template('base.html')

@app2.route('/login')

def Log():
    return render_template('login.html', methods=["GET", "POST"])

@app2.route('/connection')

def connet():
    return render_template('connection.html', methods=["GET", "POST"])
