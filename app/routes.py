# -*- coding: utf-8 -*-
import sqlite3
from hashlib import md5
from flask import render_template
from app import app, database
from flask import flash, redirect
from flask import url_for
from flask import request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app.database import conn
from app.forms import LoginForm2
from app.models import dd

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')
# ------------------------------------------------------------------------------------------------
@app.route('/register2', methods=['GET', 'POST'])
def register2():
    if current_user.is_authenticated:
        flash('Вы уже вошли в ученую запись!')
        return redirect('index')
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hpassword = (md5(password.encode())).hexdigest()
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif conn.execute(
                'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
            flash('данные используются')
        if error is None:
            conn.execute('insert into users (username, password) values (?,?);', (
            username, hpassword))
            conn.commit()
            return redirect('index')
    return render_template('register2.html')

@app.route('/login2', methods=['GET', 'POST'])
def login2():
    error = None
    form = LoginForm2(request.form)
    if form.validate_on_submit():
        hpassword = (md5(form.password.data.encode())).hexdigest()
        database.db.execute('SELECT * FROM users WHERE username = ?', (form.username.data,))
        passed = database.db.fetchone()
        if passed == None:
            flash('Invalid username_изнон')
            return redirect(url_for('login2'))
            error = 'Incorrect username.'
        elif passed[2] != hpassword:
            error = 'Incorrect password.'
        elif passed[2] == hpassword:
            user0 = dd()
            user0.id = passed[0]
            user0.name = form.username.data
            login_user(user0, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login2.html', title='ВХОд2', error=error, form=form)  # error=error

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/no/')
@login_required
def no():
    return render_template('no.html')
