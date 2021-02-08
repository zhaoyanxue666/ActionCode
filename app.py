from flask import *  # Flask, render_template, url_for, request,check_password_hash
from forms import *
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, login_user
from models import *

import os.path

app = Flask(__name__)
app.config["SECRET_KEY"] = b'_5#y2L"Ffgjfgjh4Q8z\n\xec]/'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
bootstrap = Bootstrap(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route("/", methods=["GET", "POST"])
def hello():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if not os.path.exists("test.db"):
        db.create_all()
        admin = User('admin','123456')
        db.session.add(admin)
        db.session.commit()
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", form=form)

    elif request.method == "POST" and form.validate_on_submit():
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for("index"))
        else:
            return render_template("login.html", form=form, error="登录失败")


@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    show_data = cop_sqplit(db).get_data()
    # 小的在上，大的在下，负数在最后
    show_data.sort(
        key=lambda x: (int(x[1]) if int(x[1]) >= 0 else int(x[1]) + 99999999999)
    )
    return render_template("index.html", data=show_data)


@app.route("/add_code", methods=["GET", "POST"])
@login_required
def add_code():
    form = AddForm()
    form.code.validators = [
        DataRequired(),
        NoneOf(cop_sqplit(db).get_ex_code(), message="许可码已存在"),
    ]

    if request.method == "GET":
        return render_template("add.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            cop_sqplit(db).add_data(form)
            return redirect(url_for("index"))
        else:
            return render_template("add.html", form=form)


@app.route("/delete_code/<int:id>", methods=["GET", "POST"])
@login_required
def delete_code(id):
    cop_sqplit(db).delete_data(id)
    return redirect(url_for("index"))


@app.route("/change_code/<id>", methods=["GET", "POST"])
@login_required
def change_code(id):
    form = ChangeTime()
    if request.method == "GET":
        data = cop_sqplit(db).get_data(id=id)[0]
        form = ChangeTime(
            id=data[0],
            code=data[1],
            rest_time=data[2],
            add_time=0,
            start_time=data[4],
            end_time=data[5],
            remarks=data[6],
        )
        return render_template("change.html", form=form)
    elif request.method == "POST" and form.validate_on_submit():
        cop_sqplit(db).change_code(form.id.data, form.add_time.data)
        return redirect(url_for("index"))


@app.route("/search", methods=["POST"])
def search_code():
    code = request.form["code"]
    mac = request.form["mac"]
    da = cop_sqplit(db).set_mac_check_time(code, mac)
    return da


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
