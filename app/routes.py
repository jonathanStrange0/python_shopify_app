from app import app
import shopify
from flask import session, redirect, url_for, request, current_app


@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'


@app.route('/shopify')
def shopify():
    #TODO: When directed to this route, user should be prompted to
    # install the app on their store, or if already installed
    # they should be redirected to the callback function

    #get the shop name from the request kwargs
    shop_url = request.args.get('shop')
    if shop_url:
        # setup a shopify session
        shopify.Session.setup(
            api_key=current_app.config['SHOPIFY_API_KEY'],
            secret=['SHOPIFY_SHARED_SECRET']
        )

        #Create a shopify session instance with api version and url for shop
        shop_session = shopify.Session(shop_url, '2019-04')

        #Define the access scopes the app would like to have
        scope = ["write_products", "read_products"] #may add more later

        #Generate the permissions url:
        permission_url = shop_session.create_permission_url(scope)
        return(redirect(permission_url))
    else:
        return 'Missing shop parameter. Please add ?shop=your-development-shop.myshopify.com to your request'
    

@app.route('/shopify/callback')
def callback():
    # TODO: After install/auth return the homepage of the app
    # that will be embedded in the user's store.
    pass
