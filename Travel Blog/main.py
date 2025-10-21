from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

ckeditor = CKEditor(app)
Bootstrap5(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///posts.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    posts: Mapped[List["BlogPost"]] = relationship(back_populates="author")
    comments: Mapped[List["Comment"]] = relationship(back_populates="commented_user")
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(1000))
    username: Mapped[str] = mapped_column(String(100))

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    author_id_fk: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="parent_post")

class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    author_id_fk: Mapped[int] = mapped_column(ForeignKey("user.id"))
    commented_user: Mapped["User"] = relationship(back_populates="comments")
    post_id_fk: Mapped[int] = mapped_column(ForeignKey("blog_posts.id"))
    parent_post: Mapped["BlogPost"] = relationship(back_populates="comments")

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

def admin_only(func):
    '''
    Takes a function f (usually a Flask route) and wraps it with extra logic.
    @wraps(f)
    From functools.
    Makes sure the wrapped function (decorated_function) keeps the same name, docstring, etc. as f instead of being replaced.    
    '''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.id != 1:
                return abort(403)
            else:
                return func(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    new_register_form = RegisterForm()
    if new_register_form.validate_on_submit():
        email = new_register_form.email.data
        if User.query.filter_by(email=email).first():
            return render_template('register.html', register_form=new_register_form, error='Email entered has an account already!')
        
        salted_password = generate_password_hash(
            new_register_form.password.data,
            method="pbkdf2:sha256", 
            salt_length=8
        )
        new_user = User(email=email, password=salted_password, username=new_register_form.username.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('get_all_posts'))

    return render_template("register.html", register_form=new_register_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        with app.app_context():
            result = db.session.execute(db.select(User).where(User.email == email))
            user = result.scalar()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('get_all_posts'))
        elif user == None:
            flash('Email does not exist in Database')
            return redirect(url_for('login'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))
    return render_template('login.html', login_form=login_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    if current_user.is_authenticated:
        return render_template("index.html", all_posts=posts, logged_in=current_user.is_authenticated, user=current_user)
    else:
        return render_template("index.html", all_posts=posts, logged_in=current_user.is_authenticated, user=None)

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id):
    comment_form = CommentForm()
    requested_post = db.get_or_404(BlogPost, post_id)
    post_comments = requested_post.comments
    
    if comment_form.validate_on_submit():
        if current_user.is_authenticated:
            with app.app_context():
                get_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id))
                commented_post = get_post.scalar()

            new_comment = Comment(
                comment = comment_form.comment.data,
                author_id_fk = current_user.id,
                commented_user = current_user,
                post_id_fk = post_id,
                parent_post = requested_post,
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for("show_post", post_id=post_id))
        else:
            flash("You need to login or register to comment.")
            return redirect(url_for('login'))

    if current_user.is_authenticated:
        return render_template("post.html", post=requested_post, post_comments=post_comments, user_id=current_user.id, form=comment_form)
    else:
        return render_template("post.html", post=requested_post, post_comments=post_comments, user_id=None, form=comment_form)

@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            author_id_fk = current_user.id,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=False)
