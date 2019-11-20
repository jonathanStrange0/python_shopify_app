from flask import Flask
# from app.config import DefaultConfig 
app = Flask(__name__)

from app import routes
