from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import render_template, request, flash, redirect
from os import path
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "this is the secret key for my page"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)

class Username(db.Model, UserMixin):
    username_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))


with app.app_context():
    db.create_all()


 
@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        check_username = Username.query.filter_by(username=username).first()

        if check_username:
            flash("This username already exists in the database!", category="error")

        elif len(username) < 5:
            flash("Username must have at least 5 characters.", category="error")

        elif password != confirmation:
            flash("The passwords do not match! Be sure you typed the same password.", category="error")

        elif len(password) < 6:
            flash("The password should have at least 6 characters, for more security on your account.", category="error")

        else:
            # add user to the database
            new_username = Username(username=username, password=generate_password_hash(password))
            db.session.add(new_username)
            db.session.commit()
            flash("Account created successfully!", category="success")
            
            return redirect("/login")
            

    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print(f"Attempting to log in with username: {username}")
        user = Username.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
            else:
                flash("Incorrect password, please try again.", category="error")
        else:
            flash("Username does not exist, make sure you registered the user first.", category="error")

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)