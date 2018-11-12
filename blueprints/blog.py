from flask import Blueprint,render_template,request,flash,redirect,url_for
from models import Post,Category,Comment,Admin
from forms import AdminCommentForm,CommentForm
from extensions import db
import re
from text_unidecode import unidecode
from fakes import forge
blog_bp=Blueprint('blog',__name__)

def slugify(text,delim=u'-'):
    result=[]
    _punct_re=re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).lower().split())
    return unidecode(delim.join(result))

@blog_bp.route('/about')
def about():

    # admin=Admin.query.first()
    # if admin:
    #     admin.username="kk"
    #     admin.set_password('liyuankun')
    # db.session.add(admin)
    # db.session.commit()



    return render_template('about.html')

@blog_bp.route('/')
def index():
    page=request.args.get('page',1,type=int)
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=20)
    posts=pagination.items
    return render_template('index.html',pagination=pagination,posts=posts)



@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category=Category.query.get_or_404(category_id)
    page=request.args.get('page',1,type=int)
    pagination=Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page,per_page=20)
    posts=pagination.items

    return render_template('show_category.html',category=category,pagination=pagination,posts=posts)



@blog_bp.route('/post/<slug>',methods=['GET','POST'])
def show_post(slug):
    post=Post.query.filter_by(title=slug).first_or_404()
    page=request.args.get('page',1,type=int)
    pagination=Comment.query.with_parent(post).order_by(Comment.timestamp.desc()).paginate(page,10)
    comments=pagination.items

    if True!=True:
        form=AdminCommentForm()
        form.author.data='xxx'
        form.email.data='xxx'
        form.site.data='xxx'
        from_admin=True
        reviewed=True
    else:
        form=CommentForm()
        from_admin=False
        reviewed=False
    if form.validate_on_submit():
        author=form.author.data
        email=form.email.data
        site=form.site.data
        body=form.body.data
        comment=Comment(
            author=author,email=email,site=site,body=body,from_admin=from_admin,post=post,reviewed=reviewed
        )
        db.session.add(comment)
        db.session.commit()
        #
        if True!=True:
            flash('评论已发布！','success')
        else:
            flash('Thanks,your comment will published after reviewed.','info')
        return redirect(url_for('.show_post',slug=post.title))


    return render_template('post.html',post=post,pagination=pagination,comments=comments,form=form)

@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment=Comment.query.get_or_404(comment_id)
    return redirect(url_for('.show_post',slug=comment.post.title,reply=comment_id,author=comment.author)+'#comment-form')

@blog_bp.route('/search')
def search():
    q=request.args.get('q','')
    if q=='':
        flash('请重新输入','info')
        return redirect(url_for('blog.index'))

    page = request.args.get('page', 1, type=int)
    pagination=Post.query.whooshee_search(q).paginate(page,per_page=20)
    results=pagination.items
    print(results)
    return render_template('search.html',results=results,pagination=pagination)
