from app import app
import shopify as sfy
from flask import session, redirect, url_for, request, current_app, render_template, jsonify
from app.decorators import shopify_auth_required
from dotenv import load_dotenv
import os, requests, json
from pprint import pprint
from datetime import datetime
from app.customers import generate_fake_customer_data, upload_all_customers, upload_customer_data, delete_customer
from app.products import upload_product_data, generate_fake_variant, create_fake_products_and_variants, delete_products
from app.orders import generate_orders
from app.forms import CustomerForm, ProductForm, OrderForm
from app.models import Customer, Product
from flask_nav.elements import Navbar, View
from app import nav

nav.register_element('fake_data', Navbar(
    View('Home', '.index'),
    View('Customers', '.customers'),
    View('Products', '.products'),
    View('Orders', '.orders'),
))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    shop_session = sfy.Session(session['shop_url'], '2019-04', session['token'])
    # activate the shopify session to use resources.
    # sfy.ShopifyResource.activate_session(shop_session)
    # form = FakeDataForm()
    # if request.method == 'POST':
    #     if form.validate_on_submit():
    #         generate_fake_customer_data(form.number_of_customers_field.data)
    #         create_fake_products_and_variants(form.number_of_products_field.data, 5)
    #
    return render_template('index.html')


@shopify_auth_required
@app.route('/shopify')
def shopify():
    load_dotenv()
    #TODO: When directed to this route, user should be prompted to
    # install the app on their store, or if already installed
    # they should be redirected to the callback function

    #get the shop name from the request args
    shop_url = request.args.get('shop')
    print('shop_url: ', shop_url)
    if shop_url:
        # setup a shopify session
        sfy.Session.setup(
            api_key=os.getenv('SHOPIFY_API_KEY'),
            secret=os.getenv('SHOPIFY_SHARED_SECRET')
        )
        #Create a shopify session instance with api version and url for shop
        shop_session = sfy.Session(shop_url, '2019-04')
        print('shopify session: ', shop_session)

        #Define the access scopes the app would like to have
        scope = ["write_products", "read_products",\
                    'read_orders','write_orders',\
                    'write_draft_orders', 'read_draft_orders', \
                     'write_customers','read_customers'] #may add more later

        #Generate the permissions url:
        permission_url = shop_session.create_permission_url(scope, url_for('callback', _external=True, _scheme='https'))
        print("callback url: ", url_for('callback', _external=True, _scheme='https'))
        print('Permission URL: ', permission_url)
        #TODO: Fix this redirect, it don't work yo.
        return(redirect(permission_url))
    else:
        return 'Missing shop parameter. Please add ?shop=your-development-shop.myshopify.com to your request'


@app.route('/callback')
def callback():
    #setup new shopify session:
    shop_url = request.args.get('shop')
    sfy.Session.setup(
        api_key=os.getenv('SHOPIFY_API_KEY'),
        secret=os.getenv('SHOPIFY_SHARED_SECRET')
    )
    #Create a shopify session instance with api version and url for shop
    shop_session = sfy.Session(shop_url, '2019-04')

    # Get access Token
    token = shop_session.request_token(request.args)
    #adding the shop_url and token to the flask session for future great ideas
    session['token'] = token
    session['shop_url'] = shop_url
    # Get a session specific to this shop and using its token
    shop_session = sfy.Session(shop_url, '2019-04', token)
    # activate the sesstion (not necessary until we're going to do something with a resource)
    # sfy.ShopifyResource.activate_session(shop_session)

    # send user to home page
    return(redirect(url_for('index')))

#####################################################
###### Create fake data in the following methods ####
#####################################################

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    form = CustomerForm()
    shop_session = sfy.Session(session['shop_url'], '2019-04', session['token'])
    # activate the shopify session to use resources.
    sfy.ShopifyResource.activate_session(shop_session)
    if request.method == 'POST':
        if form.validate_on_submit():
            generate_fake_customer_data(form.number_of_customers_field.data)
            # create_fake_products_and_variants(form.number_of_products_field.data, 5)

    return render_template('customers.html', form=form)

@app.route('/products', methods=['GET', 'POST'])
def products():
    form = ProductForm()
    shop_session = sfy.Session(session['shop_url'], '2019-04', session['token'])
    # activate the shopify session to use resources.
    sfy.ShopifyResource.activate_session(shop_session)
    if request.method == 'POST':
        if form.validate_on_submit():
            # generate_fake_customer_data(form.number_of_customers_field.data)
            create_fake_products_and_variants(form.number_of_products_field.data, 5)

    return render_template('products.html', form=form)

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    form = OrderForm()
    shop_session = sfy.Session(session['shop_url'], '2019-04', session['token'])
    # activate the shopify session to use resources.
    sfy.ShopifyResource.activate_session(shop_session)
    if request.method == 'POST':
        if form.validate_on_submit():
                generate_orders(form.number_of_orders_field.data,\
                                form.number_of_line_items_field.data,\
                                form.max_qty_sold_field.data,\
                                form.start_date.data,\
                                form.end_date.data,\
                                session['shop_url'],\
                                session['token'])

    return render_template('orders.html', form=form)

#####################################################
###### Delete fake data in the following methods ####
#####################################################

@app.route('/_delete_customers')
def _delete_customers():
    shop_session = sfy.Session(session['shop_url'], '2019-04', session['token'])
    # activate the shopify session to use resources.
    sfy.ShopifyResource.activate_session(shop_session)
    customers = Customer.query.all()
    for c in customers:
        delete_customer(c.gid)
    return(jsonify('ok')) #this makes the browser happy on the final call, no 500 error

@app.route('/_delete_products')
def _delete_products():
    shop_session = sfy.Session(session['shop_url'], '2019-04', session['token'])
    # activate the shopify session to use resources.
    sfy.ShopifyResource.activate_session(shop_session)
    products = Product.query.all()
    for p in products:
        delete_products(p.gid)
    return(jsonify('ok')) #this makes the browser happy on the final call, no 500 error
id
@app.route('/_create_order')
def _create_order():
    shop_session = sfy.Session(session['shop_url'], '2019-04', session['token'])
    # activate the shopify session to use resources.
    sfy.ShopifyResource.activate_session(shop_session)
    generate_orders(1, 1, 10, start_date=datetime(2015,1,1), end_date=datetime.today())
    return(jsonify('ok')) #this makes the browser happy on the final call, no 500 error

from app.get_orders import get_orders
@app.route('/_get_order')
def _get_order():
    shop_session = sfy.Session(session['shop_url'], '2019-04', session['token'])
    # activate the shopify session to use resources.
    sfy.ShopifyResource.activate_session(shop_session)
    return jsonify(get_orders())
