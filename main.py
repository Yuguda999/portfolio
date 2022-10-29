import smtplib, os
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///portfolio.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Port(db.Model):
    __tablename__ = 'portfolio'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.String(250))
    img_url = db.Column(db.String(250), unique=True)

if os.path.isfile('portfolio.db'):
    pass
else:
    with app.app_context():

        db.session.commit()
        db.create_all()


@app.route("/")
def home():
    all_project = Port.query.all()
    return render_template("index.html", projects=all_project)


@app.route("/ymsaddportfolio", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_port = Port(title=request.form["title"],
                        body=request.form["body"],
                        img_url=request.form["image-url"])
        db.session.add(new_port)
        db.session.commit()
    return render_template('add.html')
@app.route("/contact", methods=['GET','POST'])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"],data["message"])
    return redirect(url_for("home"))

def send_email(name, email, message):
    OWN_EMAIL = 'yms.pyth@gmail.com'
    OWN_PASSWORD = 'pdwjthtuonofcdfz'
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\n\nMessage:{message}"
    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        #connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail('MyBlog', OWN_EMAIL, email_message)

@app.route('/download')
def download_file():
    return  send_from_directory(directory='static',path='ymscv.pdf')

if __name__ == "__main__":
    app.run(debug=True)
