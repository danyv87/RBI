from osgeo import ogr
import os
from rasterstats import zonal_stats
import rasterio
import pandas as pd
import geopandas as gpd
import glob
from osgeo import gdal
from Scripts.csv2tableau import *


# shp_path = general_path + "\\Datos\\Shps\\Cursos_Otto4ZonalStats2_intersect.shp"
# createBuffer(shp_path, 'testbuffer2.shp', 100)

#importar raster (clipped) para cálculo de anomalías
general_path = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI'
Mapbiomas_folder ='C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI\\Datos\\Mapbiomas\\'
Mapbiomas_folder_clipped ='C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI\\Datos\\Mapbiomas\\Clipped\\'
Mapbiomas_folder_warped ='C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI\\Datos\\Mapbiomas\\warp\\'
list = glob.glob(Mapbiomas_folder + '*.tif')
Uso_suelo ="C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\modelo_diario_Carapa_cal\\usosuelo.tif"
shp_path = general_path + "\\Datos\\Shps\\Cursos_Otto4ZonalStats2_intersect.shp"
shp_path2 = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI\\Datos\\Shps\\Cursos_buffered100.shp'
shp_path3 = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI\\Datos\\Shps\\CuerposBuffered100_v2.shp'
shp_path4 = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI\\Datos\\Shps\\Cuencas_Pfastetternivel10.shp'
shp3 = gpd.read_file(shp_path2)

path_out2 = general_path + '\\csv_intermedio\\' #Aquí se escribirán los csvs intermedios
path_out2b = general_path + '\\shps_intermedio\\' #Aquí se escribirán los csvs intermedios
path_out3 = general_path + '\\csv_tableau\\' #Aquí se escribirá el csv unificado para tableau

for i in list:
    año=i.split('\\')[-1].split('.')[-2]
    input_raster = rasterio.open(i)
    tif_array = input_raster.read(1)
    affine = input_raster.transform

    #cálculo de porcentaje de cobertura de bosques con buffer 100m de cursos hídricos
    stats = zonal_stats(shp_path2, tif_array , affine=affine,categorical=True)
    stats2 = pd.DataFrame(stats)
    stats3 = stats2[3]/stats2.sum(axis=1)
    #shp3['mean'] = stats3
    #shp4 = shp3[["cocursodag", "mean"]]

    #cálculo de procentaje de cobertura de bosques con buffer 100m del emblase de la ITAIPU
    stats_emb = zonal_stats(shp_path3, tif_array , affine=affine,categorical=True)
    stats2_emb = pd.DataFrame(stats_emb)
    stats3_emb = stats2_emb[3]/(stats2_emb.sum(axis=1)-stats2_emb[33])
    #shp3['mean'] = stats3_emb
    #shp4_emb = shp3[["cocursodag", "mean"]]

    df_merged=pd.concat([stats3,stats3_emb],axis=1)
    shp3['mean'] = df_merged.max(axis=1)
    shp4 = shp3[["cocursodag", "mean"]]
    shp4.to_csv(path_out2 + 'Mapbiomas_PorcBosqCurso_' + año + '.csv')

    shp3['mean'] = df_merged.max(axis=1)*10 #puntuación
    shp4b = shp3[["cocursodag", "mean"]]


    shp4b.to_csv(path_out2 + 'Mapbiomas_PuntajeBosqProt_' + año + '.csv')
    #shp4_emb.to_csv(path_out2 + 'Mapbiomas_PorcConectEmb_' + año + '.csv')

    #cálculo del % de bosques en cuencas
    #calcula mal!!
    stats_cuenca = zonal_stats(shp_path4, tif_array, affine=affine, categorical=True)
    stats2_cue = pd.DataFrame(stats_cuenca)
    stats3_cue = stats2_cue[3] / (stats2_cue.sum(axis=1))
    shp3['mean'] = stats3_cue
    shp5 = shp3[["cocursodag", "mean"]]
    shp5.to_csv(path_out2 + 'Mapbiomas_PorcBosqCuenca_' + año + '.csv')

#compilacion de csv para tableau
csv2tbl(path_out2,'Mapbiomas', path_out3)

# def reproject_tif(path_in,path_out):
#     list = glob.glob(path_in + '*.tif')
#     for i in list:
#         input_raster = gdal.Open(i)
#         name = i.split('\\')[-1].split('.')[-2]
#         warp = gdal.Warp(path_out + name + '.tif', input_raster, dstSRS='EPSG:32721',xRes=30, yRes=30)
#         warp = None  # Closes the files
#
# #Clip y estadísticas
# def clip_tif(path_in,path_out):
#     list2 = glob.glob(path_in + '*.tif')
#     precip_hist={}
#     for i in list2:
#         input_raster = gdal.Open(i)
#         tif_array = input_raster.ReadAsArray()
#         extentRBI = [665948.6204440884757787, 7365749.4827523939311504, 782246.8822151946369559,
#                      7175974.1674450952559710]  # Area de influencia margen derecha
#         extentIB_MDMI = [668156.7341833900427446,7364195.2830760600045323, 859686.3749881399562582,
#                      7175202.8958083903416991] # Área de influencia margen derecha e izquierda
#         input_raster2 = gdal.Translate(Mapbiomas_folder_warped + i[-8:], input_raster, projWin=extentRBI)
#         precip_hist[i[-8:]]=tif_array
#         input_raster = None
#         input_raster2 = None
#     print("listo 1/4")

# def createBuffer(inputfn, outputBufferfn, bufferDist):
#     inputds = ogr.Open(inputfn)
#     inputlyr = inputds.GetLayer()
#
#     shpdriver = ogr.GetDriverByName('ESRI Shapefile')
#     if os.path.exists(outputBufferfn):
#         shpdriver.DeleteDataSource(outputBufferfn)
#     outputBufferds = shpdriver.CreateDataSource(outputBufferfn)
#     bufferlyr = outputBufferds.CreateLayer(outputBufferfn, geom_type=ogr.wkbPolygon)
#     featureDefn = bufferlyr.GetLayerDefn()
#
#     for feature in inputlyr:
#         ingeom = feature.GetGeometryRef()
#         geomBuffer = ingeom.Buffer(bufferDist)
#
#         outFeature = ogr.Feature(featureDefn)
#         outFeature.SetGeometry(geomBuffer)
#         bufferlyr.CreateFeature(outFeature)
#         outFeature = None


