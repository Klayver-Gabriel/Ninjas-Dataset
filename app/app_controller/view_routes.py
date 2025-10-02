import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import render_template,request

from app.app_controller.main import app, brute_rol


@app.route("/",methods = ["GET"])
def showDataset():
    # SHOW THE DATASET
    return render_template("dataset.html",table = pd.read_csv("Banco de Ninjas.csv").to_html())
@app.route("/dataset",methods = ["POST"])
def modifyRol():
        # GETTING THE VALUES FROM THE REQUEST
        element = request.form.get("element")
        village = request.form.get("village")
        nome = request.form.get("nome")
        salario_str = request.form.get("salario")
        rank = request.form.get("rank")
        salario = float(salario_str)
        id = request.form.get("CPF")

        # CREATE A ARRAY WITH THE VALUES OF THE NEW NINJA SIGN IN
        a = np.array([nome,element,village,salario,rank,id])
        # ARRAY TO GET THE LINE WITH THE SAME VALUES OF THE SIGNED ID
        b = np.array(brute_rol.loc[brute_rol.ID == id])

        if a.all() != b.all():
            brute_rol.loc[int(brute_rol.index.max() + 1)] = a
        else:
            raise Exception("CADASTRO JA ENCONTRADO")

        brute_rol.to_csv("Banco de Ninjas.csv",index=False)
        return f"Olá {nome}, registramos você na organização mundial dos ninjas"
@app.route("/elementos",methods = ["GET"])
def showElements():
    query = request.form.get("element")
    return render_template("dataset.html",table = brute_rol[brute_rol["Elemento"] == query].to_html())
@app.route("/histograma",methods = ["GET"])
def plot():
    plt.hist(brute_rol["Rank"],bins= 20)
    plt.show()
    return "GRAFICO GERADO"
@app.route("/linear_regression",methods = ["GET"])
def linear_regression():
    # X IS OUR PREDICTIVE VARIABLE
    x = np.array(brute_rol["Rank"].values,int)
    # Y IS OUR DEPENDENT VARIABLE
    y = np.array(brute_rol["Salario"].values)
    # BETAS ARE OUR LINEAR FUNCTION SLOPE AND INTERCEPT
    betas = np.polyfit(x,y,1)
    reta = np.poly1d(betas)

    # WE SCATTER OUR DATA ALL ACROSS A CHART, THEN WE CROSS IT WITH OUR LINEAR REGRESSION FUNCTION STRAIGHT
    plt.scatter(x,y)
    plt.plot(x,reta(x))
    plt.show()
    return "GRAFICO GERADO"
@app.route("/clear",methods =  ["PUT"])
def clean():
    # DATA CLEANING BASED ON THEIR IDS
    brute_rol["ID"] = pd.to_numeric(brute_rol["ID"],errors="coerce")
    brute_rol["ID"].dropna(inplace=True)
    brute_rol.drop_duplicates(subset=["ID"],inplace= True)
    brute_rol.reset_index(drop=True,inplace=True)

    # DATA CLEANING TO FIX INVALID INPUTS IN THE DATASET(SALARIO NEEDS TO BE A INVALID INTEGER)
    brute_rol["Salario"] = pd.to_numeric(brute_rol["Salario"],errors="coerce")
    brute_rol["Salario"] = brute_rol["Salario"].fillna(brute_rol["Salario"].mean())
    brute_rol.to_csv("Banco de Ninjas.csv",index=False)

    return "Vazios Limpos"

@app.route("/filter",methods = ["GET"])
def filter_choose():
    collum = request.form.get("Collum")
    query = request.form.get("Filter")
    filter = brute_rol[brute_rol[collum]  == query]
    print(filter)
    return render_template("dataset.html",table = filter.to_html())