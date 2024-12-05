# Code

## Vereisten

Je hebt Python op je pc nodig en de volgende bibliotheken:
- Dash
- Dash-Leaflet
- Flask
- pandas

Deze worden allemaal geïnstalleerd in de dockerfile

## Installatie

Je kunt de code installeren door de repository te clonen.
Vervolgens ga je in een integrated terminal van dashboard en doe je volgende commando's

```
sudo docker build -t dashboard .
sudo docker run -p 8050:8050 dashboard
```

Hiermee zou de website aan het runnen zijn en ga je naar http://0.0.0.0:8050 voor de website te zien.

## Tiles Brugge dataset

De tiles kunnen gedownload worden via deze link: [Kaggle.com](https://www.kaggle.com/datasets/robbedewispelaere/treedetection). Dit zijn de tiles voor Brugge, deze staan in de juiste mappen en moet gewoon aan de code toegevoegd worden.

## Andere dataset gebruiken

Als je een andere dataset wil gebruiken of een andere gemeente dan kan je die halen van [Vlaanderen.be](https://download.vlaanderen.be/product/9531). Hier kan je ook de opdeling zien van hoe alle stukken van vlaanderen is opgedeeld. Als je de dataset (het jp2 in de map) gedownload heb ga je deze eerst moet omzetten naar png. Dit doe je door volgende commando.

```
$gdal2tiles.py input.jp2 output_folder
```

De uitvoermap (output folder) zou er ongeveer als volgt uit moeten zien:

```
tiles/
    rgb/
    cir/
```

Controleer ook zelf of de paths kloppen.
Je zou de infrarode tegels (infrared tiles) in de CIR-map moeten plaatsen en de RGB- tegels in de RGB-map.

## Samenvoegen van Geojsons en png

Via het script merge.py is het mogelijk om de laatste laag van de tileset te combineren met de corresponderende geojsons.


