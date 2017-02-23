from flask_wtf import Form
from wtforms.fields import TextAreaField
from wtforms.validators import DataRequired


class LookupForm(Form):
    domain_list = TextAreaField("Enter domain's list", validators=[DataRequired()])