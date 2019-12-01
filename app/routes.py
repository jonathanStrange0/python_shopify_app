from app import app
import shopify as sfy
from flask import session, redirect, url_for, request, current_app, render_template
from app.decorators import shopify_auth_required
from dotenv import load_dotenv
import os, requests
from pprint import pprint

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
        scope = ["write_products", "read_products",\
                    'read_orders','write_orders',\
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
    #TODO: Perform security checks

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
    print('Token: ', token)
    # return('generated a shopify access token, now let\'s do something with it')
    shop_session = sfy.Session(shop_url, '2019-04', token)
    # TODO: After install/auth return the homepage of the app
    # that will be embedded in the user's store.
    # make a shop request:
    sfy.ShopifyResource.activate_session(shop_session)
    shop = sfy.Shop.current()
    # return(shop)
    client = sfy.GraphQL()
    query = '''
        {
          shop {
            name
            id
          }
        }
      '''
    # result = client.execute(query)
    # return render_template('index.html', result=result)
    shopRequestURL = 'https://' + request.args.get('shop') +'/admin/api/2019-04/products.json'
    shopRequestHeaders = {'X-Shopify-Access-Token' : token}
    return(requests.get(shopRequestURL,headers=shopRequestHeaders).json())
    # return('Successfully redirected')
# query = '''{shop {name id}}'''
