import numpy as np
import pandas as pd
from flask import Flask,render_template

app = Flask(__name__)

from view_routes import *

if __name__ == "__main__":
    app.run(port= 50001)




