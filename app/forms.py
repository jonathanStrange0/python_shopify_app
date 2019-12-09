from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

class FakeDataForm(FlaskForm):
    number_of_customers_field = IntegerField(label='Number of Customers', validators=[DataRequired()])
    number_of_products_field = IntegerField(label='Number of Products', validators=[DataRequired()])
    # number_of_customers_field = IntegerField(label='Number of Customers')
    submit_button = SubmitField(label='Generate Synthetic Data')
