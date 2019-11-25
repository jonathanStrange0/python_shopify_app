from flask import Flask
# from app.config import DefaultConfig
from config import Config
app = Flask(__name__)

app.config.from_object(Config)
from app import routes
