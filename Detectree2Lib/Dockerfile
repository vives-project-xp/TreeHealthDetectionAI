#starten met python 3.10 image
FROM python:3.10

WORKDIR  /data

# Install vereiste libraries
RUN apt-get update && \
    apt-get install -y libgdal-dev gdal-bin libgl1 wget && \
    apt-get clean

# install python packages
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install opencv-python && \
    pip install gdal==3.6.2 && \
    pip install git+https://github.com/PatBall1/detectree2.git

# Download the model    
RUN wget https://zenodo.org/record/10522461/files/230103_randresize_full.pth

#start een interactieve shell bij het opstarten
CMD ["bash"]