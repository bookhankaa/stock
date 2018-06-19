from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from flask import request
from werkzeug.urls import url_parse

from stock_app import app
from stock_app import db
from stock_app.forms import LoginForm, SignupForm
from stock_app.models import User


@app.route('/')
@login_required
def index():
    return render_template('home.html')


@app.route('/populate')
@login_required
def populate():
    from stock_app.models import Item
    import random, string
    from uuid import uuid4

    item = Item(
        vendor_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
        uuid = str(uuid4()),
        price = 1,
        amount = 2
    )
    db.session.add(item)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/apidoc')
@login_required
def apidoc():
    return render_template('api.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        if not User.query.filter_by(username=username).first():
            password = form.password.data
            user =  User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        else:
            flash('Username already exist')
            return redirect(url_for('signup'))
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
