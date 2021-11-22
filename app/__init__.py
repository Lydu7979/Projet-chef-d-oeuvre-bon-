import flask_monitoringdashboard as dashboard
from flask import Flask, redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash

app2 = Flask(__name__)

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
csrf = CSRFProtect()
login = LoginManager()
login.login_view = "users.login"
bcrypt = Bcrypt()

from app import routes

