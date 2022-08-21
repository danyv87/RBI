#cálculo de anomalías
import pandas as pd
import os
import rasterio
from rasterstats import zonal_stats
import numpy as np
from affine import Affine
import geopandas as gpd

def tetis(shpcuenca,path_OutputASC_tetis,path_out):
    # agrupacion de archivos por Fuente de datos
    os.listdir(path_OutputASC_tetis)
    shp = gpd.read_file(os.path.dirname(shpcuenca))
    for x in os.listdir(path_OutputASC_tetis):
        variable, anho = x.split('_')
        input_raster = rasterio.open(path_OutputASC_tetis + x)
        tif_array = input_raster.read(1)
        tif_array_flipped = np.flipud(tif_array)
        affine = input_raster.transform
        input_raster = None
        # correcciones de affine
        new_affine2 = Affine(affine[0], affine[1], affine[2], affine[3], affine[4], affine[5])
        # cálculo de estadísticas
        stats2 = zonal_stats(shp, tif_array, affine=new_affine2, stats=["max"],
                             all_touched=True)  # se asignan los valores maximos en la intersección con el shapefile
        stats2 = pd.DataFrame(stats2)
        shp['max'] = stats2
        shp2 = shp[['nunivo_10', 'max']]
        shp2.to_csv(path_out + 'TETIS_' + variable + '_' + anho[:4] + '.csv')
