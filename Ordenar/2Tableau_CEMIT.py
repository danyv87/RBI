import os, re
import pandas as pd
import glob

# set paths
output_path = "C:\\Users\\danielal\\PycharmProjects\\RBI\\Outputs\\"
path_tableau_output = "C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Tableau\\"

#buscar csv generados para compilarlos en uno solo que se importará en tableau
list2=glob.glob(output_path + '*.csv')
WS1 = pd.read_csv(list2[0])
WS1['anho']=re.search(r'(?<=\\Outputs\\)\w+', list2[0])[0].rsplit("_",2)[0].split(".")[0]
WS1['variable']=re.search(r'(?<=\\Outputs\\)\w+', list2[0])[0].rsplit("_",2)[-2].split(".")[0]
for x in range(1,len(list2)):
    WS2 = pd.read_csv(list2[x])
    WS2['anho'] = re.search(r'(?<=\\Outputs\\)\w+', list2[x])[0].rsplit("_",2)[0].split(".")[0]
    WS2['variable'] = re.search(r'(?<=\\Outputs\\)\w+', list2[x])[0].rsplit("_",2)[-2].split(".")[0]
    print(x)
    WS1 = WS1.append(WS2,ignore_index=True)
    #WS1 = WS1.append(WS2, ignore_index=True)

WS1.to_csv(path_tableau_output+'CEMIT_tableau2.csv')