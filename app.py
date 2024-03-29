import os.path
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'blog.db')

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    pr = db.relationship('Profiles', backref='Users', uselist=False, lazy="subquery")

    def __repr__(self):
        return f"<users {self.id}>"


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"


@app.route("/")
def index():
    try:
        info = Users.query.all()
    except:
        print("Ошибка чтения")
    return render_template("index.html", title='Главная', info=info)


@app.route("/register",  methods=["POST", "GET"])
def register():
    if request.method == "POST":
        try:
            hash = generate_password_hash(request.form['psw'])
            u = Users(email=request.form['email'], psw=hash)
            db.session.add(u)
            db.session.flush()

            p = Profiles(name=request.form["name"], old=request.form['old'],
                         city=request.form["city"], user_id=u.id)
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
            flash("Ошибка добавления в БД", category="error")
    return render_template("register.html", title='Регистрация')


if __name__ == '__main__':
    app.run(debug=True)
