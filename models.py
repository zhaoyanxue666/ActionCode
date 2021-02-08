from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)

    def __init__(self, username, password):  # 最好从数据库获取，或使用加密方式获取，这里只简单示例
        self.username = username
        self.password = password


class Code_list(db.Model):
    __tablename__ = "code_list"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50))
    rest_time = db.Column(db.String(30))
    keep_time = db.Column(db.String(30))
    start_time = db.Column(db.String(30))
    end_time = db.Column(db.String(30))
    remarks = db.Column(db.String(100))
    mac = db.Column(db.String(30))

    def __init__(self, code, keep_time, remarks):
        self.code = code
        self.rest_time = int(keep_time)  # 只是创建时候这么写
        self.keep_time = int(keep_time)
        now_time = datetime.datetime.now()
        self.start_time = now_time.strftime("%Y-%m-%d %H:%M")
        self.end_time = (now_time + datetime.timedelta(days=self.keep_time)).strftime(
            "%Y-%m-%d %H:%M"
        )
        self.remarks = remarks
        self.mac = ""


class cop_sqplit:
    def __init__(self, db):
        self.db = db

    def add_data(self, form):
        data = Code_list(
            form.code.data,
            form.keep_time.data,
            form.remarks.data,
        )
        self.db.session.add(data)
        self.db.session.commit()

    def sub_now_time(self, t1):
        t1_t = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M")
        now_time = datetime.datetime.now()
        return (t1_t - now_time).days

    def up_time(self):
        data = Code_list.query.all()
        for da in data:
            da.rest_time = self.sub_now_time(da.end_time)
        self.db.session.commit()

    def get_data(self, id=""):
        self.up_time()
        fil = self.db.session.query(
            Code_list.id,
            Code_list.code,
            Code_list.rest_time,
            Code_list.keep_time,
            Code_list.start_time,
            Code_list.end_time,
            Code_list.remarks,
            Code_list.mac,
        )
        if id == "":
            data = fil.filter().all()
        else:
            data = fil.filter(Code_list.id == id).all()
        return data

    def delete_data(self, id):
        u = Code_list.query.get(id)
        self.db.session.delete(u)
        self.db.session.commit()

    def change_code(self, id, t):
        u = Code_list.query.get(id)
        t1 = int(u.keep_time) + int(t)
        u.keep_time = t1
        u.end_time = (
            datetime.datetime.strptime(u.end_time, "%Y-%m-%d %H:%M")
            + datetime.timedelta(days=t1)
        ).strftime("%Y-%m-%d %H:%M")
        self.db.session.commit()

    def get_ex_code(self):
        data = Code_list.query.with_entities(Code_list.code)
        return [_[0] for _ in data]

    def set_mac_check_time(self, code, mac):
        data = Code_list.query.filter(Code_list.code == code).first()
        if data.mac == "":
            data.mac = mac
            self.db.session.commit()

        if data.mac != "" and data.mac != mac:
            return {"code": 0, "message": "不在注册电脑使用"}

        if datetime.datetime.now() > datetime.datetime.strptime(
            data.end_time, "%Y-%m-%d %H:%M"
        ):  # now>end_time
            return {"code": 0, "message": "不在许可时间", "截止时间": data.end_time}

        return {
            "code": 1,
            "许可码": data.code,
            "剩余时间(天)": data.rest_time,
            "截止时间": data.end_time,
        }
