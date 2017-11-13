from flask import url_for, render_template, request, session, redirect
from app import app, db
from app.models import User, Message, Comment


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None:
            return render_template('logout.html', message='There is no user named %s' % request.form['username'])
        elif user.verify_password(request.form['password']):
            session['known'] = True
            session['username'] = user.username
            session['user_id'] = user.id
        return redirect(url_for('display'))
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    if session['known']:
        session['known'] = False
        username = session.pop('username', None)
        session.pop('user_id', None)
        message = username + ', you are logged out'
    else:
        message = 'Please log in first'
    return render_template('logout.html', message=message)


@app.route('/logon', methods=['GET', 'POST'])
def logon():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()
        return render_template('display.html')
    return render_template('logon.html')


@app.route('/display', methods=['GET', 'POST'])
def display():
    if request.method == 'GET':
        messages = Message.query.order_by(db.desc(Message.pub_date))
        if messages:
            tip = 'These is no message so far.'
        else:
            tip = None
        return render_template('display.html', messages=messages, tip=tip)
    return render_template('display.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    tip = ''
    if request.method == 'POST':
        try:
            title = request.form['title']
            text = request.form['text']
            user_id = session.get('user_id')
            message = Message(title, text, user_id)
            db.session.add(message)
            db.session.commit()
            tip = 'Add success'
        except KeyError:
            tip = 'Add failure'
        return redirect(url_for('display'))
    return render_template('add.html', tip=tip)


@app.route('/add_comment', methods=['POST', 'GET'])
def add_comment():
    user_id = session['user_id']
    mes_id = request.form['mes_id']
    text = request.form['comment']
    comment = Comment(mes_id, user_id, text)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('display'))


@app.route('/my_message', methods=['GET', 'POST'])
def my_message():
    if request.method == 'GET':
        user_id = session['user_id']
        messages = Message.query.filter_by(user_id=user_id).order_by(db.desc(Message.pub_date))
        return render_template('my_message.html', messages=messages)
    else:
        uid = request.form['id']
        message = Message.query.filter_by(id=uid).first()
        if message.comments:
            for comment in message.comments:
                db.session.delete(comment)
        db.session.delete(message)
        db.session.commit()
        return redirect(url_for('my_message'))


@app.route('/modify_password', methods=['POST', 'GET'])
def modify_password():
    if request.method == 'POST':
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        password = request.form['password']
        if user.verify_password(password=password):
            new_password = request.form['new_password']
            user.password(new_password)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('display'))
    return render_template('modify_password.html')


@app.route('/my_info', methods=['GET', 'POST'])
def my_info():
    pass



