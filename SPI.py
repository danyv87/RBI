#Cálculo del índice SPI Standard precipitation index

from netCDF4 import Dataset as NetCDFFile
import matplotlib.pyplot as plt
import glob
from osgeo import gdal
import geopandas as gpd
import pandas as pd
import os
from rasterstats import zonal_stats
import numpy as np
from affine import Affine
import rasterio

path = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI\\'
path_shp = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Varios\\Ottopfasteter nivel 10.shp'
list = glob.glob(path + 'Chirps\\' + '*.tif')
list2 = glob.glob(path + 'ChirpsUTM\\' + '*.tif')
list3 = glob.glob(path + 'ChirpsUTM_clipped\\' + '*.tif')

#Clip y estadísticas
shp = gpd.read_file(os.path.dirname(path_shp))
precip_hist={}
# for i in list2:
#     input_raster = gdal.Open(i)
#     tif_array = input_raster.ReadAsArray()
#     extentRBI = [665948.6204440884757787, 7365749.4827523939311504, 782246.8822151946369559,
#                  7175974.1674450952559710]  # Area de influencia margen derecha
#     input_raster2 = gdal.Translate(path + 'ChirpsUTM_clipped\\' + i[-8:], input_raster, projWin=extentRBI)
#     precip_hist[i[-8:]]=tif_array
#     input_raster2 = None

#calcular media para anomalías
sum=np.empty((27,17))
for i in list3:
     input_raster = gdal.Open(i)
     tif_array = input_raster.ReadAsArray()
     precip_hist[i[-8:-4]] = tif_array
     input_raster = None
     sum = precip_hist[i[-8:-4]] + sum
mean = sum/len(precip_hist)

#cálculo de anomalías
for i in list3:
    if int(i[-8:-4]) >= 2014:
        #importar raster (clipped) para cálculo de anomalías
        input_raster = rasterio.open(i)
        tif_array = input_raster.read(1)
        tif_array_flipped = np.flipud(tif_array)
        affine = input_raster.transform
        input_raster = None
        #correcciones de affine
        new_affine = Affine(affine[1], affine[2], affine[0], affine[4], affine[5]*-1, affine[3] + (affine[5] * (tif_array.shape[0]-1)))
        new_affine2 = Affine(affine[0], affine[1], affine[2], affine[3], affine[4], affine[5])
        #cálculo de estadísticas
        stats = zonal_stats(shp, tif_array, affine=new_affine2, stats=["max"], all_touched=True)  # se asignan los valores maximos en la intersección con el shapefile
        anomalia = mean - stats
        anomalia = pd.DataFrame(anomalia)
        #asignar resultados del cálculo de anomalía al shapefile y exportar como csv
        shp['max'] = anomalia['max']
        shp.to_csv(path + 'ChirpsCSV\\' + i[-8:-4] + '_zonal.csv')


