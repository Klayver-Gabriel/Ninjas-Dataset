import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import render_template,request

from app.app_controller.main import app

@app.route("/data",methods = ["GET"])
def read():
    nome_dataset = request.form.get("dataset")

    # SHOW THE DATASET
    return render_template("dataset.html",table = pd.read_csv(nome_dataset+".csv").to_html())
@app.route("/dataset",methods = ["POST"])
def create():
    nome_dataset = request.form.get("dataset")

    # GETTING THE VALUES FROM THE REQUEST
    brute_rol = pd.read_csv(str(nome_dataset) + ".csv")

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

    brute_rol.to_csv(nome_dataset+".csv",index=False)
    return f"Olá {nome}, registramos você na organização mundial dos ninjas"
@app.route("/histograma",methods = ["GET"])
def plot():
    nome_dataset = request.form.get("dataset")

    brute_rol = pd.read_csv(str(nome_dataset) + ".csv")

    plt.hist(brute_rol["Rank"],bins= 20)
    plt.show()
    return "GRAFICO GERADO"
@app.route("/linear_regression",methods = ["GET"])
def linear_regression():
    nome_dataset = request.form.get("dataset")

    brute_rol = pd.read_csv(str(nome_dataset) + ".csv")

    # X IS OUR PREDICTIVE VARIABLE
    x = np.array(brute_rol["Rank"].values, int)
    # Y IS OUR DEPENDENT VARIABLE
    y = np.array(brute_rol["Salario"].values)
    # BETAS ARE OUR LINEAR FUNCTION SLOPE AND INTERCEPT
    betas = np.polyfit(x, y, 1)
    reta = np.poly1d(betas)

    # WE SCATTER OUR DATA ALL ACROSS A CHART, THEN WE CROSS IT WITH OUR LINEAR REGRESSION FUNCTION STRAIGHT
    plt.scatter(x, y)
    plt.plot(x, reta(x))
    plt.show()
    return "GRAFICO GERADO"
@app.route("/clear",methods =  ["PUT"])
def clean():
    nome_dataset = request.form.get("dataset")

    brute_rol = pd.read_csv(str(nome_dataset) + ".csv")

    # DATA CLEANING BASED ON THEIR IDS
    brute_rol["ID"] = pd.to_numeric(brute_rol["ID"],errors="coerce")
    brute_rol["ID"].dropna(inplace=True)
    brute_rol.drop_duplicates(subset=["ID"],inplace= True)
    brute_rol.reset_index(drop=True,inplace=True)

    # DATA CLEANING TO FIX INVALID INPUTS IN THE DATASET(SALARIO NEEDS TO BE A INVALID INTEGER)
    brute_rol["Salario"] = pd.to_numeric(brute_rol["Salario"],errors="coerce")
    brute_rol["Salario"] = brute_rol["Salario"].fillna(brute_rol["Salario"].mean())
    brute_rol.to_csv(nome_dataset+".csv",index=False)

    return "Vazios Limpos"

@app.route("/filter",methods = ["GET"])
def filter_choose():
    nome_dataset = request.form.get("dataset")

    brute_rol = pd.read_csv(str(nome_dataset) + ".csv")

    collum = request.form.get("Collum")
    query = request.form.get("Filter")
    nome_filtro = request.form.get("Nome do filtro")
    print(nome_filtro)
    rol_filtrado = brute_rol[brute_rol[collum]  == query]
    if nome_filtro != "":
        rol_filtrado.to_csv(nome_filtro+".csv",index=False)
        print(f"TABELA CRIADA: {nome_filtro}")
    return render_template("dataset.html",table = rol_filtrado.to_html())