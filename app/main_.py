import os

from flask import Flask, render_template, flash, make_response, send_file, redirect, session, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired
from APIToJSON import JsonCreator
from JsonToCal import ical_creat

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'a hard string you never guess'


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
        session['user'] = user
        password = form.password.data
        jsoncreator = JsonCreator(user, password)
        if jsoncreator.stu.isLogin:
            jsoncreator.creatJson()
            ical_creat(user)
            flash('ics文件生成成功')
            return redirect(url_for('downloadicsfile'))
        else:
            flash('帐号密码有误，请重试')
            form.user.data = session.get('user')
            return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/downloadicsfile', methods=['GET', 'POST'])
def downloadicsfile():
    filename = session.get('user')
    response = make_response(send_file(os.path.abspath('cache/ics/' + filename + '.ics')))
    response.headers["Content-Disposition"] = "attachment; filename=CourseTable-2019-2020-2.ics;"
    return response

