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
    database='lentopeli',
    user='nahal1',
    password='Umerasif1',
    autocommit=True
)
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
    import mysql.connector
    import random
    from geopy.distance import geodesic
    import mysql.connector
    from geopy.distance import geodesic

    yhteys = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='the_wonders',
        user='nahal1',
        password='Umerasif1',
        autocommit=True
    )


    def register():
        lista = []
        sql = "SELECT id FROM game ORDER BY ID DESC LIMIT 1;"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            newid = int(i[-1]) + 1
            lista.append(newid)
        return str(lista[-1])


    def player_name(nimi):
        id_funktio = str(register())
        sql = "insert into game(id, screen_name, location, co2_budget, co2_consumed) "
        sql += "values('" + id_funktio + "' , '" + nimi + "' , '" + "EFHK" + "' , '" + "10000" + "' , '" + "0" + "');"
        # print(sql)
        cursor = yhteys.cursor()
        cursor.execute(sql)
        return


    def find_id():
        mycursor = yhteys.cursor()
        mycursor.execute("SELECT id FROM game WHERE screen_name ='" + name + "'")
        myresult = mycursor.fetchone()
        return (myresult)


    def location():
        mycursor = yhteys.cursor()
        mycursor.execute("SELECT location FROM game WHERE screen_name ='" + name + "'")
        myresult = mycursor.fetchone()
        return myresult


    def get_airport_info(nimi):
        mycursor = yhteys.cursor()
        mycursor.execute("SELECT latitude_deg,longitude_deg FROM airport WHERE ident =  '" + nimi + "'  ")
        myresult = mycursor.fetchone()
        longitude = myresult[1]
        latitude = myresult[0]
        return [latitude, longitude]


    def story_intro():
        print("Tervetuloa pelaamaan The Seven Wonders -peliä!")
        print("---------------------------------------------------------------")
        print(
            "Tavoitteenasi on matkustaa näkemään seitsemän eri nähtävyyttä, mahdollisimman vähäisillä hiilidioksidipäästöillä.")
        print("Aloitat Helsinki-Vantaa lentokentältä. Pääset matkustamaan eri lentokentille ICAO-koodien avulla.")
        print("Nyt kohti ensimmäistä nähtävyyttä!")
        print()
        return


    def update_location(location):
        x = find_id()
        id = x[0]
        sql = f"UPDATE game SET location ='" + location + "' WHERE id = '" + str(id) + "'"
        cursor = yhteys.cursor()
        cursor.execute(sql)


    def update_co2budget(answer):
        x = find_id()
        id = x[0]
        sql = f"UPDATE game SET co2_consumed = co2_consumed +'" + str(answer) + "' WHERE id = '" + str(id) + "'"
        cursor = yhteys.cursor()
        cursor.execute(sql)


    def update_co2budget2(answer):
        x = find_id()
        id = x[0]
        sql = f"UPDATE game SET co2_consumed = co2_consumed -'" + str(answer) + "' WHERE id = '" + str(id) + "'"
        cursor = yhteys.cursor()
        cursor.execute(sql)


    def get_airports():
        sql = f"SELECT iso_country, municipality, ident FROM airport WHERE nahtavyydet = 'yes'"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


    def co2_consumed_updated():
        mycursor = yhteys.cursor()
        mycursor.execute("SELECT co2_consumed FROM game WHERE screen_name ='" + name + "'")
        myresult = mycursor.fetchone()
        return myresult


    def matkamuistot_updated():
        sql = f"select name from goal left join goal_reached on goal.id = goal_id  left join game on game.id = game_id where screen_name = '" + name + "'"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


    def distance(maa):
        sql_1 = "select airport.latitude_deg, airport.longitude_deg, game.location from airport, game  where airport.ident = game.location and screen_name = '" + name + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql_1)
        tulos = kursori.fetchall()
        for line in tulos:
            lttd_1 = line[0]
            lon_1 = line[1]
            airport_1 = (lttd_1, lon_1)

        icoa_2 = maa
        sql_2 = "select latitude_deg, latitude_deg from airport where ident = '" + icoa_2 + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql_2)
        tulos = kursori.fetchall()
        for line in tulos:
            lttd_2 = line[0]
            lon_2 = line[1]
            airport_2 = (lttd_2, lon_2)

        answer = int((geodesic(airport_1, airport_2).kilometers) * 0.1)
        update_co2budget(str(answer))


    def matkamuistojenkeräily():
        print("Sait: \n"
              "Norsu-patsaan, \n"
              "Bumerangin, \n"
              "Puisen käsikorun, \n"
              "Christ the redeemer-patsaan, \n"
              "Colosseum-patsaan, \n"
              "Pääkallo koriste-esineen ja\n"
              "Poro-avaimenperän")


    def onkokaikkikerätty():
        x = find_id()
        id = x[0]
        mycursor = yhteys.cursor()
        mycursor.execute("SELECT * FROM goal_reached WHERE game_id ='" + str(id) + "'")
        result = mycursor.fetchall()
        määrä = 0
        for i in result:
            määrä = määrä + 1
        return määrä


    def matkamuistot(maa_id):
        x = find_id()
        id = x[0]
        mycursor = yhteys.cursor()
        mycursor.execute(
            "SELECT game_id, goal_id FROM goal_reached WHERE game_id ='" + str(id) + "' and goal_id = '" + str(
                maa_id) + "'")
        result = mycursor.fetchall()
        if len(result) == 0:
            sql = "insert into goal_reached (game_id, goal_id) values ('" + str(id) + "' , '" + str(maa_id) + "');"

            cursor = yhteys.cursor()
            cursor.execute(sql)
            print("Sait matkamuistoksi: ")
            mycursor.execute("SELECT name FROM goal where id ='" + str(maa_id) + "'")
            result = mycursor.fetchall()
            muisto = result[0]
            print(muisto)

        elif len(result) != 0:
            print('Olet jo saanut matkamuistot: ')
            x = matkamuistot_updated()
            for m in x:
                print(m)


    name = input("Syötä nimi: ")
    player_name(name)

    print("Hei " + name + "! Tervetuloa pelaamaan The Seven Wonders -peliä")
    print("---------------------------------------------------------------")
    print(
        "Tavoitteenasi on matkustaa näkemään seitsemän eri nähtävyyttä, mahdollisimman vähäisillä hiilidioksidipäästöillä.")
    print("Aloitat Helsinki-Vantaa lentokentältä. Pääset matkustamaan eri lentokentille ICAO-koodien avulla.")
    print("Nyt kohti ensimmäistä nähtävyyttä!")

    paastot = 10000
    scenery = False
    peli = False
    while True:
        vastaus = input("Aloitetaanko peli, kyllä tai ei? ").lower()
        if vastaus == "kyllä":
            peli = True
            break
        if vastaus == "ei":
            break
        else:
            print('En ymmärtänyt. Kirjoita uudelleen, kiitos!')
    while peli:
        muistot = onkokaikkikerätty()
        if muistot == 7:
            print('Keräsit kaikki, onneksi olkoon!')
            break
        x = co2_consumed_updated()
        päästö = x[0]
        päästö = int(päästö)
        if päästö > 10000:
            print('CO2 päästösi ylittivät 10 000 kg rajan. Päästö määräsi on:  ', päästö, ' kg')
            break
        x = location()
        maa = x[0]
        if maa == 'EFHK':
            print('Olet, Helsinki-Vantaa lentokentällä, Suomessa')
            print("-" * 30)
            tapa = input('Lennä toiseen maahan = 5: \n'
                         'Lopeta = 6')
            if tapa == '5':
                print(get_airports())
                maa = input(
                    'Valitse mihin kohteeseen haluat lentää ensimmäisenä, yllä olevien ICAO-koodein avulla: ').upper()

                while True:
                    if maa == "EFRO" or maa == "FLLI" or maa == "LIRF" or maa == "MMMX" or maa == "SBGL" or maa == "VIAG" or maa == "YBCS":
                        update_location(maa)
                        distance(maa)
                        break
                    else:
                        print('Hups taisit syöttää väärän koodin. Kokeile uudelleen!')
                        print(get_airports())
                        maa = input('Syötä koodi: ')
            if tapa == "6":
                break
        if maa == 'EFRO':
            maa_id = 4
            if scenery == True:
                print('Olet joulupukin kylässä!')
                print("-" * 30)
                i = co2_consumed_updated()
                onkokaikkikerätty()
                print(f"CO2 Consumed: {i[0]}")
                print("-" * 30)
                matkamuistot(maa_id)

                tapa = input('Miten haluaisit matkustaa takaisin lentokentälle? \n '
                             'Taksilla = 1 \n'
                             'Kävellen = 2\n'
                             'Lopeta = 3')
                if tapa == '1':
                    print("-" * 30)
                    print("Rangaistuksena saat 500 kg lisää päästöihisi.")
                    print("-" * 30)
                    update_co2budget(500)
                    scenery = False
                if tapa == '2':
                    print("-" * 30)
                    print("Palkinnoksi päästöistäsi vähennetään 500 kg. ")
                    print("-" * 30)
                    update_co2budget(500)
                    scenery = False
                if tapa == "3":
                    break
            else:
                print('Olet, Rovaniemen lentokentällä, Suomessa')
                print("-" * 30)
                i = co2_consumed_updated()
                print(f"CO2 Consumed: {i[0]}")
                print("-" * 30)
                tapa = input('Miten haluaisit matkustaa nähtävyydelle? \n '
                             'Taksilla = 1 \n'
                             'Hiihtäen = 2 \n'
                             'Patikoimalla = 3 \n'
                             'Lennä toiseen maahan = 5: \n'
                             'Lopeta = 6')
                if tapa == '1':
                    print("-" * 30)
                    print("Oh my days! Taksikuskisi pysäytetään epäillystä huumeiden hallussapidosta.\n"
                          "Sinua epäillään osalliseksi ja viedään suurella poliisiautolla putkaan kuulusteltavaksi.\n"
                          "Rangaistuksena saat 500 kg lisää päästöihin")
                    print("-" * 30)
                    update_co2budget(500)
                    scenery = True
                if tapa == '2':
                    scenery = True
                if tapa == '3':
                    print(
                        "Tapaat joulupukin! Koska olet ollut kiltti, hän vie sinut näkemään revontulia. Palkinnoksi sinulta vähennetään 500kg päästöistäsi")
                    update_co2budget2(500)
                    scenery = True
                if tapa == '5':
                    while True:

                        print(get_airports())
                        maa = input('Minne haluat lentää seuraavaksi: ').upper()

                        if maa == "EFRO" or maa == "FLLI" or maa == "LIRF" or maa == "MMMX" or maa == "SBGL" or maa == "VIAG" or maa == "YBCS":
                            update_location(maa)
                            distance(maa)
                            break
                        else:
                            print('Hups taisit syöttää väärän koodin. Kokeile uudelleen!')
                            print(get_airports())
                            maa = input('Syötä koodi: ')
                            distance(maa)
                if tapa == "6":
                    break
        if maa == 'FLLI':
            maa_id = 5
            if scenery == True:
                print('Olet Victorian vesiputouksilla')
                print("-" * 30)
                i = co2_consumed_updated()
                print(f"CO2 Consumed: {i[0]}")
                print("-" * 30)
                matkamuistot(maa_id)

                tapa = input('Miten haluaisit matkustaa takaisin lentokentälle?\n '
                             'Taksilla = 1 \n'
                             'Kävellen = 2\n'
                             'Lopeta = 3')
                if tapa == '1':
                    update_co2budget(500)
                    scenery = False
                if tapa == '2':
                    update_co2budget2(500)
                    scenery = False
                if tapa == "3":
                    break
            else:
                print('Olet, Harry Mwanga Nkumbula kansainvälisellä lentokentällä, Sambiassa')
                print("-" * 30)
                i = co2_consumed_updated()
                print(f"CO2 Consumed: {i[0]}")
                print("-" * 30)
                tapa = input('Miten haluasit matkustaa nähtävyydelle?\n '
                             'Taksilla = 1 \n'
                             'Kävellen = 2 \n'
                             'Tuk tukilla = 3 \n'
                             'Lennä toiseen maahan = 5: \n'
                             'Lopeta = 6')
                if tapa == '1':
                    scenery = True
                if tapa == '2':
                    print("-" * 30)
                    print("Auts! Nyrjäytät nilkkasi kävellessä ja joudut menemään lääkäriin taksilla. \n"
                          "Rangaistuksena saat 500 kg lisää hiilidioksidipäästöjä")
                    print("-" * 30)
                    update_co2budget(500)
                    scenery = True
                if tapa == '3':
                    scenery = True
                if tapa == '5':
                    while True:

                        print(get_airports())
                        maa = input('Valitse seuraava matkakohde, yllä olevien ICAO-koodien avulla: : ').upper()
                        if maa == "EFRO" or maa == "FLLI" or maa == "LIRF" or maa == "MMMX" or maa == "SBGL" or maa == "VIAG" or maa == "YBCS":
                            distance(maa)
                            update_location(maa)
                            break
                        else:
                            print('Hups taisit syöttää väärän koodin. Kokeile uudelleen')
                            print(get_airports())
                            maa = input('Syötä koodi: ')
                            distance(maa)
                if tapa == "6":
                    break
        if maa == 'LIRF':
            maa_id = 7
            if scenery == True:
                print('Olet Rooman Colosseumilla')
                print("-" * 30)
                i = co2_consumed_updated()
                print(f"CO2 Consumed: {i[0]}")
                print("-" * 30)
                matkamuistot(maa_id)
                tapa = input('Miten haluasit matkustaa takaisin lentokentälle?\n '
                             'Taksilla = 1 \n'
                             'Kävellen = 2\n'
                             'Lopeta = 3')
                if tapa == '1':
                    scenery = False

                if tapa == '2':
                    scenery = False
                if tapa == "3":
                    break
            else:
                print('Olet, Fiumicon lentokentällä, Italiassa')
                print("-" * 30)
                i = co2_consumed_updated()
                print(f"CO2 Consumed: {i[0]}")
                print("-" * 30)
                tapa = input('Miten haluasit matkustaa nähtävyydelle? \n '
                             'Taksilla = 1 \n'
                             'Vuokra-autolla = 2 \n'
                             'Sähköpotkulaudalla = 3 \n'
                             'Bussilla = 4 \n'
                             'Lennä toiseen maahan = 5: \n'
                             'Lopeta = 6')
                if tapa == '1':
                    scenery = True
                if tapa == '2':
                    print("-" * 30)
                    print("Voi rähmä! Renkaasi puhkesi ja joudut soittamaan huoltoauton.\n"
                          "Rangaistuksena päästöihisi lisätään 500 kg.")
                    ("-" * 30)
                    update_co2budget(500)
                    scenery = True
                if tapa == '3':
                    scenery = True
                if tapa == '4':
                    scenery = True
                if tapa == "6":
                    break
                if tapa == '5':
                    while True:

                        print(get_airports())
                        maa = input('Valitse seuraava matkakohde yllä olevien ICAO-koodien avulla: : ').upper()
                        if maa == "EFRO" or maa == "FLLI" or maa == "LIRF" or maa == "MMMX" or maa == "SBGL" or maa == "VIAG" or maa == "YBCS":
                            distance(maa)
                            update_location(maa)
                            break
                        else:
                            print('Hups taisit syöttää väärän koodin. Kokeile uudelleen!')
                            print(get_airports())
                            maa = input('Syötä koodi: ')
                            distance(maa)
        if maa == 'MMMX':
            maa_id = 6
            if scenery == True:
                print('Olet, San Juan Teotihuacanassa, Meksikossa')
                print("-" * 30)
                i = co2_consumed_updated()
                print(f"CO2 Consumed: {i[0]}")
                print("-" * 30)
                matkamuistot(maa_id)
                tapa = input('Miten haluaisit matkustaa takaisin lentokentälle?\n '
                             'Taksilla = 1 \n'
                             'Kävellen = 2\n'
                             'Lopeta = 3')
                if tapa == '3':
                    break
                if tapa == '1':
                    scenery = False
                    paastot = paastot + 30
                if tapa == '2':
                    scenery = False
            else:
                print('Olet, Licenciado Benito Juarez kansainvälisellä lentokentällä, Meksikossa. ')
                print("-" * 30)
                print("-" * 30)
                i = co2_consumed_updated()
                print(f"CO2 Consumed: {i[0]}")
                print("-" * 30)
                tapa = input('Miten haluasit matkustaa nähtävyydelle?\n '
                             'Taksilla = 1 \n'
                             'Vuokra-autolla = 2 \n'
                             'Julkisella liikenteellä = 3 \n'
                             'Lennä toiseen maahan = 5: \n'
                             'Lopeta = 6')
                if tapa == '6':
                    break
                if tapa == '1':
                    print("-" * 30)
                    print("Puhelimestasi loppui akku ja unohdit matkalaturisi hotellille.\n"
                          "Sinun täytyy palata lataamaan akkuasi hotellihuoneeseen ennen liikkeelle lähtöä.\n"
                          "Rangaistuksena saat 500 kg lisää päästöjä")
                    print("-" * 30)
                    update_co2budget(500)
                    scenery = True
                if tapa == '2':
                    scenery = True
                if tapa == '3':
                    print("-" * 30)
                    print("Bussi, jolla matkustat, toimii sähköenergialla. \n "
                          "Tästä ympäristöteosta sinua palkitaan vähentämällä 500 kg hiilidioksidipäästöistä.")
                    print("-" * 30)
                    update_co2budget2(500)
                    scenery = True
                if tapa == '5':
                    while True:

                        print(get_airports())
                        maa = input('Valitse seuraava matkakohde yllä olevien ICAO-koodien avulla: ').upper()
                        if maa == "EFRO" or maa == "FLLI" or maa == "LIRF" or maa == "MMMX" or maa == "SBGL" or maa == "VIAG" or maa == "YBCS":
                            distance(maa)
                            update_location(maa)
                            break
                        else:
                            print('Hups taisit syöttää väärän koodin. Kokeile uudelleen!')
                            print(get_airports())
                            maa = input('Syötä koodi: ')
                            distance(maa)
        if maa == 'SBGL':
            maa_id = 3
            if scenery == True:
                print('Olet Kristus Vapahtaja -patsaalla.')
                print("-" * 30)
                i = co2_consumed_updated()
                print(f"CO2 Consumed: {i[0]}")
                print("-" * 30)
                matkamuistot(maa_id)
                tapa = input('Miten haluasit matkustaa takaisin lentokentälle?\n '
                             'Taksilla = 1 \n'
                             'Kävellen = 2\n'
                             'Lopeta = 3')
                if tapa == '3':
                    break
                if tapa == '1':
                    scenery = False
                    paastot = paastot + 30
                if tapa == '2':
                    scenery = False
            else:
                print('Olet, Tom Jobimin kansainvälisellä lentokentällä, Brasiliassa.')
                print("-" * 30)
                tapa = input('Miten haluasit matkustaa nähtävyydelle? \n '
                             'Taksilla = 1 \n'
                             'Junalla = 2 \n'
                             'Patikoimalla = 3 \n'
                             'Lennä toiseen maahan = 5: \n'
                             'Lopeta = 6')
                if tapa == '6':
                    break
                if tapa == '1':
                    print("-" * 30)
                    print("Lucky day! Kuljettajasi tietää oikoreittejä.\n"
                          "Tästä hyvästä saat 500 kg vähennyksen hiilidioksidipäästöistäsi!")
                    print("-" * 30)
                    update_co2budget2(500)
                    scenery = True
                if tapa == '2':
                    print("-" * 30)
                    print("Eihäään! Junan kuljettajat ovat lakossa ja\n"
                          "joudut vuokraamaan auton.\n"
                          "Rangaistuksena saat 500 kg lisää päästöjä")
                    print("-" * 30)
                    update_co2budget(500)
                    scenery = True
                if tapa == '3':
                    scenery = True
                if tapa == '5':
                    while True:

                        print(get_airports())
                        maa = input('Valitse seuraava matkakohde yllä olevien ICAO-koodien avulla: : ').upper()
                        if maa == "EFRO" or maa == "FLLI" or maa == "LIRF" or maa == "MMMX" or maa == "SBGL" or maa == "VIAG" or maa == "YBCS":
                            distance(maa)
                            update_location(maa)
                            break
                        else:
                            print('Hups taisit syöttää väärän koodin. Kokeile uudelleen!')
                            print(get_airports())
                            maa = input('Syötä koodi: ')
                            distance(maa)
        if maa == 'VIAG':
            maa_id = 1
            if scenery == True:
                print('Olet Taj Mahalilla.')
                print("-" * 30)
                i = co2_consumed_updated()
                print(f"CO2 Consumed: {i[0]}")
                print("-" * 30)
                matkamuistot(maa_id)
                print("-" * 30)
                tapa = input('Miten haluaisit matkustaa takaisin lentokentälle?\n '
                             'Taksilla = 1 \n'
                             'Kävellen = 2\n'
                             'Lopeta = 3')
                if tapa == '3':
                    break
                if tapa == '1':
                    scenery = False

                if tapa == '2':
                    scenery = False
            else:
                print('Olet, Agran lentokentällä, Intiassa')
                tapa = input('Miten haluasit matkustaa nähtävyydelle? \n '
                             'Taksilla = 1 \n'
                             'Kävellen = 2 \n'
                             'Tuk tukilla = 3 \n'
                             'Lennä toiseen maahan = 5: \n'
                             'Lopeta = 6')
                if tapa == '6':
                    break
                if tapa == '1':
                    scenery = True
                if tapa == '2':
                    scenery = True
                if tapa == '3':
                    print("-" * 30)
                    print("Voi itku! Jäit ruuhkaan jumiin.\n"
                          "Rangaistuksena päästöihisi lisätään 500kg")
                    print("-" * 30)
                    update_co2budget(500)
                    scenery = True
                if tapa == '5':
                    while True:

                        print(get_airports())
                        maa = input('Valitse seuraava matkakohde yllä olevien ICAO-koodien avulla: : ').upper()
                        if maa == "EFRO" or maa == "FLLI" or maa == "LIRF" or maa == "MMMX" or maa == "SBGL" or maa == "VIAG" or maa == "YBCS":
                            distance(maa)
                            update_location(maa)
                            break
                        else:
                            print('Hups taisit syöttää väärän koodin. Kokeile uudelleen!')
                            print(get_airports())
                            maa = input('Syötä koodi: ')
                            distance(maa)
        if maa == 'YBCS':
            maa_id = 2
            if scenery == True:
                print('Olet Australian Isolla Valliriutalla')
                print("-" * 30)
                i = co2_consumed_updated()
                print(f"CO2 Consumed: {i[0]}")
                print("-" * 30)
                matkamuistot(maa_id)
                print("-" * 30)
                print("-" * 30)
                tapa = input('Miten haluaisit matkustaa takaisin lentokentälle?\n '
                             'Taksilla = 1 \n'
                             'Kävellen = 2\n'
                             'Lopeta = 3')
                if tapa == "3":
                    break
                if tapa == '1':
                    scenery = False
                    paastot = paastot + 30
                if tapa == '2':
                    scenery = False
            else:
                print('Olet, Cairns:in lentokentällä, Australiassa')
                tapa = input('Miten haluasit matkustaa \n '
                             'Taksilla = 1 \n'
                             'Vuokra-autolla = 2 \n'
                             'Lennä toiseen maahan = 5: \n'
                             'Lopeta = 6')
                if tapa == "6":
                    break
                if tapa == '1':
                    print("-" * 30)
                    print("Taxi kuskisi yskii koko matkan ja nyt epäilet, että olet saanut koronavirus tartunnan.\n"
                          "Käyt virus-testissä, pitkän matkan päässä, Taksilla.\n"
                          "Rangaistuksena päästöihin lisätään 500 kg")
                    print("-" * 30)
                    update_co2budget(500)
                    scenery = True
                if tapa == '2':
                    scenery = True
                if tapa == '5':
                    while True:

                        print(get_airports())
                        maa = input('Valitse seuraava matkakohde yllä olevien ICAO-koodien avulla: : ').upper()
                        if maa == "EFRO" or maa == "FLLI" or maa == "LIRF" or maa == "MMMX" or maa == "SBGL" or maa == "VIAG" or maa == "YBCS":
                            distance(maa)
                            update_location(maa)
                            break
                        else:
                            print('Hups taisit syöttää väärän koodin. Kokeile uudelleen!')
                            print(get_airports())
                            maa = input('Syötä koodi: ')
                            distance(maa)
    print("-------------------------------")
    i = co2_consumed_updated()

    print('Peli päättyi')
    print("-------------------------------")
    print(f"CO2 päästösi: {i[0]}")
    print("-------------------------------")
    print('Keräsit nämä matkamuistot: ')
    x = matkamuistot_updated()
    for m in x:
        print(m)
    print("-------------------------------")