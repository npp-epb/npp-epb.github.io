# For Debug

from src.util import *
from src.template_vars import *

from flask import Flask, render_template

app = Flask(__name__)
main_css = 'static/main.css'

@app.route("/")
def index():
    return render_template("index.jinja", **globals())
