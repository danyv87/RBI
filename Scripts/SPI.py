# #Cálculo del índice SPI Standard precipitation index
# Insumo para índices hidrológicos de la RBI

from Scripts.SPI_funciones import *
from Scripts.csv2tableau import *

#definir paths
shpcuenca = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Varios\\Ottopfasteter nivel 10.shp'
generalpath = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI'
path_tifUTM_folder = generalpath + '\\ChirpsUTM\\' + '*.tif' #Aquí se encuentran los tiffs de chirps convertidos a UTM
path_out1 = generalpath + '\\ChirpsUTM_clipped\\' #Aquí se escribirán los tiffs de chirps cortados al extent de la RBI
path_out2 = generalpath + '\\ChirpsCSV\\' #Aquí se escribirán los csvs intermedios
path_out3 = generalpath + '\\Chirps_tableau\\' #Aquí se escribirá el csv unificado para tableau

#Clip y estadísticas
clip_tif(path_tifUTM_folder, path_out1)

#calcular media para anomalías
stats = media_anomalia(shpcuenca,path_out1+ '*.tif',1981,2021)

#cálculo de anomalías, desde anho_inicio en adelante y conversión a csv
cal_anomalia(shpcuenca,path_out1+ '*.tif',2014,stats,path_out2)

#Unificación de csv para tableau
csv2tbl(path_out2,'CHIRPS', path_out3)