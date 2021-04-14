from flask import Flask, render_template, request, url_for, redirect, flash 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from flask_wtf import FlaskForm
#from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import UserMixin, login_user, current_user, logout_user, login_required, LoginManager
#from flask.ext.user import roles_required



app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flask_warships'
app.config['SECRET_KEY'] = '8456984at5b1ace7gfs578fhdjs129e8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/warship_jan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#csrf = CsrfProtect(app)
bcrypt =Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



from warships_blog import routes