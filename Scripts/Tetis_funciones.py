#cálculo de anomalías
import pandas as pd
import os
import rasterio
from rasterstats import zonal_stats
import numpy as np
from affine import Affine
import geopandas as gpd

def tetis(shpcuenca,path_OutputASC_tetis,list_var,path_out):
    # agrupacion de archivos por Fuente de datos
    os.listdir(path_OutputASC_tetis)
    shp = gpd.read_file(os.path.dirname(shpcuenca))
    for x in os.listdir(path_OutputASC_tetis):
        variable, anho = x.split('_')
        if variable in list_var:
            input_raster = rasterio.open(path_OutputASC_tetis + x)
            tif_array = input_raster.read(1)
            tif_array_flipped = np.flipud(tif_array)
            affine = input_raster.transform
            # correcciones de affine
            new_affine2 = Affine(affine.a, affine.b, affine.c,affine.d, affine.e*-1, affine.f + (affine.e * (input_raster.read(1).shape[0]-1))) # leer https://github.com/perrygeo/python-rasterstats/issues/98
            # cálculo de estadísticas
            stats2 = zonal_stats(shp, tif_array, affine=affine, stats=["max"],
                                 all_touched=True)  # se asignan los valores maximos en la intersección con el shapefile
            stats2 = pd.DataFrame(stats2)
            shp['max'] = stats2
            shp2 = shp[['nunivo_10', 'max']]
            shp2.to_csv(path_out + 'TETIS_' + variable + '_' + anho[:4] + '.csv')
            input_raster = None
