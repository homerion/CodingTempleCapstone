from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Entries, Tags, tag_map
from werkzeug.urls import url_parse



@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@login_required
def index():
    uTags = Tags.query.join(Entries.tags).filter(Entries.user_id==current_user.id).all()
    if request.method == "POST":
        e = Entries.query.filter_by(user_id=current_user.id,text=request.form['entry']).first()
        t = Tags.query.filter_by(tag=request.form['tag']).first()
        if e is None:
            e = Entries(user_id=current_user.id,text=request.form['entry'])
        if t is None:
            t = Tags(tag=request.form['tag'])
        e.tags.append(t)
        db.session.add(e)
        db.session.commit()
    list = Entries.query.filter_by(user_id=current_user.id).all()
    return render_template('list.html',list=list)

@app.route('/new')
@login_required
def new_list():
    if request.method == "POST":
        e = Entries.query.filter_by(user_id=current_user.id,text=request.form['entry']).first()
        t = Tags.query.filter_by(tag=request.form['tag']).first()
        if t is None:
            t = Tags(tag=request.form['tag'])
            db.session.add(t)
        if e is None:
            e = Entries(user_id=current_user.id,text=request.form['entry'])
            e.tags.append(t)
            db.session.add(e)
        db.session.commit()
    list=Entries.query.filter_by(user_id=current_user.id).all()
    return render_template('list.html',list=list)


@app.route('/t/<tag>')
@login_required
def tag_list(tag):
    list=Entries.query.join(Tags.entries).filter(Entries.user_id==current_user.id).filter(Tags.tag==tag).all()
    if list is None:
        return redirect(url_for('new_list'))
    return render_template('list.html',list=list)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first() or User.query.filter_by(username=login_form.email.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid login credentials')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # flash('Thanks for loggin in {}!'.format(current_user.email))
        return redirect(next_page)
    return render_template('form.html',form=login_form, title="Login")



@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = User(username=register_form.username.data,email=register_form.email.data)
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))

    return render_template('form.html',form=register_form, title="Register")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
