# -*- coding: utf-8 -*-
# @Author: srajith
# @Date:   2020-06-16 18:46:01
# @Last Modified by:   srajith
# @Last Modified time: 2020-06-18 13:08:27
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"
login_manager.login_message_category = 'info'


from rlms import routes