# Detectree2Lib

Om de Detectree2Lib te gebruiken, moet je verschillende stappen volgen. Deze stappen worden hieronder beschreven. De code die wij hebben geschreven zorgt er voor dat het model kan worden toegepast in verschillende mappen binnen een map.

## Extra map toevoegen

Zorg ervoor dat de map **/Own_Tiles** aanwezig is in de **/Detectree2Lib** directory. Als je de naam van deze map wilt veranderen, kun je dit aanpassen in de `result.py` file. Specifiek moet je de `tiles_path`, `output_folder` en `input_folder` variabele aanpassen naar de nieuwe naam. **Dit is de map waar de Tiles moeten komen te staan**.

## Model toepassen

Het is de bedoeling dat je een voorgetraind model downloadt [via deze link](https://zenodo.org/records/12773341). Nadat je de **.pth** file hebt gedownload, zet je deze in de **/Detectree2Lib** map. (Als je meer info wilt zien over de modellen klik [hier](docs/) we hebben deze allemaal getest). Zorg er ook dat in de `result.py` code het juiste pad naar het modelbestand is gedefinieerd. Dit kan worden aangepast in de volgende regel:

```bash
trained_model = "./urban_trees_Cambridge_20230630.pth"
```

## Werken in docker container

Om in de Docker-container te kunnen werken, moet je de volgende twee commando's uitvoeren. Zorg ervoor dat je in de juiste directory bent, namelijk de Detectree2Lib map, voordat je de commando's uitvoert.

### Stap 1: Docker-image bouwen

Het eerste commando bouwt het Docker-image op basis van de `Dockerfile` in je huidige directory. Dit commando moet worden uitgevoerd vanuit de **Detectree2Lib** map:

```bash
sudo docker build -t treedetection .
```

Dit commando maakt het image met de naam **treedetection**. Het kan enige tijd duren, afhankelijk van de grootte van de image en de hoeveelheid werk die nodig is om deze te bouwen.

### Stap 2: Docker-container uitvoeren

Het tweede commando start een interactieve Docker-container op basis van het eerder gebouwde image. Het maakt gebruik van de optie `-v "$(pwd):/data"`, die de huidige directory (waar je werkt) koppelt aan de **/data** directory binnen de container. Dit maakt het mogelijk om bestanden tussen je host en de container te delen.

```bash
sudo docker run -it -v "$(pwd):/data" treedetection
```

Na het uitvoeren van dit commando kom je in de container terecht en kun je werken met de bestanden in je huidige directory, zoals als je lokaal zou werken.

### Link to GitHub

[https://github.com/PatBall1/detectree2](https://github.com/PatBall1/detectree2).
