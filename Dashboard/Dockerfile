# Starten met python3.12.3 image
FROM python:3.12.3

WORKDIR /data

# Installeer dependencies
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy the tiles and assets
COPY ./tiles ./tiles
COPY ./assets ./assets
COPY ../Detectree2lib/Own_Tiles ./Own_Tiles

# Copy the application code and the tree pattern
COPY multipleLayers.py /data/
COPY tree_pattern.avif /data/
COPY data.py /data/

# Geef de poort weer waarop de app draait
EXPOSE 8050

# Start een interactieve shell bij het opstarten
CMD ["python", "multipleLayers.py"]