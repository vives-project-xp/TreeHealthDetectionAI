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

## Mappen structuur

De uitvoermap (output folder) zou er ongeveer als volgt uit moeten zien:

```
tiles/
    rgb/
    cir/
    Collor_Tiles/
    Processed_Tiles/
```

Controleer ook zelf of de paths kloppen.
Je zou de infrarode tegels (infrared tiles) in de CIR-map moeten plaatsen en de RGB- tegels in de RGB-map.

## Samenvoegen van Geojsons en png

Hiervoor zijn 2 scripts geschreven **merge.py** en **mergCollor.py** puur omdat dit map gewijs anders is. Dit wordt gedaan zodat je de geosjon kunt zien op een png foto. 


