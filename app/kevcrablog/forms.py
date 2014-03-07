from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms import validators


class PostForm(Form):
    title = TextField(u'Post Title', validators=[validators.InputRequired("Please enter a good title.")])
    body = TextAreaField(u'Content', validators=[validators.InputRequired("This would be the worst blog post.")])
    #TODO: sizing?
    #TODO: add to kevcrablog.models also
