from flask import Flask, render_template, redirect, url_for, flash
from werkzeug import debug
from time import localtime, strftime
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, rooms, send, emit, join_room, leave_room

from wt_forms import *
from models import *


app = Flask(__name__)
app.secret_key = 'replace'

app.config['SQLALCHEMY_DATABASE_URI'] = """postgresql://yhpysqkoarzser:725098228542cfd280492ff5c32905ba8c814561cd44a16be280caf34e1cb06a@ec2-54-224-194-214.compute-1.amazonaws.com:5432/dejdgbbeu8vv5r"""

db = SQLAlchemy(app)

socketio = SocketIO(app)
ROOMS = ["Team 1","Team 2","Team 3"]

login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):

    return User.query.get(int(id))

@app.route("/", methods=['GET','POST'])
def index():

    register = RegistrationForm()

    #this will update the database if user register successfully
    if register.validate_on_submit():
        user1 = register.user_name.data
        pass1 = register.pass_word.data

        hashed_pass = pbkdf2_sha256.hash(pass1)

        #adding user to database
        user = User(usernm=user1,passw=hashed_pass)
        db.session.add(user)
        db.session.commit()

        flash('You are Registered Successfully..!Please Login.')
        return redirect(url_for('login'))
        
    return render_template("index.html", form=register)

@app.route("/login", methods=['GET','POST'])
def login():

    login_form = LoginForm()

    #this allow user to login
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(usernm=login_form.user_name.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)

@app.route("/chat",methods=['GET','POST'])
def chat():
    if not current_user.is_authenticated:
        flash('Please Login.')
        return redirect(url_for('login'))
    return render_template('chat.html', username=current_user.usernm, rooms=ROOMS)


@app.route("/logout",methods=['GET'])
def logout():

    logout_user()
    flash('You have Logged out Successfully')
    return redirect(url_for('login'))


@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    send({'msg': data['msg'], 'username': data['username'],'time_stamp': strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])
    

@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg': data['username'] + " has joined the " + data['room'] + "chat."}, room=data['room'])

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + " has left the " + data['room'] + "chat."}, room=data['room'])


if __name__ == "__main__":
    socketio.run(app, debug=True)