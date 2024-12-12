# Code

## Vereisten

Je hebt Python op je pc nodig en de volgende bibliotheken:

- Dash
- Dash-Leaflet
- Flask
- pandas

Deze worden allemaal geïnstalleerd in de Dockerfile

## Installatie

Je kunt de code installeren door de repository te clonen. Vervolgens ga je in een terminal van TreeHealthDetectionAI en doe je volgende commando’s:

```bash
sudo docker build -t dashboard .
sudo docker run -p 8050:8050 dashboard
```

Hiermee zou de website aan het runnen zijn en ga je naar <http://0.0.0.0:8050> voor de website te zien.

## Mappen structuur

De map tiles moet je nog toevoegen. Hierin staan alle .png files voor op de map weer te geven. Deze map plaats je in de Dashboard folder.

```bash
tiles/
    rgb/
    cir/
    Collor_Tiles/
    Processed_Tiles/
```

Controleer ook zelf of de paths kloppen.
Je zou de infrarode tegels (infrared tiles) in de CIR-map moeten plaatsen en de RGB- tegels in de RGB-map.

## Samenvoegen van Geojsons en png

Hiervoor zijn 2 scripts geschreven **merge.py** en **mergeCollor.py** puur omdat deze map anders is. Dit wordt gedaan zodat je de geosjon kunt zien op een png foto.
