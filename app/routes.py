from app import app
import shopify as sfy
from flask import session, redirect, url_for, request, current_app
from app.decorators import shopify_auth_required
from dotenv import load_dotenv
import os


@app.route('/')
@app.route('/index')
# @shopify_auth_required
def index():
    return 'Hello World'

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
        scope = ["write_products", "read_products"] #may add more later

        #Generate the permissions url:
        permission_url = shop_session.create_permission_url(scope, url_for('callback', _external=True))
        print('Permission URL: ', permission_url)
        #TODO: Fix this redirect, it don't work yo.
        return(redirect(permission_url))
    else:
        return 'Missing shop parameter. Please add ?shop=your-development-shop.myshopify.com to your request'


@app.route('/shopify/callback')
def callback():
    # TODO: After install/auth return the homepage of the app
    # that will be embedded in the user's store.
    return('Successfully redirected')
    # pass
