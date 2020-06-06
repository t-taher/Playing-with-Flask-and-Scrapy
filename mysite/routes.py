from flask import render_template, url_for, flash, redirect, request
import os
from mysite.forms import (RegistrationForm, LoginForm, Update_Form
                            , Postform, Reset_form, Reset_password)
from mysite.info import Run_spdr
from mysite import app, bcrybt, db, mail
from mysite.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import secrets
from PIL import Image

@app.route("/")
@app.route("/home")
def home():
    path = os.getcwd()
    Run_spdr("filgoal", path=path)
    os.chdir(f"{path}/mysite/tutorial")
    b = open("info.txt", "r")
    os.chdir(path)
    i = b.read()
    b.close()
    posts = eval(i)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        h_pass = bcrybt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(name=form.username.data, password=h_pass, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrybt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            n_page = request.args.get("next")
            return redirect(n_page) if n_page else redirect(url_for("home"))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/yesterday")
def yesterday():
    path = os.getcwd()
    os.chdir(f"{path}/mysite/tutorial")
    b = open("yesterday.txt", "r")
    os.chdir(path)
    i = b.read()
    b.close()
    posts = eval(i)
    # print('hala')
    return render_template('home.html', posts=posts)


@app.route("/tomorrow")
def tomorrow():
    path = os.getcwd()
    os.chdir(f"{path}/mysite/tutorial")
    b = open("tomorrow.txt", "r")
    os.chdir(path)
    i = b.read()
    b.close()
    posts = eval(i)
    return render_template('home.html', posts=posts)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


def save_pic(pic):
    random = secrets.token_hex(8)
    _, f_ext = os.path.splitext(pic.filename)
    pic_fn = random+f_ext
    pic_path = os.path.join(app.root_path, 'static/images', pic_fn)
    size = (125, 125)
    i = Image.open(pic)
    i.thumbnail(size)
    i.save(pic_path)
    return pic_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = Update_Form()
    if request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.name
    if form.validate_on_submit():
        if form.p_img.data:
            pic_f = save_pic(form.p_img.data)
            current_user.p_img = pic_f
        current_user.name = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("ur info has been updated", "success")
        redirect(url_for("account"))
    p_img = url_for("static",filename="images/"+current_user.p_img)
    return render_template("acc.html", title='account', form=form, img=p_img)


@app.route("/post", methods=['GET', 'POST'])
@login_required
def post():
    form = Postform()
    if form.validate_on_submit():
        p_post = Post(title=form.title.data, post=form.content.data, author=current_user)
        db.session.add(p_post)
        db.session.commit()
        flash("ur post has been created ", "success")
        return redirect(url_for('home'))

    return render_template("post.html", title="New Post", form=form)


@app.route("/post/<name_1>/<name_2>")
def match(name_1,name_2):
    return render_template("matches.html",)


@app.route("/posts", methods=['GET', 'POST'])
def posts():
    page = request.args.get('page', 1, type=int)
    p_posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=2)
    form = Postform()
    if form.validate_on_submit():
        p_post = Post(title=form.title.data, post=form.content.data, author=current_user)
        db.session.add(p_post)
        db.session.commit()
        flash("ur post has been created ", "success")
        return redirect(url_for('posts'))
    return render_template('posts.html', posts=p_posts, form=form)


def send(user):
    token = user.rest()
    msg = Message("password reset request", sender="no reply@demo.com",
                  recipients=[user.email])
    msg.body=f"""
to reset ur password visit the link below :
{url_for('reset_token',token=token, _external=True)}
if u did not request reset password just ignore this message"""
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = Reset_form()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send(user)
        flash("ur reset password email sent to ur email", "info")
        return redirect(url_for("login"))
    return render_template('reset_password.html', title='send request',form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user= User.verify(token)
    if user is None:
        flash("this token is invalid","warning")
        return redirect(url_for("reset_password"))
    form = Reset_password()
    if form.validate_on_submit():
        h_pass = bcrybt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = h_pass
        db.session.commit()
        flash('ur password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template("reset_token.html", title="reset password",form=form)
