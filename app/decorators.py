from functools import wraps
import shopify, os
from flask import session, redirect, url_for, request, current_app
from dotenv import load_dotenv



def shopify_auth_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        load_dotenv()
        #TODO add authorization code here
        if 'shopify_token' not in session:
            shop_url = request.args.get('shop')
            shopify.Session.setup(
                api_key=os.getenv('SHOPIFY_API_KEY'),
                secret=os.getenv('SHOPIFY_SHARED_SECRET'))
            try:
                shop_session = shopify.Session.validate_params(request.args)
                print('Parameters verified in decoration function. \n session: ', shop_session)
            except Exception as ex:
                return redirect(url_for('app.shopify', **request.args))
        else:
            try:
                session.pop("shopify_token")
                session.pop("shopify_url")
                session.pop("shopify_id")
                return redirect(url_for('shopify_bp.install', **request.args))
            except Exception as e:
                return('There has been an error: ', e)

        return function(*args, **kwargs)

    return decorated_function
