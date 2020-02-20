import os

from flask import Flask, render_template
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, patch_request_class
from wtforms import SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard string'
app.config['UPLOAD_FOLDER'] = os.getcwd()

doc = UploadSet('doc', DOCUMENTS)
configure_uploads(app, doc)
patch_request_class(app)git


class UploadForm(Form):
    doc = FileField(validators=[
        FileAllowed(doc, u'只允许上传Excel文件！'),
        FileRequired(u'文件未选择！')
    ])
    submit = SubmitField(u'上传')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = doc.save(form.doc.data)
        file_url = doc.url(filename)
        file_path = doc.path()
    else:
        file_url = None
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()
