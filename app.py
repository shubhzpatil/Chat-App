from flask import Flask, render_template, redirect, url_for


from wt_forms import *
from models import *


app = Flask(__name__)
app.secret_key = 'replace'

app.config['SQLALCHEMY_DATABASE_URI'] = """postgresql://yhpysqkoarzser:725098228542cfd280492ff5c32905ba8c814561cd44a16be280caf34e1cb06a@ec2-54-224-194-214.compute-1.amazonaws.com:5432/dejdgbbeu8vv5r"""

db = SQLAlchemy(app)

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
        return redirect(url_for('login'))
        
    return render_template("index.html", form=register)

@app.route("/login", methods=['GET','POST'])
def login():

    login_form = LoginForm()

    #this allow user to login
    if login_form.validate_on_submit():
        return "Login successfully..."

    return render_template("login.html", form=login_form)


if __name__ == "__main__":
    app.run(debug=True)