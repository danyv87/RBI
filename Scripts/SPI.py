from Scripts.SPI_funciones import *
from Scripts.csv2tableau import *

#descomentar solo las funciones a emplear

#download data from chirps
#path_out = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\Proyectos\\RBI\\Datos\\Chirps\\Chirps\\'
#def download_annual_chirps(1981,2021,path_out)

#definir paths
local_user = 'danielal'
shpcuenca = 'C:\\Users\\'+ local_user + '\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Varios\\Ottopfasteter nivel 10.shp'
generalpath = 'C:\\Users\\'+ local_user + '\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI'
pathtif_folder = generalpath + '\\Datos\\Chirps\\Chirps\\'
path_tifUTM_folder = generalpath + '\\Datos\\Chirps\\ChirpsUTM\\' #Aquí se encuentran los tiffs de chirps convertidos a UTM
path_clipped = generalpath + '\\Datos\\Chirps\\ChirpsUTM_clipped\\' #Aquí se escribirán los tiffs de chirps cortados al extent de la RBI
path_csv_interm = generalpath + '\\csv_intermedio\\' #Aquí se escribirán los csvs intermedios
path_csv_tableau = generalpath + '\\csv_tableau\\' #Aquí se escribirá el csv unificado para tableau

#reproject
#reproject_tif(pathtif_folder,path_tifUTM_folder)

#Clip y estadísticas
#clip_tif(path_tifUTM_folder,path_clipped)

#calcular media para anomalías
stats, stats2b = media_anomalia(shpcuenca,path_clipped,1981,2010)

#cálculo de anomalías, desde anho_inicio en adelante y conversión a csv
cal_anomalia(shpcuenca,path_clipped,2014,stats,stats2b,path_csv_interm)

#Unificación de csv para tableau
csv2tbl(path_csv_interm,'CHIRPS', path_csv_tableau)