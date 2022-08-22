# #Procedimiento para extraer datos de TETIS
# Insumo para calculo de indice morfologico de la RBI

import os
from Scripts.Tetis_funciones import *
from Scripts.csv2tableau import *

#inputs
shpcuenca = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Varios\\Ottopfasteter nivel 10.shp'
#definir paths
generalpath = 'C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\RBI'
path_OutputASC_tetis = generalpath + '\\Datos\\Tetis\\Tetis_Outputs\\'
path_out2 = generalpath + '\\csv_intermedio\\' #Aquí se escribirán los csvs intermedios
path_out3 = generalpath + '\\csv_tableau\\' #Aquí se escribirá el csv unificado para tableau

#convertir tetis a csv
list_var = ['FS4','P4','X1','X3','X4','X5','Y1','Y2','Y3','Y4'] #definir variables a imprimir
tetis(shpcuenca,path_OutputASC_tetis,list_var,path_out2)

#compilacion de csv para tableau
csv2tbl(path_out2,'TETIS', path_out3)