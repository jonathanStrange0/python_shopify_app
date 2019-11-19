from functools import wraps
import shopify
from flask import session, redirect, url_for, request, current_app

def shopify_auth_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        #TODO add authorization code here
        pass
