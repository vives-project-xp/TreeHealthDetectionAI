# TreeHealthDetectionAI

## Het team

<<<<<<< HEAD
- Robbe De Wispelaere
- Colin Bossuyt
- Niels Denoo
=======
[<img src="https://github.com/RobbeDeW.png" alt="" width="25" style="margin-bottom:-6px;"> Robbe De Wispelaere](https://github.com/RobbeDeW)

[<img src="https://github.com/BossuytC.png" alt="" width="25" style="margin-bottom:-6px;"> Colin Bossuyt](https://github.com/BossuytC)

[<img src="https://github.com/NielsDenoo.png" alt="" width="25" style="margin-bottom:-6px;"> Niels Denoo](https://github.com/NielsDenoo)
>>>>>>> 4488035a3a2793cd81b781eed2c76d77e220e1bb

## Beschrijving van project

Dit is de opdracht die we kregen voor dit project.

- **Dataverzameling**: Zoek de nodige luchtfoto's en infraroodkaarten van Vlaanderen. Deze zijn beschikbaar via online bronnen, maar ook bij VIVES-collega's in Roeselare.
<<<<<<< HEAD
- **Dataset opbouw**: Annoteer een groot aantal bomen om een gelabelde dataset op te
bouwen. Dit proces kan deels geautomatiseerd worden met bestaande modellen, zoals 'Segment Anything'. Onderzoek ook bestaande labeling tools om het annotatieproces te versnellen.
- **Modelontwikkeling**: Train een model dat bomen herkent en hun gezondheid voorspelt,
gebruikmakend van Python en PyTorch.
- **Dashboard**: Ontwikkel een uitgebreid dashboard met Plotly Dash, waarin gebruikers de resultaten kunnen bekijken en navigeren. Zorg voor een interactieve en gebruiksvriendelijke interface.
=======
- **Dashboard**: Ontwikkel een uitgebreid dashboard met Plotly Dash, waarin gebruikers de resultaten kunnen bekijken en navigeren. Zorg voor een interactieve en gebruiksvriendelijke interface.
- **Boom herkenning**: Met behulp van een online library moeten bomen worden gedetecteerd vanlucht foto's.
>>>>>>> 4488035a3a2793cd81b781eed2c76d77e220e1bb
- **Deployment op mini-PC**: Zorg dat het volledige systeem offline werkt en stand-alone kan draaien op een mini-PC met een Linux-besturingssysteem, geschikt voor gebruik tijdens open dagen en evenementen

## Concept

We passen een bestaand model toe dat, op basis van luchtfoto’s en een infraroodlaag, bomen kan detecteren en hun gezondheid kan beoordelen. De dataset die we hiervoor gebruiken, bestaat uit grote JP2-bestanden die niet direct bruikbaar zijn. Daarom converteren we deze bestanden naar kleinere PNG-tiles met behulp van de gdal2tiles-bibliotheek. Dit proces verdeelt de grote afbeeldingen in meerdere kleine tiles die het model kan gebruiken om bomen te detecteren.

Na de detectie van de bomen controleren we de infraroodkleur op de locaties waar bomen zijn gedetecteerd. Hiermee kunnen we beoordelen of een boom gezond is of tekenen van aftakeling vertoont. Op basis van deze gegevens kunnen we bijvoorbeeld statistieken genereren over het aantal gezonde bomen in een bepaalde regio, zoals Brugge.

Voor de visualisatie ontwikkelen we een interactief dashboard in Python met de Dash- en Dash-Leaflet-bibliotheken. Dit dashboard zal verschillende kaartlagen bevatten, waaronder RGB-foto’s, CIR (Color Infrared) beelden, en een kaart die de resultaten van het model toont. Daarnaast biedt het dashboard statistieken over de gezondheid van de bomen. Het doel is een gebruiksvriendelijke en interactieve interface te creëren waarmee iedereen eenvoudig kan werken.

<<<<<<< HEAD
=======
## Mappenstructuur
- [Detectree2Lib](Detectree2Lib/): Alle info over hoe we de library toepassen op ons project. 

>>>>>>> 4488035a3a2793cd81b781eed2c76d77e220e1bb
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
