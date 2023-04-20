'use strict';

/*
  Ongelmakenttä:

  Synkroninen funktiokutsu (normaali): Suoritetaan ohjemaan rivi riviltä, törmätään fuktiokutsuun.
  Käydään suorittamassa funktio ja vasta kun se on suoritettu kokonaan jatketaan rivi riviltä etenemistä.

  Asynkroninen funktiokutsu (tässä, suositeltu javascriptissä): suoritetaan ohjelmaa rivi riviltä, törmätään funktiokutsuun.
  Lähdetään suorittamaan funktiota,
  mutta ei odotetakaan funktion suoritusta loppuun vaan samaan aikaan jatketaan kutsuvan ohjelman osan rivien etenemistä

  Asynkronisella kutsulla vältetään sivun jääminen jumiin mutta samaan aikaan se hankaloittaa meidän koodaamista.

  Fetch on javascriptin kurssilla aikaisemmin esitellyn REST rajapinnan GET.
  Eli suorittaa back endin määrittelemän end point kutsun. (Meillä tässä maat, näkyy urlin lopussa)

  Ja emme voi sille mitään, että fetch on asynkroninen.

  Usein kuitenkin se on meille olennaista, että jatkamme vasta kun kutsu on suoritettu kokonaan.
  Tässä esimerkissä olisi aika hölmöä, että nettisivun vetolaatikkoon generoituisi ensin muutama maa ja
  käyttäjän voisi painaa hae nappia kesken kaiken. Sen sijaan haluamme, että vetolaatikkoon tulee kerralla kaikki maailman maat.

  Joten haluamme pakottaa fetch kutsun olemaan synkroninen. Tähän on Ilen materiaalissa kaksi tapaa:

  1) await
  2) then

  Kysyin teollisuudessa developerina toimilta parilta kaverilta. Heillä molemmilla lievä preferenssi then
  mutta sanouvat olevan pitkälti makuasuia. ChatGPT sanoo myös valinnan olevan makuasia.
  Jätän then koodin kommenttina loppuun mutta keskitymme Ilen materiaaleissa vahvemmin esiin tuotuun await-tapaan.

  1) await

  Elämämme ei kuitenkaan ole vielä fetchin synkroniseksi pakottamisen jälkeenkään simppeliä koska
  await komentoa ei saa käyttää kuin asynkronisessa funktiossa. Meillä tässä haeMaat().

  Koska haeMaat() on asynkroninen (vaikka sen sisällä itse fecth() onkin pakotettu asynkroniseksi) emme voi tehdä siten,
  että meillä olisi taytaVetolaatikko() funktio joka kutsuisi haeMaat()-funktiota ja saisi siltä jsonina maailman maat.

  Koska asynkronisesta haeMaat() funktiosta voidaan hypätä pois ja takaisin, voimme havaita,
  että edestakaisin hyppivään asynkroniseen funktioon emme voi kirjoittaa return-lausetta paluuarvolle.
  Meillä tassä maailman maat sisältävää jsonia.

  Joten emme pysty kirjoittamaan taytaVetolaakikko()-funktioon kutsua asynkroniseen haeMaat() funktioon
  hyödyntäen sen paluuarvoa.

  Joten meille jää jäljelle vain vaihtoehto, että kirjoitamme asynkronisen haeMaat() funktioon kutsun
  taytaVetolaatikko()-funktioon. Synkroniseksi pakotetun fecth rivin jälkeen tiedämme että meillä on kaikki maailman maat
  json olemassa kokonaisena. Ja sen voimme antaa parametrina taytaVetolaatikko() funktiolle.

  2) then

  Nyt tulee vääjäämättä mieleen, että teemme synkronisen haeMaat() funktion ja voimme ihan rauhassa kutsua
  teeVetolaatikko()-funktiosta paluuarvon palauttavaa haeMaat() funktiota. Mutta emme voi koska then jää odottamaan
  responcea eli ratkaisussa syntyy call back pino...

  Joka tapauksessa nyt keskitymme versioon 1) await

 */

// 1) await
async function haeMaat() {

  try {
    // fetch on se meidän puhuma REST-rajapinnan GET
    // maat urlin päässä on se meidän Python Flaskissa määrittämä end point
    const vastaus = await fetch('http://localhost:3000/maat');

    // vastaus sisältää muutakin kuin meidän end pointin palauttaman jsonin. Se sisältää mm. http tilakoodin
    // ja siksi se json pitää vielä erikseen pyytää vastaukselta
    const jsonMaat = await vastaus.json();

    taytaVetolaatikko(jsonMaat);
  } catch (error) {
    console.log(error.message);
  } finally {
    console.log('asynchronous load complete');
  }
}

// 2) then (Johon emme keskity nyt kurssilla, on tässä mukana sivistykseksi, koska on myös suosiossa teollisuudessa)
/*
function haeMaat() {

  fetch('http://localhost:3000/maat').then((vastaus) => {
    return vastaus.json();
  }).then((jsonMaat) => {

    // Tässä kohtaa json näpeissä
    taytaVetolaatikko(jsonMaat);
  });
};*/

function taytaVetolaatikko(jsonMaat) {
  // Generoidaan HTML-merkkijono jossa select tagi ja option tagi
  let htmlvetolaatikko = '<select>';
  for (let i = 0; i < jsonMaat.length; i++) {
    let maa = jsonMaat[i];
    htmlvetolaatikko = htmlvetolaatikko + '<option>' + maa + '</option>';
  }
  htmlvetolaatikko = htmlvetolaatikko + '</select>';

  //Lisätään äsken generoitu html-koodia sisältävä merkkijono html pohjassa olevan select tagin tilalle
  document.getElementById('maat').innerHTML = htmlvetolaatikko;
}

function taytaLista(jsonKentat) {

  // Generoidaan HTML-merkkijono jossa select ul ja li tagi
  let htmlLista = '<ul>';
  for (let i = 0; i < jsonKentat.length; i++) {
    let kentta = jsonKentat[i];
    htmlLista = htmlLista + '<li>' + kentta + '</li>';
  }
  htmlLista = htmlLista + '</ul>';

  //Lisätään äsken generoitu html-koodia sisältävä merkkijono html pohjassa olevan select tagin tilalle
  document.getElementById('kentat').innerHTML = htmlLista;
}

async function haeNappi() {
  console.log('hae nappi toimii');

  // Meidän pitää selvittää käyttäjän valitsema maa vetolaatikosta
  let vetolaatikko = document.getElementById('maat');
  let maa = vetolaatikko.options[vetolaatikko.selectedIndex].text;

  // kutsutaan back endin end pointtia, samat edellä selitetyt await kujeet
  try {
    // fetch on se meidän puhuma REST-rajapinnan GET
    // maat urlin päässä on se meidän Python Flaskissa määrittämä end point
    const vastaus = await fetch('http://localhost:3000/kentatMaasta/' + maa);

    // vastaus sisältää muutakin kuin meidän end pointin palauttaman jsonin. Se sisältää mm. http tilakoodin
    // ja siksi se json pitää vielä erikseen pyytää vastaukselta
    const jsonKentat = await vastaus.json();

    taytaLista(jsonKentat);
  } catch (error) {
    console.log(error.message);
  } finally {
    console.log('asynchronous load complete');
  }
}

// Pääohjelma ensimmäinen rivi

//Täyttää vetolaatikon
haeMaat();

//Lisää kuuntelijan hae-napille. Kuuntelija suorittaa haeNappi() funktion
document.querySelector('#hae').addEventListener('click', haeNappi);

