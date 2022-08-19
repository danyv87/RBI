#convertir csv intermedio a csv para tableau

import pandas as pd
import glob

def csv2tbl(csv_folder_input,ID_source, csv_folder_tableauOut):
    list2 = glob.glob(csv_folder_input + '*.csv')
    WS1 = pd.read_csv(list2[0])
    WS1['anho'] = list2[0].split("_")[2][0:4]
    WS1['variable'] = list2[0].split("_")[1]
    for x in range(1, len(list2)):
        if list2[x] == ID_source:
            WS2 = pd.read_csv(list2[x])
            WS1['anho'] = list2[x].split("_")[2]
            WS1['variable'] = list2[x].split("_")[1]
            print(x)
            WS1 = WS1.append(WS2, ignore_index=True)
    WS1.to_csv(csv_folder_tableauOut + ID_source + '.csv')
    print("listo 4/4")