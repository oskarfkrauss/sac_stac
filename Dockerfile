FROM continuumio/miniconda3:4.7.12

LABEL maintainer="Oskar Fraser-Krauss"

RUN apt-get update \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

RUN conda update conda --quiet --yes \
    && conda clean --all -f -y \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

RUN conda install --quiet --yes \
    boto3 \
    geopandas \
    hdmedians \
    matplotlib \
    pandas \
    pyyaml \
    rasterio \
    requests \
    scikit-learn \
    xarray \
    && conda clean --all -f -y \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

RUN pip install --no-cache-dir \
    asynchronousfilereader \
    redis \
    salem \
    sklearn-xarray \
    rioxarray \
    google-cloud-storage \
    sentinelsat \
    descartes \
    sedas_pyapi \
    usgs \
    ipynb \
    pystac \
    xmltodict \
    landsatxplore

# ------------------------------------------

RUN conda install --quiet --yes \
    jupyterlab \
    notebook \
    && conda clean --all -f -y \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

CMD jupyter lab \
    --allow-root \
    --notebook-dir=/opt/notebooks \
    --NotebookApp.ip='0.0.0.0' \
    --NotebookApp.port='8888' \
    --NotebookApp.token='secretpassword' \
    --NotebookApp.open_browser='False'
    