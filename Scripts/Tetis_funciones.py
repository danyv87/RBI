#cálculo de anomalías
import pandas as pd
import os
import rasterio
from rasterstats import zonal_stats
import numpy as np
from affine import Affine
import geopandas as gpd

def tetis(shpcuenca,input_bulkdensity,path_OutputASC_tetis,list_var,path_out):
    # agrupacion de archivos por Fuente de datos
    os.listdir(path_OutputASC_tetis)
    shp = gpd.read_file(os.path.dirname(shpcuenca))
    for x in os.listdir(path_OutputASC_tetis):
        variable, anho = x.split('_')
        if variable in list_var:
            input_raster = rasterio.open(path_OutputASC_tetis + x)
            tif_array = input_raster.read(1)
            affine = input_raster.transform

            # cálculo de estadísticas sobre los resultados del tetis
            stats2 = zonal_stats(shp, tif_array, affine=affine, stats=["mean"],nodata=-9999,
                                 all_touched=True)  # se asignan los valores medios en la intersección con el shapefile
            stats2 = pd.DataFrame(stats2)
            shp['mean'] = stats2
            shp2 = shp[['nunivo_10', 'mean']]
            shp2.to_csv(path_out + 'TETIS_' + variable + '_' + anho[:4] + '.csv')
            input_raster = None

            # importar archivos de bulkdensity
            tif = rasterio.open(input_bulkdensity)
            # adecuar raster a numpy
            tif_array2 = tif.read(1)
            affine2 = tif.transform  # usar este affine

            # clasificación por tasa de erosión
            if variable == "P4":
                # zonal statistics
                stats3 = zonal_stats(shp, tif_array2, affine=affine2, stats=["mean"],nodata=-9999,
                                    all_touched=True)  # se asignan los valores maximos en la intersección con el shapefile
                stats3 = pd.DataFrame(stats3)
                shp['Bulkdensity_mean'] = stats3['mean']

                # operación
                bulkdensity = shp['Bulkdensity_mean']
                ErosionTNperHa = bulkdensity * 1 / (270 * 270 / 1000) * shp2['mean']
                shp['mean'] = ErosionTNperHa * -1 #mean es un campo estandar
                shp4 = shp[['nunivo_10', 'mean']]
                shp4.to_csv(path_out + 'TETIS' + '_ErosionTNperHa_' + anho[:4] + '.csv')

                # Clasificacion = {
                #     'Class': ['Muy leve', 'Ligero', 'Moderado', 'Alto', 'Severo', 'Muy severo', 'Catastrófico'],
                #     'Erosion rate (t/ha)': ['<2', '2–5', '5–10', '10–50', '50–100', '100–500', '>500']}
                #
                # shp.loc[shp['mean'].le(2), 'mean'] = 'Muy leve'
                # shp.loc[shp['mean'].ge(2) & shp['mean'].le(5), 'mean'] = 'Ligero'
                # shp.loc[shp['mean'].ge(5) & shp['mean'].le(10), 'mean'] = 'Moderado'
                # shp.loc[shp['mean'].ge(10) & shp['mean'].le(50), 'mean'] = 'Alto'
                # shp.loc[shp['mean'].ge(50) & shp['mean'].le(100), 'mean'] = 'Severo'
                # shp.loc[shp['mean'].ge(100) & shp['mean'].le(500), 'mean'] = 'Muy severo'
                # shp.loc[shp['mean'].ge(500), 'mean'] = 'Catastrofico'
                #
                # # shp a csv
                # shp5 = shp[['nunivo_10', 'RatioErosion']]
                # shp5.to_csv(path_out + 'TETIS' + '_RatioErosion_' + anho[:4] + '.csv')