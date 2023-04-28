import mysql.connector
from flask import Flask, Response, request
from flask import Flask, jsonify
import requests
import json
yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='sevenwonders',
         user='hanna',
         password='nimohanna',
         autocommit=True
         )
app = Flask(__name__)

def player_name(nimi):
    id_funktio = str(register())
    sql = "insert into game(id, screen_name, location, co2_budget, co2_consumed) "
    sql += "values('" + id_funktio + "' , '" + nimi + "' , '" + "EFHK" + "' , '" + "10000" + "' , '" + "0" + "');"
    #print(sql)
    cursor = yhteys.cursor()
    cursor.execute(sql)
    return

def register():
    lista=[]
    sql = "SELECT id FROM game ORDER BY ID DESC LIMIT 1;"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        newid= int(i[-1]) + 1
        lista.append(newid)
    return str(lista[-1])

@app.route('/register/<nimi>')
def registerr(nimi):
    response=player_name(nimi)
    return response

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)