<<<<<<< HEAD
FROM continuumio/miniconda3:4.7.12

LABEL maintainer="Oskar Fraser-Krauss"

RUN apt-get update \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip
=======
  
FROM continuumio/miniconda3:4.8.2

LABEL maintainer="Tom Jones"
>>>>>>> 96fded2fb53c372112a05f422b20e6b9156ebd22

RUN conda update conda --quiet --yes \
    && conda clean --all -f -y \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

RUN conda install --quiet --yes \
<<<<<<< HEAD
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
=======
	-c conda-forge \
	gdal==3.1.4 \
    boto3 \
    pyyaml \
    rasterio \
    pip \
    && conda clean --all -f -y \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

RUN conda install --quiet --yes -c fastai nbdev \
>>>>>>> 96fded2fb53c372112a05f422b20e6b9156ebd22
    && conda clean --all -f -y \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

<<<<<<< HEAD
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
=======
RUN apt-get update --yes

RUN apt-get install ruby-full build-essential zlib1g-dev --yes
RUN echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
RUN echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
RUN echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
# RUN source ~/.bashrc

RUN pip install --no-cache-dir \
    redis  \
	nbconvert==5.6.1 \
	requests \
	pystac[validation] \
	shapely \
	sedas_pyapi \
	geopandas \
	xmltodict

RUN apt install htop
>>>>>>> 96fded2fb53c372112a05f422b20e6b9156ebd22

RUN conda install --quiet --yes \
    jupyterlab \
    notebook \
    && conda clean --all -f -y \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

<<<<<<< HEAD
=======
RUN conda install --quiet --yes -c conda-forge nodejs intake-stac

RUN jupyter labextension install @jupyterlab/toc
RUN jupyter labextension install @aquirdturtle/collapsible_headings

>>>>>>> 96fded2fb53c372112a05f422b20e6b9156ebd22
CMD jupyter lab \
    --allow-root \
    --notebook-dir=/opt/notebooks \
    --NotebookApp.ip='0.0.0.0' \
    --NotebookApp.port='8888' \
    --NotebookApp.token='secretpassword' \
<<<<<<< HEAD
    --NotebookApp.open_browser='False'
=======
    --NotebookApp.open_browser='False' \
	--NotebookApp.allow_hidden='True'
>>>>>>> 96fded2fb53c372112a05f422b20e6b9156ebd22
