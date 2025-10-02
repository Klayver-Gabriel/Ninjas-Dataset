import numpy as np
import pandas as pd
from flask import Flask,render_template


app = Flask(__name__)
from view_routes import *
brute_rol = pd.read_csv("Banco de Ninjas.csv")
if __name__ == "__main__":
    app.run(port= 50001)




