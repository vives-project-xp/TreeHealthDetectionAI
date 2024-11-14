# TreeHealthDetectionAI

## Het team

[<img src="https://github.com/RobbeDeW.png" alt="" width="25" style="margin-bottom:-6px;"> Robbe De Wispelaere](https://github.com/RobbeDeW)

[<img src="https://github.com/BossuytC.png" alt="" width="25" style="margin-bottom:-6px;"> Colin Bossuyt](https://github.com/BossuytC)

[<img src="https://github.com/NielsDenoo.png" alt="" width="25" style="margin-bottom:-6px;"> Niels Denoo](https://github.com/NielsDenoo)

## Beschrijving van project

Dit is de opdracht die we kregen voor dit project.

- **Dataverzameling**: Zoek de nodige luchtfoto's en infraroodkaarten van Vlaanderen. Deze zijn beschikbaar via online bronnen, maar ook bij VIVES-collega's in Roeselare.
- **Dashboard**: Ontwikkel een uitgebreid dashboard met Plotly Dash, waarin gebruikers de resultaten kunnen bekijken en navigeren. Zorg voor een interactieve en gebruiksvriendelijke interface.
- **Boom herkenning**: Met behulp van een online library moeten bomen worden gedetecteerd vanlucht foto's.
- **Deployment op mini-PC**: Zorg dat het volledige systeem offline werkt en stand-alone kan draaien op een mini-PC met een Linux-besturingssysteem, geschikt voor gebruik tijdens open dagen en evenementen

## Concept

We gaan met behulp van een dataset een AI trainen die via luchtfoto's bomen kan detecteren en hun gezondheid beoordelen.
De dataset die we gebruiken bestaat uit JP2 bestanden die we niet kunnen gebruiken. We aan daarom die bestanden omzetten naar PNG tiles met behulp van de gdal2tiles library.
Met deze tiles kunnen we de AI trainen en ook een interactief dashboard maken. 

Het dashboard ontwikkelen we in python met behulp van Dash en Dash-Leaflet. Het zal ook meerdere kaarten bevatten voor RGB foto's, CIR foto's en tot slot een kaart die de resultaten van de AI toont. Verder zal het ook statistieken tonen over de bomen.

## Mappenstructuur
- [Detectree2Lib](Detectree2Lib/): Alle info over hoe we de library toepassen op ons project. 

## Dataset

Link naar de dataset die we gaan gebruiken voor de AI te trainen en voor het dashboard.
[Vlaanderen.be](https://download.vlaanderen.be/product/9531)

## Proces

### Week 1

In de eerste week hebben we vooral het concept uitgewerkt en zitten brainstormen over hoe we het gingen aanpakken. We waren ook al begonnen met het zoeken naar een goede dataset. Verder hebben we het [projectcanvas](./docs/project-canvas.pdf) ingevuld en begonnen aan de README.

### Week 2

In de tweede week hebben we gezocht naar een goede library voor een AI algoritme, deze is [detectree2Lib](https://github.com/PatBall1/detectree2). We hebben ook gezocht naar een manier om de JP2 bestanden uit onze dataset om te zetten naar een ander formaat. Hierbij hadden we wat problemen om een goede manier te vinden.

### Week 3

In de derde week zijn we bezig geweest om de library te gebruiken, we hebben er wat moeilijkheden mee. Verder hebben we ook een manier gevonden om de JP2 bestanden om te zetten naar PNG bestanden die we kunnen gebruiken als tiles voor dashboard en de AI te trainen. We zijn ook begonnen met hetmaken van het dashboard die als kaart een stuk van Brugge toont.
