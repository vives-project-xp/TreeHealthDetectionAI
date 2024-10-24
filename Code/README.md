# Code

## Requirements

U will need to have python on your pc and the following libraries:
- Dash 
- Dash-Leaflet 
- flask

The easiest way to install them is by doin the following command in the terminal.
```
$pip install dash dash-leaflet flask
```

## Installation

U can install the code by cloning the repository.

## Usage

To use the code u have to first get a dataset. The dataset we used is from [Vlaanderen.be](https://download.vlaanderen.be/product/9531). After u have the dataset u have to convert them into tiles using the command.

```
$gdal2tiles.py input.jp2 output_folder
```

The output folder should have look similair to this.

```
tiles/
    rgb/
    cir/
```

U should put the infrared tiles in the CIR folder and the rgb tiles in the RGB folder.
After that u run multipleLayers.py