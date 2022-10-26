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
# tif_array2 = input_raster2.read(1)
# affine2 = input_raster2.transform
#
# stats = zonal_stats(shp_path, tif_array1, affine=affine1, categorical=True)  # se asignan los valores maximos en la intersección con el shapefile
# stats2 = zonal_stats(shp_path, tif_array2, affine=affine2, categorical=True)  # se asignan los valores maximos en la intersección con el shapefile
#
# statsb = pd.DataFrame(stats) #bina
# stats2b = pd.DataFrame(stats2)


from osgeo import gdal,gdal_array
import numpy.ma as ma
import numpy as np
import matplotlib.pyplot as plt

# Open band 1 as array
ds = gdal.Open('C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI\\Datos\\Biologia\\Mapbiomasbinario.tif')
ds.GetRasterBand(1).SetNoDataValue(-9999)
b1 = ds.GetRasterBand(1)
arr = b1.ReadAsArray()


ds2 = gdal.Open('C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI\\Datos\\Biologia\\Prioridad_masked.tif')
ds2.GetRasterBand(1).SetNoDataValue(-9999)
b2 = ds2.GetRasterBand(1)
arr2 = b2.ReadAsArray()


# apply equation
mx = ma.masked_array(arr2, mask=arr)*-5+5
mx = ma.masked_array(mx.data, mask=np.invert(mx.mask)*1)*5+5
mx[mx<0]=-9999


gdal_array.SaveArray(mx.astype("float32"), 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI\\Datos\\Shps\\puntuacionConectividad_multiplesEspecies2.tif', "GTIFF", ds)
del ds
del ds2