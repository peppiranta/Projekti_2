from flask import Flask, Response
from flask_cors import CORS
import mysql.connector
import json

# Jotta end point toimii javascriptissä pitää vielä asentaa Flask Cors ja importoida se
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/maat')
def maat():
    sql = "select name from country"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()

    paluujson = json.dumps(tulos)
    tilakoodi = 200
    # palautetaan muutakin kuin json ja siksi tehdään Response olio joka sisältää statuksen ja nimetypen
    return Response(response=paluujson, status=tilakoodi, mimetype="application/json")


@app.route('/kentatMaasta/<maa>')
def kentatMaasta(maa):
    sql = "select airport.name from airport, country where airport.iso_country = country.iso_country and country.name = '" + maa + "'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()

    print(sql)

    paluujson = json.dumps(tulos)
    tilakoodi = 200
    # palautetaan muutakin kuin json ja siksi tehdään Response olio joka sisältää statuksen ja nimetypen
    return Response(response=paluujson, status=tilakoodi, mimetype="application/json")


yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='Peppi10',
    password='123456',
    autocommit=True
)
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)