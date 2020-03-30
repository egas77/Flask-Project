from flask import Flask
from config import Develop

app = Flask(__name__)
app.config.from_object(Develop)
