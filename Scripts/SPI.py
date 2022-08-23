# #Cálculo del índice SPI Standard precipitation index
# Insumo para índices hidrológicos de la RBI

from Scripts.SPI_funciones import *
from Scripts.csv2tableau import *

#descomentar solo las funciones a emplear

#download data from chirps
#path_out = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\Proyectos\\RBI\\Datos\\Chirps\\Chirps\\'
#def download_annual_chirps(1981,2021,path_out)

#definir paths
shpcuenca = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Varios\\Ottopfasteter nivel 10.shp'
generalpath = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI'
pathtif_folder = generalpath + '\\Datos\\Chirps\\Chirps\\'
path_tifUTM_folder = generalpath + '\\Datos\\Chirps\\ChirpsUTM\\' #Aquí se encuentran los tiffs de chirps convertidos a UTM
path_out1 = generalpath + '\\Datos\\Chirps\\ChirpsUTM_clipped\\' #Aquí se escribirán los tiffs de chirps cortados al extent de la RBI
path_out2 = generalpath + '\\csv_intermedio\\' #Aquí se escribirán los csvs intermedios
path_out3 = generalpath + '\\csv_tableau\\' #Aquí se escribirá el csv unificado para tableau

#reproject
reproject_tif(pathtif_folder,path_tifUTM_folder)

#Clip
clip_tif(path_tifUTM_folder, path_out1)

#calcular media para anomalías
stats = media_anomalia(shpcuenca,path_out1,1981,2010)

#cálculo de anomalías, desde anho_inicio en adelante y conversión a csv
cal_anomalia(shpcuenca,path_out1+ '*.tif',2001,stats,path_out2)

#Unificación de csv para tableau
csv2tbl(path_out2,'CHIRPS', path_out3)


