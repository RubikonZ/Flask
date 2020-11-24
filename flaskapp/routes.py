from flask import Flask, render_template, flash, redirect, url_for
from flaskapp.forms import RegistrationForm, LoginForm
from flaskapp.models import User, Post
from flaskapp import app

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 'success' and 'danger' are built-in bootstrap classes
        if form.email.data == 'admin@blog.com' and form.password.data == 'qwe':
            flash(f"Successfully logged in as {form.email.data}", 'success')
            return redirect(url_for('home'))
        else:
            flash(f"Wrong login information", 'danger')
    return render_template('login.html', titler='Login', form=form)