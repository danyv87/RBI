#convertir csv intermedio a csv para tableau

import pandas as pd
from collections import defaultdict
import os

def csv2tbl(csv_folder_input,ID_source, csv_folder_tableauOut):
    #agrupacion de archivos por Fuente de datos
    groups = defaultdict(list)

    for filename in os.listdir(csv_folder_input):
        basename, extension = os.path.splitext(filename)
        BDfuente, variable, anho = basename.split('_')
        groups[BDfuente].append(filename)

    list2 = groups[ID_source]
    WS1 = pd.read_csv(csv_folder_input + list2[0])
    WS1['anho'] = list2[0].split('.')[0].split('_')[2]
    WS1['variable'] = list2[0].split('.')[0].split('_')[1]

    for x in range(1, len(list2)):
        if list2[x].split("\\")[-1].split('_')[0] == ID_source:
            WS2 = pd.read_csv(csv_folder_input + list2[x])
            WS2['anho'] = list2[x].split('.')[0].split('_')[2]
            WS2['variable'] = list2[x].split('.')[0].split('_')[1]
            print(x)
            WS1 = WS1.append(WS2, ignore_index=True)

    WS1.to_csv(csv_folder_tableauOut + ID_source + '.csv')
    print("listo 4/4")