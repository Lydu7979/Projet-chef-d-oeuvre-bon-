
import datetime
from flask import Flask,  jsonify, request, render_template, redirect, url_for
from pathlib import Path
import os
import os.path
import pytest
import pandas as pd
import numpy as np
import sqlite3
import hashlib
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf,pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
import warnings                                  
warnings.filterwarnings('ignore')
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
import pymongo
from statsmodels.tsa.seasonal import seasonal_decompose
from datetime import date
import base64 
import time
timestr = time.strftime("%Y%m%d")
import dns
import logging
from Base_données.DBMongo import get_client_mongodb
from Base_données.DBsqlite import create_usertable, add_userdata, login_user, view_all_users
from Base_données.DB2sqlite import bdd_sql
import seaborn as sns
from Sécurité.Safe import modi, verif
from sklearn.preprocessing import MinMaxScaler
import pickle
from statsmodels.tsa.arima_model import ARIMAResults
import datetime 
from Pages_db.Admin import admin
import config
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import LoginForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import sqlite3
logging.basicConfig(filename='demo.log')
logging.debug('This message should go to the log file')

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])

def index():
    return render_template('base.html')

@app.route('/login')

def Log():
    return render_template('login.html', methods=["GET", "POST"])

@app.route('/connection')

def connet():
    return render_template('connection.html', methods=["GET", "POST"])


if __name__ == "__main__":
    app.run(debug=True)

