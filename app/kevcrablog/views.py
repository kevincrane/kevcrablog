from flask import Blueprint, render_template, flash, redirect, request, url_for
from app import db
from app.kevcrablog.forms import PostForm
from app.kevcrablog.models import Post

# from appname import cache         # TODO add cache

blog = Blueprint('blog', __name__)


@blog.route('/')
@blog.route('/index', methods=['GET', 'POST'])
@blog.route('/index/<int:page>', methods=['GET', 'POST'])
# @cache.cached(timeout=1000)       # TODO add cache
def home(page=1):
    # posts = Post.all().paginate(page, Config.POSTS_PER_PAGE, False) #TODO pagination
    posts = Post.all()
    return render_template('index.html',
                           posts=posts)


@blog.route('/newpost', methods=['GET', 'POST'])
def newpost():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author_id=None)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('.home'))
    elif request.method == 'POST':
        flash("There was a problem submitting the form!", 'danger')
    return render_template('new_post.html',
                           form=form)
