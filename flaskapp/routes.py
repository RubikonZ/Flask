from flask import Flask, render_template, flash, redirect, url_for, request
from flaskapp.forms import RegistrationForm, LoginForm
from flaskapp.models import User, Post
from flaskapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='ZDAROVA')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f"You are already logged in", 'success')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # crypted password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"You successfully logged in", 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash(f"Wrong login information", 'danger')
    return render_template('login.html', titler='Login', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    else:
        flash(f"You aren't logged in", 'danger')
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', titler='Account')
