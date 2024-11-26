# Code

## Vereisten

Je hebt Python op je pc nodig en de volgende bibliotheken:
- Dash
- Dash-Leaflet
- Flask

De eenvoudigste manier om ze te installeren is door de volgende opdracht in de terminal uit te voeren.
```
$pip install dash dash-leaflet flask pandas
```

## Installatie

Je kunt de code installeren door de repository te clonen.

## Gebruik

Om de code te gebruiken, moet je eerst een dataset verkrijgen. De dataset die we hebben gebruikt komt van [Vlaanderen.be](https://download.vlaanderen.be/product/9531). Nadat je de dataset hebt gedownload, moet je deze omzetten naar tegels (tiles) met de volgende opdracht.

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
Je zou de infrarode tegels (infrared tiles) in de CIR-map moeten plaatsen en de RGB- tegels in de RGB-map. Daarna kun je `multipleLayers.py` uitvoeren.

## Tiles Brugge dataset

De tiles kunnen ook gedownload worden via deze link: [Kaggle.com](https://kaggle.com/datasets/aee5a2ae97dd59ebb42c70f3fcc3bbfafbba3aab6f5d182c5d81d81d72f3c07d).