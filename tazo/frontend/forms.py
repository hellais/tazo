from flask.ext.wtf import Form
from wtforms import (StringField, TextAreaField,
                     FieldList, FormField,
                     SelectField, SubmitField,
                     ValidationError, HiddenField, BooleanField)
from wtforms.validators import DataRequired, Length, EqualTo, Email

from ..config import category_codes, country_codes

class URLForm(Form):
    url = StringField("URL", validators=[DataRequired()])
    category = SelectField("Category for the URL",
                           choices=map(lambda x: (x[0], x[1][0]),
                                       category_codes.items()))
    notes = StringField("Notes")

class NewURLForm(Form):
    urls = TextAreaField(u"URLs of websites", [DataRequired()])
    contributor = StringField(u"Your name", [DataRequired()])
    submit = SubmitField(u"Add")


class CategorizeURLSForm(Form):
    urls = FieldList(FormField(URLForm))
    contributor = HiddenField()
    country = HiddenField()
    submit = SubmitField(u"Add")
