from flask import Flask, render_template

from wt_forms import *

app = Flask(__name__)
app.secret_key = 'replace'

@app.route("/", methods=['GET','POST'])
def index():

    register = RegistrationForm()
    
    if register.validate_on_submit():
        return "Success..."
        
    return render_template("index.html", form=register)
    
if __name__ == "__main__":
    app.run(debug=True)