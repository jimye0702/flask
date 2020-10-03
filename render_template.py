# coding=utf-8

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.getcwd()
app = Flask(__name__)
Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'qweasd123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/user/<name>')
def user(name):
    mydict = {'Jim': 1, 'Dave':2}
    v = mydict[name]
    mylist = [2, 5, 3, 6, 8]
    return render_template('user.html', name=name, dict_v=v, list_v=mylist[v])

@app.route('/control_structures/<user>')    
def control_structures(user):
    return render_template('control.html', user=user)

@app.route('/for_loop')
def for_loop():
    comments = ['a', 'b', 'c', 'd', 'e']
    return render_template('for_loop.html', comments=comments)

@app.route('/block_example')
def block():
    return render_template('block_example.html')

@app.route('/bootstrap/<name>')
def bootstrap(name):
    return render_template('base_bootstrap.html', name=name)

@app.route('/momentjs/<name>')
def momentjs(name):
    return render_template('momentjs.html', name=name, current_time=datetime.utcnow())

@app.route('/wtform', methods=['GET', 'POST'])
def wtform():  #與 wtform_red 比較
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('flask_wtf.html', form=form, name=name)

@app.route('/wtform_red', methods=['GET', 'POST'])
def wtform_red():  #與 wtform 比較，重新整理頁面不跳詢問視窗
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('wtform_red'))
    return render_template('flask_wtf.html', form=form, name=session.get('name'))

@app.route('/wtform_flash', methods=['GET', 'POST'])
def wtform_flash():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name != None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('wtform_flash'))
    return render_template('wtf_flash.html', form=form, name=session.get('name'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error page.html')
    
if __name__ == '__main__':
    app.run()