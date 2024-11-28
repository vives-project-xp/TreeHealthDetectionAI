# Starten met python3.12.3 image
FROM python:3.12.3

WORKDIR /data

# Installeer dependencies
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy the tiles
COPY ./tiles ./tiles

# Copy the application code
COPY multipleLayers.py /data/multipleLayers.py
COPY tree_pattern.avif /data/tree_pattern.avif

# Geef de poort weer waarop de app draait
EXPOSE 8050

# Start een interactieve shell bij het opstarten
CMD ["python", "multipleLayers.py"]