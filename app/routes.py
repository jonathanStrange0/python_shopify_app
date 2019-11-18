from app import app
import shopify


@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'


@app.route('/shopify'):
def shopify():
    #TODO: When directed to this route, user should be prompted to
    # install the app on their store, or if already installed
    # they should be redirected to the callback function
    pass

@app.route('/shopify/callback')
def callback():
    # TODO: After install/auth return the homepage of the app
    # that will be embedded in the user's store.
    pass
