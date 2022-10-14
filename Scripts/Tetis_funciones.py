#cálculo de anomalías
import pandas as pd
import os
import rasterio
from rasterstats import zonal_stats
import numpy as np
from affine import Affine
import geopandas as gpd

def rasterioimport(path):
    input_raster = rasterio.open(path)
    tif_array = input_raster.read(1)
    affine = input_raster.transform
    input_raster = None
    return tif_array, affine

def zonal_stats_RBI(shp,tif_array,affine,nodata,path_out,ID,variable,anho,escribir_noescribircsv):
    stats2 = zonal_stats(shp, tif_array, affine=affine, stats=["mean"], nodata=-9999,
                         all_touched=True)  # se asignan los valores medios en la intersección con el shapefile
    stats2 = pd.DataFrame(stats2)
    shp['mean'] = stats2
    shp2 = shp[['nunivo_10', 'mean']]
    if escribir_noescribircsv == 'escribircsv':
        shp2.to_csv(path_out + 'TETIS_' + variable + '_' + anho + '.csv')
    return shp2

def tetis(shpcuenca,input_bulkdensity,path_OutputASC_tetis,list_var,path_out):
    # agrupacion de archivos por Fuente de datos
    os.listdir(path_OutputASC_tetis)
    shp_Otto10 = gpd.read_file(os.path.dirname(shpcuenca)) #Otto nivel 10
    # importar archivos de bulkdensity para cálculo de tasa de erosión con variable P4
    tif_array_bulk, affine_bulk = rasterioimport(input_bulkdensity)
    stats_bulk = zonal_stats_RBI(shp_Otto10, tif_array_bulk, affine_bulk, -9999, path_out, 'TETIS', '_', 00,
                                 'noescribircsv')
    for x in os.listdir(path_OutputASC_tetis):
        variable, anho = x.split('_')
        if variable in list_var:
            #importar output TETIS
            tif_array_TETIS, affine_TETIS = rasterioimport(path_OutputASC_tetis + x)
            # cálculo de estadísticas sobre los resultados del TETIS
            stats_TETIS = zonal_stats_RBI(shp_Otto10, tif_array_TETIS, affine_TETIS, -9999, path_out,'TETIS', variable, anho[:4],'escribircsv')
            # clasificación por tasa de erosión
            if variable == "P4":
                # operación para conversión de erosión en m3 a TN/Ha
                ErosionTNperHa = stats_bulk['mean'] * 1 / (270 * 270 / 1000) * stats_TETIS['mean']
                shp_Otto10['mean'] = ErosionTNperHa * -1
                shp_Otto10_v2 = shp_Otto10[['nunivo_10', 'mean']]
                shp_Otto10_v2.to_csv(path_out + 'TETIS' + '_' + 'ErosionTNperHa' + '_' + anho[:4] + '.csv')
                print(variable + anho[:4])
                #transformar de acumulado a incremental
                if anho[:4] != '2014':
                    df = pd.read_csv(path_out + 'TETIS' + '_' + 'ErosionTNperHa' + '_' + str(int(anho[:4])-1) + '.csv') #año anterior para posterior resta del acumulado
                    ErosionTNperHa = shp_Otto10['mean'] - df['mean']
                    shp_Otto10['mean'] = ErosionTNperHa
                    shp_Otto10_v3 = shp_Otto10[['nunivo_10', 'mean']]
                    shp_Otto10_v3.to_csv(path_out + 'TETIS' + '_ErosionTNperHa_' + anho[:4] + '.csv')
                    df = None

                # Clasificacion = {
                #     'Class': ['Muy leve', 'Ligero', 'Moderado', 'Alto', 'Severo', 'Muy severo', 'Catastrófico'],
                #     'Erosion rate (t/ha)': ['<2', '2–5', '5–10', '10–50', '50–100', '100–500', '>500']}
                #
                shp_Otto10.loc[(shp_Otto10['mean'] > 2), 'RatioErosion'] = 'Muy leve'
                shp_Otto10.loc[(shp_Otto10['mean'] > 2) & (shp_Otto10['mean'] < 5), 'RatioErosion'] = 'Ligero'
                shp_Otto10.loc[(shp_Otto10['mean'] > 5) & (shp_Otto10['mean'] < 10), 'RatioErosion'] = 'Moderado'
                shp_Otto10.loc[(shp_Otto10['mean'] > 10) & (shp_Otto10['mean'] < 50), 'RatioErosion'] = 'Alto'
                shp_Otto10.loc[(shp_Otto10['mean'] > 50) & (shp_Otto10['mean'] < 100), 'RatioErosion'] = 'Severo'
                shp_Otto10.loc[(shp_Otto10['mean'] > 100) & (shp_Otto10['mean'] < 500), 'RatioErosion'] = 'Muy severo'
                shp_Otto10.loc[(shp_Otto10['mean'] > 500), 'RatioErosion'] = 'Catastrofico'

                shp5 = shp_Otto10[['nunivo_10', 'RatioErosion']]
                shp5b=shp5.rename(columns={'RatioErosion': 'mean'})
                shp5b.to_csv(path_out + 'TETIS' + '_RatioErosion_' + anho[:4] + '.csv')

                ## Tags a puntaje
                shp_Otto10.loc[shp_Otto10['RatioErosion'] == "Muy leve", 'RatioPuntaje'] = 10
                shp_Otto10.loc[shp_Otto10['RatioErosion'] == "Ligero", 'RatioPuntaje'] = 9
                shp_Otto10.loc[shp_Otto10['RatioErosion'] == "Moderado", 'RatioPuntaje'] = 8
                shp_Otto10.loc[shp_Otto10['RatioErosion'] == "Alto", 'RatioPuntaje'] = 5
                shp_Otto10.loc[shp_Otto10['RatioErosion'] == "Severo", 'RatioPuntaje'] = 4
                shp_Otto10.loc[shp_Otto10['RatioErosion'] == "Muy severo", 'RatioPuntaje'] = 3
                shp_Otto10.loc[shp_Otto10['RatioErosion'] == "Catastrofico", 'RatioPuntaje'] = 1

                shp6 = shp_Otto10[['nunivo_10', 'RatioPuntaje']]
                shp6b = shp6.rename(columns={'RatioPuntaje': 'mean'})
                shp6b.to_csv(path_out + 'TETIS' + '_RatioPuntaje_' + anho[:4] + '.csv')

