from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

class CustomerForm(FlaskForm):
    number_of_customers_field = IntegerField(label='Number of Customers', validators=[DataRequired()])
    submit_button = SubmitField(label='Generate Synthetic Customer Data')

class ProductForm(FlaskForm):
    number_of_products_field = IntegerField(label='Number of Products', validators=[DataRequired()])
    submit_button = SubmitField(label='Generate Synthetic Product Data')

class OrderForm(FlaskForm):
    number_of_orders_field = IntegerField(label='Number of Orders', validators=[DataRequired()])
    number_of_line_items_field = IntegerField(label='Max Number of Line Items Per Order', validators=[DataRequired()])
    max_qty_sold_field = IntegerField(label='Max Number of Items Sold on Each Line Item', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit_button = SubmitField(label='Generate Synthetic Order Data')
