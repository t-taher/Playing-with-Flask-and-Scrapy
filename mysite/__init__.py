# from flask import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import threading
from flask_mail import Mail
from mysite.info import y_t
# from site.dl import cr_m_spdr
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrybt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
threading.Thread(target=y_t).start()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME']= ''
app.config['MAIL_PASSWORD']=''
mail = Mail(app)

from mysite import routes
