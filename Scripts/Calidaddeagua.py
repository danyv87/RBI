# #Procedimiento para transformación de datos de la BD IB-CEMIT a tableau
# Insumo para índices de calidad de agua de la RBI

import os
from Scripts.Calidaddeagua_funciones import calagua
from Scripts.csv2tableau import *

#definir paths
absolute_path = os.path.abspath(__file__)
general_path = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI'
path_CEMITBD = general_path + "\\Serie_temporal_Full_Data_data (1).csv"
shp_path = general_path + "\\Datos\\Shps\\Cursos_Otto4ZonalStats2_intersect.shp"
path_out= general_path + '\\csv_intermedio\\'
path_out2= general_path + '\\csv_tableau\\'

#calculos de calidad de agua
calagua(shp_path,path_CEMITBD,path_out)

#eliminar archivos remanentes
test = os.listdir(path_out)
for item in test:
    if not item.endswith(".csv"):
        os.remove(path_out + item)

#compilacion de csv para tableau
csv2tbl(path_out,'CEMIT', path_out2)
