from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_whooshee import Whooshee

bootstrap=Bootstrap()
db=SQLAlchemy()
moment=Moment()
ckeditor=CKEditor()
mail=Mail()
csrf=CSRFProtect()
whooshee=Whooshee()
login_manager=LoginManager()
login_manager.login_view='auth.login'
login_manager.login_message_category='warning'
login_manager.login_message='Please log in to access this page'
@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    user=Admin.query.get(int(user_id))
    return user