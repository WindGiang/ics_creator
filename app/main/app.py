from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired

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
        label='登陆'
    )


@app.route('/', methods=['GET', 'POST'])
def main_app():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
    else:
        return render_template('index.html', form=form)


@app.route('/icsfile', methods=['GET', 'POST'])
def ics_file():
    return render_template('icsfile.html')


if __name__ == '__main__':
    app.run()
