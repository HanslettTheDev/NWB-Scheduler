from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, length

class MonthSelector(FlaskForm):
    category = SelectField(u"Select A Month", validators=[DataRequired()], choices=[('January'), 
        ('February'), ('March'), ('April'),('May'), ('June'), ('July'), ('August'), ('September'), ('October'), ('November'), ('December')])
    submit = SubmitField('Next')