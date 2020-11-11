# AUTOGENERATED! DO NOT EDIT! File to edit: 01A_pleiades.ipynb (unless otherwise specified).

__all__ = ['prep_pleiades', 'pleiades_get_dt', 'pleiades_parsemeta', 'pleiades_get_crs', 'pleiades_get_geom',
           'pleiades_get_bbox', 'pleiades_get_gsd', 'pleiades_get_cloudcover', 'pleiades_bands', 'pleiades_band_refs']

# Cell
import os
from glob import glob
import time
import numpy as np
from datetime import datetime
import json

import xmltodict
import pystac
from pystac import STAC_IO
from pystac.extensions.eo import Band
import geopandas as gpd

from .utils import sedas_client, sedas_find_datasets, sedas_download, sedas_extract
from .utils import cogmosaicbands
from .utils import s3_upload_dir, s3_list_objects_paths, clean_up
from .utils import pystac_setIO, create_uri

# Cell
def prep_pleiades(sedas_supplierId, inter_dir="/tmp/data/intermediate/",
                  s3_bucket="public-eo-data", s3_dir="uksa-ssgp/pleiades/"):
    try:
        inter_dir = f"{inter_dir}{sedas_supplierId}_tmp/"
        os.makedirs(inter_dir, exist_ok=True)
        scene_name = sedas_supplierId
        down_zip = f"{inter_dir}{scene_name}.zip"
        scene_dir = f"{down_zip[:-4]}/"
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} Preparing {scene_name} within {inter_dir}")
        # find & download
        sedas_scene_res = sedas_client().search_product(sedas_supplierId)[0]
        sedas_download([sedas_scene_res], inter_dir)
        sedas_extract(down_zip, scene_dir)
        # sensor-specific band mosaicing and cogifying
        imgs_ms = glob(f"{scene_dir}*/*MS_002*/*.TIF")
        imgs_pan = glob(f"{scene_dir}*/*P_001*/*.TIF")
        cogmosaicbands(imgs_pan, 1, imgs_pan[0][:-13])
        cogmosaicbands(imgs_ms, 4, imgs_ms[0][:-13])
        # upload
        s3_upload_dir(scene_dir, s3_bucket, s3_dir)
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} Prepared {scene_name} at {s3_dir}{scene_name}/")
        clean_up(inter_dir)
    except Exception as e:
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} Failed with {e}")
        clean_up(inter_dir)

# Cell
pystac_setIO()

# Cell
def pleiades_get_dt(scene_name):
    return datetime.strptime(scene_name.split('_')[5][:14], '%Y%m%d%H%M%S')

# Cell
def pleiades_parsemeta(scene_name, scene_obj_paths):
    meta_path = [i for i in scene_obj_paths if (i.endswith('.XML')) & (os.path.basename(i).startswith('DIM'))][0]
    return xmltodict.parse(pystac.STAC_IO.read_text(create_uri(meta_path)))

# Cell
def pleiades_get_crs(metadata):
    return int(metadata['Dimap_Document']['Coordinate_Reference_System']['Projected_CRS']['PROJECTED_CRS_NAME'])

# Cell
def pleiades_get_geom(scene_paths):
    roi_path = [i for i in scene_paths if (i.endswith('1_MSK.GML') * os.path.basename(i).startswith('ROI'))][0]
    roi_uri = create_uri(roi_path)
    return json.loads(gpd.read_file(roi_uri).to_crs('EPSG:4326').to_json(show_bbox=True))['features'][0]['geometry']

# Cell
def pleiades_get_bbox(metadata):
    lons = [float(i['LON']) for i in metadata['Dimap_Document']['Dataset_Content']['Dataset_Extent']['Vertex']]
    lats = [float(i['LAT']) for i in metadata['Dimap_Document']['Dataset_Content']['Dataset_Extent']['Vertex']]
    return [min(lons), min(lats), max(lons), max(lats)]

# Cell
def pleiades_get_gsd(metadata):
    across = float(metadata['Dimap_Document']['Geometric_Data']['Use_Area']['Located_Geometric_Values'][0]['Ground_Sample_Distance']['GSD_ACROSS_TRACK']['#text'])
    along = float(metadata['Dimap_Document']['Geometric_Data']['Use_Area']['Located_Geometric_Values'][0]['Ground_Sample_Distance']['GSD_ALONG_TRACK']['#text'])
    return round(( across + along ) / 2, 2)

# Cell
def pleiades_get_cloudcover(metadata):
    return round(float(metadata['Dimap_Document']['Dataset_Content']['CLOUD_COVERAGE']['#text']),2)

# Cell
pleiades_bands = [Band.create(name='Panchromatic', description='Panchromatic: 480 - 830 nm', common_name='pan'),
                  Band.create(name='Blue', description='Blue: 430 - 550 nm', common_name='blue'),
                  Band.create(name='Green', description='Green: 490 - 610 nm', common_name='green'),
                  Band.create(name='Red', description='Red: 600 - 720 nm', common_name='red'),
                  Band.create(name='Near-Infrared', description='Near-Infrared: 750 - 950 nm', common_name='nir')]

# Cell
pleiades_band_refs = {
    'Panchromatic':{'ends':'_band1', 'dif':'_P_', 'id':'B0'},
    'Blue':{'ends':'_band1', 'dif':'_MS_', 'id':'B1'},
    'Green':{'ends':'_band2', 'dif':'_MS_', 'id':'B2'},
    'Red':{'ends':'_band3', 'dif':'_MS_', 'id':'B3'},
    'Near-Infrared':{'ends':'_band4', 'dif':'_MS_', 'id':'B4'}
}