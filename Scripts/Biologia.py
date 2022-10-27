# from osgeo import ogr
# import os
# from rasterstats import zonal_stats
# import rasterio
# import numpy as np
# import pandas as pd
# import geopandas as gpd
# import glob
# from osgeo import gdal
# from Scripts.csv2tableau import *
#
# #importar raster (clipped) para cálculo de anomalías
# general_path = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI'
# BinarioPrioridad = general_path + '\\Datos\\Biologia\\BinarioPrioridad.tif'
# Match_2021MapB_Prioridad = general_path + '\\Datos\\Biologia\\Match_2021MapB_Prioridad.tif'
# shp_path = general_path + "\\Datos\\Shps\\Cursos_Otto4ZonalStats2_intersect.shp"
#
# input_raster1 = rasterio.open(BinarioPrioridad)
# tif_array1 = input_raster1.read(1)
# affine1 = input_raster1.transform
#
# input_raster2 = rasterio.open(Match_2021MapB_Prioridad)
# array_mapbiomas = input_raster2.read(1)
# affine2 = input_raster2.transform
#
# stats = zonal_stats(shp_path, tif_array1, affine=affine1, categorical=True)  # se asignan los valores maximos en la intersección con el shapefile
# stats2 = zonal_stats(shp_path, array_mapbiomas, affine=affine2, categorical=True)  # se asignan los valores maximos en la intersección con el shapefile
#
# statsb = pd.DataFrame(stats) #bina
# stats2b = pd.DataFrame(stats2)


from osgeo import gdal,gdal_array
import numpy.ma as ma
import numpy as np
from rasterstats import zonal_stats
import rasterio
import glob
import geopandas as gpd
import pandas as pd
from Scripts.csv2tableau import *

from osgeo import gdal

general_path = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI'
Mapbiomas_folder ='C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI\\Datos\\Mapbiomas\\'
list = glob.glob(Mapbiomas_folder + '*.tif')
PrioBiologica = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI\\Datos\\Biologia\\Prioridad_masked.tif'
shp_path = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI\\Datos\\Shps\\Cuencas_Pfastetternivel10.shp'
path_out2 = general_path + '\\csv_intermedio\\' #Aquí se escribirán los csvs intermedios
path_out2b = general_path + '\\shps_intermedio\\' #Aquí se escribirán los csvs intermedios
path_out3 = general_path + '\\csv_tableau\\' #Aquí se escribirá el csv unificado para tableau
shp = gpd.read_file(shp_path)

input_raster = rasterio.open(PrioBiologica)
arr_prioridad = input_raster.read(1)

for i in list:
    anho = i.split('\\')[-1].split('.')[-2]
    input_raster2 = rasterio.open(i)
    array_mapbiomas = input_raster2.read(1)
    affine = input_raster2.transform

    #cálculo del puntaje sobre conectibidad biológica
    stats = zonal_stats(shp_path, array_mapbiomas , affine=affine2,stats=["mean"],all_touched=True)
    #convertir raster mapbiomas a binario
    array_mapbiomas[(array_mapbiomas == 3),(array_mapbiomas == 11),(array_mapbiomas == 12)] = 1
    array_mapbiomas[(array_mapbiomas != 1)] = 0

    #cáclulo de puntaje
    array_puntajebiologia = ma.masked_array(arr_prioridad, mask=array_mapbiomas) * -10 + 10
    array_puntajebiologia = ma.masked_array(array_puntajebiologia.data, mask=np.invert(array_puntajebiologia.mask) * 1) * 10
    array_puntajebiologia[(array_puntajebiologia < 0),(array_puntajebiologia > 10)] = -9999

    # tif a shp cuenca otto nivel 10
    stats_bio = zonal_stats(shp_path, array_puntajebiologia, affine=affine, categorical=True)
    stats2_bio = pd.DataFrame(stats_bio)
    shp['mean'] = stats2_bio
    shp2 = shp[["nunivo_10", "mean"]]

    shp2.to_csv(path_out2 + 'Smithsonian_PuntBiologia_' + anho + '.csv')

#compilacion de csv para tableau
csv2tbl(path_out3,'Smithsonian', path_out2)