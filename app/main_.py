import os

from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired
from APIToJSON import JsonCreator
from JsonToCal import ical_creat

app = Flask(__name__)
app.config['SECRET_KEY'] = 'windgiang'


class LoginForm(FlaskForm):
    user = StringField(
        label='学号',
        validators=[DataRequired()]
    )
    password = PasswordField(
        label='密码',
        validators=[DataRequired()]

    )
    submit = SubmitField(
        label='导出'
    )


@app.route('/', methods=['GET', 'POST'])
def main_app():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
        coursejson = JsonCreator(user, password)
        if coursejson.stu.isLogin:
            coursejson.creatJson()
            flash('json解析成功，正在导出ICS文件，请等待')
            response = ical_creat(user)
            flash('ics文件生成成功')
            return response
        else:
            flash('帐号密码有误，请重试')
    return render_template('index.html', form=form)


@app.route('/downloadicsfile/<filename>', methods=['GET', 'POST'])
def ics_file(filename):
    return 'hello ,'+filename+' no exist'

