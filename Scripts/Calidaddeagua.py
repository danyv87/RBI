# #Procedimiento para transformación de datos de la BD IB-CEMIT a tableau
# Insumo para índices de calidad de agua de la RBI

import os
from Scripts.Calidaddeagua_funciones import calagua

#definir paths
absolute_path = os.path.abspath(__file__)
general_path = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI'
path_CEMITBD= os.path.dirname(absolute_path) + "\\Serie_temporal_Full_Data_data (1).csv"
shp_path = general_path + "\\Shps\\Cursos_Otto4ZonalStats2_intersect.shp"
path_out= general_path + '\\csv_intermedio\\'


calagua(shp_path,path_CEMITBD,path_out)