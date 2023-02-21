from Scripts.csv2tableau import *
import glob, os, rasterio
import geopandas as gpd
import pandas as pd
from rasterstats import zonal_stats

#Cálculo de % de cobertura de conexiones de agua potable
#definir paths
local_user = 'C:\\Users\\danielal'
root_path =  '\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos'
shpcuenca = local_user + root_path + '\\RED\\RBI\\Datos\\Shps\\Cuencas_Pfastetternivel10.shp'
generalpath = local_user + root_path +'\\RED\\RBI'
pathtif = generalpath + '\\Datos\\ERSSAN\\Por_Cob_agua.tif'
path_csv_interm= generalpath + '\\csv_intermedio\\'
path_csv_tableau = generalpath + '\\csv_tableau\\' #Aquí se escribirá el csv unificado para tableau

#cargar inputs
shp = gpd.read_file(os.path.dirname(shpcuenca))
input_raster = rasterio.open(pathtif)
tif_array = input_raster.read(1)
affine = input_raster.transform
input_raster = None

#cálculo de estadísticas
stats2 = zonal_stats(shpcuenca, tif_array*10, affine=affine, stats=["mean"], all_touched=True)  # se asignan los valores maximos en la intersección con el shapefile
stats2 = pd.DataFrame(stats2)
shp['mean'] = stats2['mean']
shp2 = shp[['nunivo_10','mean']]

#Asignación de puntajes
shp3 = shp2
shp3.loc[shp3['mean'] >10, 'mean'] = 10 #artificio para corrección de error en bd de ERSSAN
shp3.loc[shp3['mean'] <0, 'mean'] = 0 #artificio para corrección de error en bd de ERSSAN
shp3.to_csv(path_csv_interm + 'ERSSAN_PorcCobAgua_' + "2023" + '.csv')

#Unificación de csv para tableau
csv2tbl(path_csv_interm,'ERSSAN', path_csv_tableau)

