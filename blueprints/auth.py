from flask import Blueprint,redirect,url_for,render_template,flash
from models import Admin
from forms import LoginForm
from flask_login import login_user,current_user,logout_user,login_required
from extensions import load_user

auth_bp=Blueprint('auth',__name__)

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data

        remember=form.remember.data
        admin=Admin.query.first()
        if admin:
            print(admin.validate_password(password))
            if username==admin.username and admin.validate_password(password):

                login_user(admin,remember)
                flash('欢迎回来！','info')
                return redirect(url_for('blog.index'))
            else:
                flash('登录失败！','warning')
    return render_template('login.html',form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功！','info')
    return redirect(url_for('blog.index'))


