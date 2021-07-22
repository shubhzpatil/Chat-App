from flask import Flask, render_template

from wt_forms import *
from models import *


app = Flask(__name__)
app.secret_key = 'replace'

app.config['SQLALCHEMY_DATABASE_URI'] = """postgresql://yhpysqkoarzser:725098228542cfd280492ff5c32905ba8c814561cd44a16be280caf34e1cb06a@ec2-54-224-194-214.compute-1.amazonaws.com:5432/dejdgbbeu8vv5r"""

db = SQLAlchemy(app)

@app.route("/", methods=['GET','POST'])
def index():

    register = RegistrationForm()
    
    if register.validate_on_submit():
        user1 = register.user_name.data
        pass1 = register.pass_word.data

        user_object = User.query.filter_by(usernm=user1).first()
        if user_object:
            return "Someone already taken this username!"

        user = User(usernm=user1,passw=pass1)
        db.session.add(user)
        db.session.commit()
        return "Inserted Into Database!"
        
    return render_template("index.html", form=register)
    
if __name__ == "__main__":
    app.run(debug=True)