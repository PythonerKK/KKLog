from flask import Blueprint,url_for,render_template,redirect,request,flash
from flask_login import login_required
from models import Admin,Post,Comment,Category
from forms import PostForm,CategoryForm
from extensions import db
admin_bp=Blueprint('admin',__name__)

@admin_bp.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page=request.args.get('page',1,type=int)
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=20)
    posts=pagination.items
    return render_template('manage_post.html',pagination=pagination,posts=posts)

@admin_bp.route('/category/manage')
@login_required
def manage_category():
    page=request.args.get('page',1,type=int)
    pagination=Category.query.paginate(page,per_page=20)
    categories=pagination.items
    return render_template('manage_category.html',pagination=pagination,categories=categories)


@admin_bp.route('/post/<int:post_id>/delete',methods=['POST'])
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('文章已删除！.','success')

    return redirect(url_for('.manage_post'))

@admin_bp.route('/post/<int:post_id>/edit',methods=['GET','POST'])
@login_required
def edit_post(post_id):
    form=PostForm()
    post=Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title=form.title.data
        post.body=form.body.data
        post.category=Category.query.get(form.category.data)
        db.session.commit()
        flash('文章已更新','success')
        return redirect(url_for('blog.show_post',slug=post.title))
    form.title.data=post.title
    form.body.data=post.body
    form.category.data=post.category
    return render_template('edit_post.html',form=form)



@admin_bp.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        title=form.title.data
        body=form.body.data
        category=Category.query.get(form.category.data)
        if Post.query.filter_by(title=title).first():
            print('标题重复')
            title=title+'_'
        post=Post(title=title,body=body,category=category)
        db.session.add(post)
        db.session.commit()
        flash('文章发布成功！','success')
        return redirect(url_for('blog.show_post',slug=post.title))
    return render_template('new_post.html',form=form)

@admin_bp.route('/comment/<comment_id>/delete',methods=['GET','POST'])
@login_required
def delete_comment(comment_id):
    comment=Comment.query.get_or_404(comment_id)
    print(comment)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('blog.index'))



@admin_bp.route('/category/<int:category_id>/delete',methods=['POST'])
@login_required
def delete_category(category_id):
    category=Category.query.get_or_404(category_id)
    if category.id==1:
        flash('你不能把默认的分类删除！','warning')
        return redirect(url_for('.manage_category'))
    category.delete()
    flash('分类已删除！','success')
    return redirect(url_for('.manage_category'))

@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
    filter_rule=request.args.get('filter','all')
    page=request.args.get('page',1,type=int)
    if filter_rule=='unread':
        filtered_comments=Comment.query.filter_by(reviewed=False)
    elif filter_rule=='admin':
        filtered_comments=Comment.query.filter_by(from_admin=True)
    else:
        filtered_comments=Comment.query
    pagination=filtered_comments.order_by(Comment.timestamp.desc()).paginate(page,per_page=20)
    comments=pagination.items
    return render_template('manage_comment.html',pagination=pagination,comments=comments)

@admin_bp.route('/comment/<int:comment_id>/approve')
@login_required
def approve_comment(comment_id):
    comment=Comment.query.get_or_404(comment_id)
    comment.reviewed=True
    db.session.commit()
    flash('审核通过！','success')
    return redirect(url_for('.manage_comment'))






@admin_bp.route('/category/new',methods=['GET','POST'])
@login_required
def new_category():
    form=CategoryForm()
    if form.validate_on_submit():
        name=form.name.data
        if form.validate_name(name):
            category=Category(name=name)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('admin.manage_category'))
        else:
            flash('分类名字已经存在','warning')
            return redirect(url_for('admin.manage_category'))

    return render_template('new_category.html',form=form)


@admin_bp.route('/new')
@login_required
def new():
    return render_template('new_page.html')


@admin_bp.route('/manage')
@login_required
def manage():
    return render_template('manage_page.html')