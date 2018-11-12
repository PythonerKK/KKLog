from flask import Flask,redirect,render_template,url_for,flash
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
from blueprints.blog import blog_bp
from extensions import db,ckeditor,moment,mail,bootstrap,login_manager,load_user,csrf,whooshee
from models import Admin,Category,Comment
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from fakes import forge
import config

def register_logging(app):
    pass
def register_extensions(app):
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    whooshee.init_app(app)
def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
def register_shell_context(app):
    @app.shell_context__processor
    def make_shell_context():
        return dict(db=db)

def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin=Admin.query.first()
        categories=Category.query.order_by(Category.name).all()
        if current_user.is_authenticated:
            unread_comments=Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments=None

        return dict(admin=admin,categories=categories,unread_comments=unread_comments)

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return 'bad request'

def create_app():
    app=Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_logging(app)
    register_errors(app)
    register_template_context(app)
    return app

app=create_app()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('400.html',description=e.description),400


if __name__ == '__main__':
    app.run(port=5000)
    #app.run(host='0.0.0.0',port=5000)