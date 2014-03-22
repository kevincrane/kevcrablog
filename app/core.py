""" :core.py
    Contains core objects that are used
    throughout the application
"""
import re

from flask.ext.sqlalchemy import SQLAlchemy

# SQLAlchemy instance
db = SQLAlchemy()

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, prefix=None, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    if prefix:
        result.append(prefix)
    for word in _punct_re.split(text.lower()):
        word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))
