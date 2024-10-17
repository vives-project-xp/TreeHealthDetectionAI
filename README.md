# TreeHealthDetectionAI

## Het team

- Robbe De Wispelaere
- Colin Bossuyt
- Niels Denoo

## Beschrijving van project

- **Dataverzameling**: Zoek de nodige luchtfoto's en infraroodkaarten van Vlaanderen. Deze zijn beschikbaar via online bronnen, maar ook bij VIVES-collega's in Roeselare.
- **Dataset opbouw**: Annoteer een groot aantal bomen om een gelabelde dataset op te
bouwen. Dit proces kan deels geautomatiseerd worden met bestaande modellen, zoals 'Segment Anything'. Onderzoek ook bestaande labeling tools om het annotatieproces te versnellen.
- **Modelontwikkeling**: Train een model dat bomen herkent en hun gezondheid voorspelt,
gebruikmakend van Python en PyTorch.
- **Dashboard**: Ontwikkel een uitgebreid dashboard met Plotly Dash, waarin gebruikers de resultaten kunnen bekijken en navigeren. Zorg voor een interactieve en gebruiksvriendelijke interface.
- **Deployment op mini-PC**: Zorg dat het volledige systeem offline werkt en stand-alone kan draaien op een mini-PC met een Linux-besturingssysteem, geschikt voor gebruik tijdens open dagen en evenementen

## Dataset

[Vlaanderen.be](https://download.vlaanderen.be/product/9531) 

## Concept

- Dataset van [vlaanderen.be](#dataset) gebruiken voor AI-training om bomen te detecteren en gezondheid te beoordelen.
- GDAL2Tiles wordt gebruik om jp2-bestanden te converteren naar kleinere png-bestanden.
- AI-training via Detectree2 library en de png-bestanden.
- Dashboard ontwikkelen in Python met Dash en Dash-Leaflet.
- png-bestanden als tiles inzetten op het dashboard.
- Dashboard toont:
  - RGB-kaart
  - Infraroodkaart
  - Kaart met AI-resultaten.