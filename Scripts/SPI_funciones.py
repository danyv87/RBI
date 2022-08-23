import glob, os, rasterio
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import pandas as pd
from rasterstats import zonal_stats
from osgeo import gdal
from affine import Affine
import wget
import requests
from bs4 import BeautifulSoup

def download_annual_chirps(anho_ini,anho_fin,path_out):
    url_base = 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_annual/tifs/'
    page = requests.get(url_base)
    soup = BeautifulSoup(page.text, 'html.parser')
    a = soup.find(id='indexlist')
    b = a.find_all('a')
    for a in b:
        anho = a.prettify()[-13:-9]
        if anho.isnumeric():
            if int(anho) in range(anho_ini, anho_fin):
                print(anho)
                filename = wget.download(url_base + list(a)[0], out=path_out)


#Clip y estadísticas
def clip_tif(path_tifUTM_folder, path_out):
    list2 = glob.glob(path_tifUTM_folder)
    precip_hist={}
    for i in list2:
        input_raster = gdal.Open(i)
        tif_array = input_raster.ReadAsArray()
        extentRBI = [665948.6204440884757787, 7365749.4827523939311504, 782246.8822151946369559,
                     7175974.1674450952559710]  # Area de influencia margen derecha
        extentIB_MDMI = [668156.7341833900427446,7364195.2830760600045323, 859686.3749881399562582,
                     7175202.8958083903416991] # Área de influencia margen derecha e izquierda
        input_raster2 = gdal.Translate(path_out + i[-8:], input_raster, projWin=extentIB_MDMI)
        precip_hist[i[-8:]]=tif_array
        input_raster2 = None
    print("listo 1/4")

#calcular media para anomalías
def media_anomalia(shpcuenca,ChirpsUTM_clipped_folder,anho_inicio,anho_fin):
    shp = gpd.read_file(os.path.dirname(shpcuenca))
    list3 = glob.glob(ChirpsUTM_clipped_folder)
    input_raster = gdal.Open(list3[0])
    sum=np.empty((input_raster.RasterYSize,input_raster.RasterXSize))
    input_raster = None
    precip_hist = {}
    i2=0
    for i in list3:
        if int(i[-8:-4]) >= anho_inicio and int(i[-8:-4]) <= anho_fin:
            input_raster = rasterio.open(i)
            tif_array = input_raster.read(1)
            precip_hist[i[-8:-4]] = tif_array
            affine = input_raster.transform
            input_raster = None
            sum = precip_hist[i[-8:-4]] + sum
            i2=i2+1
    mean = sum/i2
    stats = zonal_stats(shp, tif_array, affine=affine, stats=["mean"], all_touched=True)  # se asignan los valores maximos en la intersección con el shapefile
    stats = pd.DataFrame(stats)
    print("listo 2/4")
    return stats


#cálculo de anomalías
def cal_anomalia(shpcuenca,ChirpsUTM_clipped_folder,anho_inicio,stats,path_out):
    list3 = glob.glob(ChirpsUTM_clipped_folder)
    shp = gpd.read_file(os.path.dirname(shpcuenca))
    no=0
    for i in list3:
        if int(i[-8:-4]) >= anho_inicio:
            #importar raster (clipped) para cálculo de anomalías
            input_raster = rasterio.open(i)
            tif_array = input_raster.read(1)
            tif_array_flipped = np.flipud(tif_array)
            affine = input_raster.transform
            input_raster = None
            #cálculo de estadísticas
            stats2 = zonal_stats(shp, tif_array, affine=affine, stats=["mean"], all_touched=True)  # se asignan los valores maximos en la intersección con el shapefile
            stats2 = pd.DataFrame(stats2)
            anomalia = stats2 - stats
            #asignar resultados del cálculo de anomalía al shapefile y exportar como csv
            shp['mean'] = anomalia['mean']
            shp2 = shp[['nunivo_10','mean']]
            shp2.to_csv(path_out + 'CHIRPS_anomalia_' + i[-8:-4] + '.csv')
            no = no + 1
    print("listo 3/4")