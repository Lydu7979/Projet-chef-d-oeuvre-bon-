
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

app = Flask(__name__)

@app.route('/')

def index():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True)

