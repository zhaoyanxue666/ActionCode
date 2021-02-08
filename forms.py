from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, AnyOf, NoneOf
from models import *
from flask_sqlalchemy import SQLAlchemy


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('登录')


class AddForm(FlaskForm):
    code = StringField('授权码', validators=[])
    keep_time = StringField('有效时间', validators=[DataRequired()])
    remarks = StringField('备注')
    submit = SubmitField('添加')


class ChangeTime(FlaskForm):
    id = StringField('***不要修改***id')
    code = StringField('***不要修改***授权码')
    rest_time = StringField('***不要修改***剩余时间')
    add_time = StringField('请在此处填写要增加的时间', validators=[DataRequired()])
    start_time = StringField('***不要修改***起始时间')
    end_time = StringField('***不要修改***结束时间')
    remarks = StringField('备注')
    submit = SubmitField('更改')
