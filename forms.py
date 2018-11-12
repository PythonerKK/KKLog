from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField,TextAreaField,ValidationError,HiddenField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired,Length,Email,URL,Optional
class LoginForm(FlaskForm):
    username=StringField('账号',validators=[DataRequired(),Length(1,20)])
    password=PasswordField('密码',validators=[DataRequired(),Length(8,128)])
    remember=BooleanField('记住我')
    submit=SubmitField('登录')

from models import Category
class PostForm(FlaskForm):
    title=StringField('标题',validators=[DataRequired(),Length(1,60)])
    category=SelectField('分类',coerce=int,default=1)
    body=CKEditorField('内容',validators=[DataRequired()])
    submit=SubmitField('发布')

    def __init__(self,*args,**kwargs):
        super(PostForm, self).__init__(*args,**kwargs)
        self.category.choices=[
            (category.id,category.name) for category in Category.query.order_by(Category.name).all()
        ]

class CategoryForm(FlaskForm):
    name=StringField('类名',validators=[DataRequired(),Length(1,30)])
    submit=SubmitField('提交')

    def validate_name(self,field):
        if Category.query.filter_by(name=field).first():
            return False
        else:
            return True



class CommentForm(FlaskForm):
    author=StringField('姓名',validators=[DataRequired(),Length(1,30)])
    email=StringField('邮箱',validators=[DataRequired(),Email(),Length(1,254)])
    site=StringField('网址（可不填）',validators=[Optional(),URL(),Length(0,255)])
    body=TextAreaField('评论内容',validators=[DataRequired()])
    submit=SubmitField('提交评论')

class AdminCommentForm(CommentForm):
    author=HiddenField()
    email=HiddenField()
    site=HiddenField()