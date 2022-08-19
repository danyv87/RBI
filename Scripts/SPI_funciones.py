import glob, os, rasterio
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import pandas as pd
from rasterstats import zonal_stats
from osgeo import gdal
from affine import Affine

#Clip y estadísticas
def clip_tif(path_tifUTM_folder, path_out):
    list2 = glob.glob(path_tifUTM_folder)
    precip_hist={}
    for i in list2:
        input_raster = gdal.Open(i)
        tif_array = input_raster.ReadAsArray()
        extentRBI = [665948.6204440884757787, 7365749.4827523939311504, 782246.8822151946369559,
                     7175974.1674450952559710]  # Area de influencia margen derecha
        input_raster2 = gdal.Translate(path_out + i[-8:], input_raster, projWin=extentRBI)
        precip_hist[i[-8:]]=tif_array
        input_raster2 = None
    print("listo")

#calcular media para anomalías
def media_anomalia(shpcuenca,ChirpsUTM_clipped_folder):
    list3 = glob.glob(ChirpsUTM_clipped_folder)
    shp = gpd.read_file(os.path.dirname(shpcuenca))
    sum=np.empty((27,17))
    precip_hist = {}
    for i in list3:
         input_raster = gdal.Open(i)
         tif_array = input_raster.ReadAsArray()
         precip_hist[i[-8:-4]] = tif_array
         affine2 = input_raster.GetGeoTransform()
         input_raster = None
         sum = precip_hist[i[-8:-4]] + sum
    mean = sum/len(precip_hist)
    new_affine2 = Affine(affine2[1],affine2[2],affine2[0],affine2[4],affine2[5],affine2[3])
    stats = zonal_stats(shp, tif_array, affine=new_affine2, stats=["max"], all_touched=True)  # se asignan los valores maximos en la intersección con el shapefile
    stats = pd.DataFrame(stats)
    return stats
    print("listo")

#cálculo de anomalías
def cal_anomalia(shpcuenca,ChirpsUTM_clipped_folder,anho_inicio,stats,path_out):
    list3 = glob.glob(ChirpsUTM_clipped_folder)
    shp = gpd.read_file(os.path.dirname(shpcuenca))
    for i in list3:
        if int(i[-8:-4]) >= anho_inicio:
            #importar raster (clipped) para cálculo de anomalías
            input_raster = rasterio.open(i)
            tif_array = input_raster.read(1)
            tif_array_flipped = np.flipud(tif_array)
            affine = input_raster.transform
            input_raster = None
            #correcciones de affine
            new_affine2 = Affine(affine[0], affine[1], affine[2], affine[3], affine[4], affine[5])
            #cálculo de estadísticas
            stats2 = zonal_stats(shp, tif_array, affine=new_affine2, stats=["max"], all_touched=True)  # se asignan los valores maximos en la intersección con el shapefile
            stats2 = pd.DataFrame(stats2)
            anomalia = stats2 - stats
            #asignar resultados del cálculo de anomalía al shapefile y exportar como csv
            shp['max'] = anomalia['max']
            shp.to_csv(path_out + i[-8:-4] + '_zonal.csv')