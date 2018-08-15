from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Entries, Tags, tag_map
from werkzeug.urls import url_parse


#will produce every list for every tag
@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@login_required
def index():
    info=request.form
    if request.method == "POST":
        if 'entry' in info:
            e = Entries.query.filter_by(user_id=current_user.id,text=request.form['entry']).first()
            t = Tags.query.filter_by(tag=request.form['tag']).first()
            if e is None:
                e = Entries(user_id=current_user.id,text=request.form['entry'])
            if t is None:
                t = Tags(tag=request.form['tag'])
            e.tags.append(t)
            db.session.add(e)
        db.session.commit()
    uTags = Tags.query.join(Entries.tags).filter(Entries.user_id==current_user.id).all()
    entryList = Entries.query.join(Tags.entries).filter_by(user_id=current_user.id)
    listsByTag = {}
    for t in uTags:
        listsByTag[t.tag]=entryList.filter(Tags.tag==t.tag).all()
    return render_template('index.html',list=listsByTag)

#gets rid of a list from a user
# @app.route('/removetag',methods=['POST'])
# def removetag():
#     #done is a special function for the user loader
#     info = request.form['tag_id']
#     relations = db.session.query(tag_map).filter(tag_map.c.entry_id==info[1],tag_map.c.tag_id==tag.id)
#     db.session.delete(entry)
#     db.session.commit()
#     return str(info)

#gets rid of an entry from the db
@app.route('/done',methods=['POST'])
def did():
    #done is a special function for the user loader so have to call the function did
    info = request.form['entry_id']
    entry = Entries.query.get(info)
    db.session.delete(entry)
    db.session.commit()
    return str(info)

#gets rid of an association between a tag and an entry
@app.route('/decouple',methods=['POST'])
def decouple():
    info = request.form['joined_id']
    # the split returns the tag key (a string) and the entry id (int)
    info = str(info).split('ent')
    tag = Tags.query.filter_by(tag=info[0]).first()
    info = db.session.query(tag_map).filter(tag_map.c.entry_id==info[1],tag_map.c.tag_id==tag.id)
    info.delete(synchronize_session=False)
    db.session.commit()
    return str('done!')

#adds a new entry to the db and associates it to the tag it was made in
@app.route('/newentry',methods=['POST'])
def new_entry():
    e = Entries.query.filter_by(user_id=current_user.id,text=request.form['entry']).first()
    t = Tags.query.filter_by(tag=request.form['tag']).first()
    if e is None:
        e = Entries(user_id=current_user.id,text=request.form['entry'])
    if t is None:
        t = Tags(tag=request.form['tag'])
    e.tags.append(t)
    db.session.add(e)
    db.session.commit()
    id = Entries.query.filter_by(user_id=current_user.id,text=request.form['entry']).first().id
    return str(id)

#a new list for a yet unspecified tag
@app.route('/new', methods=['GET','POST'])
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
    return render_template('new.html')


#produces a list of entries with this tag
@app.route('/t/<tag>', methods=['GET','POST'])
@login_required
def tag_list(tag):
    t = Tags.query.filter_by(tag=tag).first()
    if t is None:
        return redirect(url_for('new_list'))
    if request.method == "POST":
        e = Entries.query.filter_by(user_id=current_user.id,text=request.form['entry']).first()
        if e is None:
            e = Entries(user_id=current_user.id,text=request.form['entry'])
        e.tags.append(t)
        db.session.add(e)
        db.session.commit()
    list=Entries.query.join(Tags.entries).filter(Entries.user_id==current_user.id,Tags.tag==tag).all()
    return render_template('list.html',list=list,head=tag)

# every tag listed out as links to the tag_list page
@app.route('/tags', methods=['GET','POST'])
@login_required
def tags():
    list=Tags.query.join(Entries.tags).filter(Entries.user_id==current_user.id,Tags.tag!='').all()
    return render_template('tags.html',list=list)


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
