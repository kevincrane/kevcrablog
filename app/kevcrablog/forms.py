from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms import validators
from wtforms.widgets import TextArea, HTMLString


class MarkdownWidget(TextArea):
    """ Replacement TextArea for blog Markdown
        - When typing, text is converted to markdown and displayed in
          HTML div 'markdown-preview'
    """

    def __call__(self, field, **kwargs):
        html = super(MarkdownWidget, self).__call__(field, id='markdown-input', **kwargs)
        return HTMLString(html)


class PostForm(Form):
    """ Form for new blog Post object
    """
    title = TextField(u'Post Title', validators=[validators.InputRequired("Please enter a good title.")])
    body = TextAreaField(u'Content', validators=[validators.InputRequired("This would be the worst blog post.")],
                         widget=MarkdownWidget())


class CommentForm(Form):
    """ Form for a Comment on a blog Post
    """
    body = TextAreaField(u'Comment', validators=[validators.InputRequired("Say something at least.")])
    author = TextField(u'Name', validators=[validators.InputRequired("Don't be scared, what's your name?")])