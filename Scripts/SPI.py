# #Cálculo del índice SPI Standard precipitation index
# Insumo para índices hidrológicos de la RBI

from Scripts.SPI_funciones import *

#definir paths
shpcuenca = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Varios\\Ottopfasteter nivel 10.shp'
generalpath = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI'
path_tifUTM_folder = generalpath + '\\ChirpsUTM\\' + '*.tif'
path_out1 = generalpath + '\\ChirpsUTM_clipped\\'
path_out2 = generalpath + '\\ChirpsCSV\\'

#Clip y estadísticas
clip_tif(path_tifUTM_folder, path_out1)

#calcular media para anomalías
stats = media_anomalia(shpcuenca,path_out1+ '*.tif')

#cálculo de anomalías
cal_anomalia(shpcuenca,path_out1+ '*.tif',2014,stats,path_out2)
