##Leer datos del CEMIT y extrapolar en cursos hídricos s/ cod Pfastetter

import pandas as pd
import numpy as np
import geopandas as gpd
from osgeo import gdal
from rasterstats import zonal_stats
from affine import Affine
import rasterio, os
from os import listdir


def calagua(shp_path,path_CEMITBD,path_out):
    #importar csv de la base de datos de calidad de agua de la ITAIPU
    df = pd.read_csv(path_CEMITBD,on_bad_lines='skip',sep = ';',decimal=',')

    #convertir fechas en formato datetime y agregar columnas auxiliares de anho y mes
    TimeConverted=pd.to_datetime(df['fecha_muestreo'])
    TimeConverted_anho=list()
    TimeConverted_month=list()
    for time in TimeConverted:
        TimeConverted_anho.append(time.year)
        TimeConverted_month.append(time.month)
    df["Año"]=TimeConverted_anho
    df["Mes"]=TimeConverted_month
    #table = pd.pivot_table(df,values="valor",index=["fecha_muestreo"],aggfunc=np.sum) #pivotear por fecha
    años = ["2015","2016","2017","2018","2021"]

    #Definir los parametros para la generación de shapefiles, estos deben corresponder a BD IB-CEMIT
    Param_ODS632=['DBO-5 (20º C)','Oxígeno Disuelto','Turbidez','Color','pH','Fósforo Total','NTK']
    Param_label_ODS632=['DBO','OxigenoDisuelto','Turbidez','Color','pH','FosforoTotal','NTK']

    #iterar por año y parametro
    for i in range(len(años)):
        for j in range(len(Param_ODS632)):
            #definir grupo de muestreo (Grupo 2, cursos hídricos)
            df2=df.query("Año == "+ años[i] + " and Grupo == 'Grupo 2' and Variable == '" + Param_ODS632[j] +"'") #Filtrar por variable, grupo y año
            if len(df2) != 0:
                #df2.to_csv(path2 + Param_label_ODS632[j]+".csv")
                data_gdf = gpd.GeoDataFrame(df2, geometry = gpd.points_from_xy(df2['lng'], df2['lat']))
                #data_gdf.plot()
                ESRI_WKT = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
                data_gdf.to_file(filename=path_out+años[i]+Param_label_ODS632[j]+'.shp')
                df2=[]
                data_gdf=[]

                ############ GDAL p/ IDW
                ##reproyectar
                data = gpd.read_file(path_out + años[i] + Param_label_ODS632[j] + '.shp')
                data = data.set_crs(epsg=4326)
                data = data.to_crs(epsg=32721)
                data.to_file(filename=path_out + años[i] + Param_label_ODS632[j] + '_UTM.shp')
                data=[]

                ##IDW
                extentRBI = [665948.6204440884757787,7175974.1674450952559710,782246.8822151946369559,7365749.4827523939311504] #Area de influencia margen derecha
                idw= gdal.Grid(path_out + años[i] + Param_label_ODS632[j] + '_UTM.tif',path_out + años[i] + Param_label_ODS632[j] + '_UTM.shp', zfield="valor",algorithm = "invdist:power=3:radius=15000",outputBounds=extentRBI,width = 100, height = 100)
                idw=[]


                #read shapefile
                shp = gpd.read_file(os.path.dirname(shp_path)) #elegir aqui shp curso hídrico según pfastetter o el mismo pero segmentado/intersectado por subcuenca
                #shp = "C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Varios\\Cursos_Otto4ZonalStats2.shp"
                #shp.plot()
                #read raster
                tif = rasterio.open(path_out + años[i] + Param_label_ODS632[j] + '_UTM.tif')
                #tif2 = gdal.Open(path2 + años[i] + Param_label_ODS632[j] + '_UTM.tif')

                #assign raster values to a numpy and array
                tif_array = tif.read(1)
                tif_array_flipped = np.flipud(tif_array)
                #tif_array2 = tif2.ReadAsArray()

                affine=tif.transform
                #affine2=tif2.GetGeoTransform()

                new_affine2 = Affine(affine.a, affine.b, affine.c,affine.d, affine.e*-1, affine.f + (affine.e * (tif.read(1).shape[0]-1))) # leer https://github.com/perrygeo/python-rasterstats/issues/98
                #new_affine3 = Affine(affine2[1], affine2[2], affine2[0], affine2[4], affine2[5]*-1, affine2[3] + (affine2[5] * (tif_array2.shape[0]-1))) #https://github.com/perrygeo/python-rasterstats/issues/98
                #show(tif)
                stats = zonal_stats(shp, tif_array_flipped , affine=new_affine2, stats=["mean"],all_touched=True) #se asignan los valores valorimos en la intersección con el shapefile
                stats = pd.DataFrame(stats)
                shp['valor'] = stats['mean']
                #shp.to_file(filename=path2 + años[i] + Param_label_ODS632[j] + '_zonal.shp')

                #definición de umbrales según resolución 222/02 de la SEAM http://www.mades.gov.py/wp-content/uploads/2019/05/Resolucion_222_02-Padr%C3%B3n-de-calidad-de-las-aguas.pdf
                    # Parametro	        Clase 1	    Clase 2	            Clase 3	            Clase 4	        Unidad
                    # DBO-5 (20º C)     DBO<3	    3<DBO<5	            5<DBO<10	        s/d	            mg/l
                    # Oxígeno Disuelto	OD>6	    6>OD>5	            5>OD>4	            4>OD>2	        mg/l
                    # Turbidez	        <40	        40<Turbidez<100	    40<Turbidez<100	    Turbidez>100	UNT
                    # Color	            <15	        15<Color<75	        15<Color<75		                    mgPt/l
                    # pH	            6<PH<9	    6<PH<9	            6<PH<9	            6<PH<9          PH
                    # Fósforo Total     P<0.025	    0.025<P<0.05	    P>0.05	            s/d	            mg/l
                    # NTK	            Ni<0.3	    0.3<Ni<0.6	        Ni>0.6	            s/d	            mg/l


                data2= {'Parametro':['DBO-5 (20º C)','Oxígeno Disuelto','Turbidez','Color','pH','Fósforo Total','NTK'],'Clase1':['DBO<3','OD>6','Turbidez<40','Color<15','6<PH<9','P<0.025','Ni<0.3'],
                                  'Clase2':['3<DBO<5','6>OD>5','40<Turbidez<100','15<Color<75','6<PH<9','0.025<P<0.05','0.3<Ni<0.6'],'Clase3':['5<DBO<10','5>OD>4','40<Turbidez<100','15<Color<75','6<PH<9','P>0.05','Ni>0.6'],
                                  'Clase4':['s/d','4>OD>2','Turbidez>100','s/d','6<PH<9','s/d','s/d']}

                data3 = {
                    'Parametro':    ['DBO-5 (20º C)',                                 'Oxígeno Disuelto',                           'Turbidez',                                         'Color',                                        'pH',                                       'Fósforo Total',                                        'NTK'],
                    'Clase1':       ['stats["mean"].le(3)',                            'stats["mean"].ge(6)',                         'stats["mean"].le(40)',                              'stats["mean"].le(15)',                          'stats["mean"].ge(6) & stats["mean"].le(9)',  'stats["mean"].le(0.025)',                               'stats["mean"].le(0.3)'],
                    'Clase2':       ['stats["mean"].ge(3) & stats["mean"].le(5)',       'stats["mean"].ge(5) & stats["mean"].le(6)',    'stats["mean"].ge(40) & stats["mean"].le(100)',       'stats["mean"].ge(15) & stats["mean"].le(75)',    's/d',                                      'stats["mean"].ge(0.025) & stats["mean"].le(0.05)',       'stats["mean"].ge(0.3) & stats["mean"].le(0.6)'],
                    'Clase3':       ['stats["mean"].ge(5) & stats["mean"].le(10)',      'stats["mean"].ge(4) & stats["mean"].le(5)',    'stats["mean"].ge(40) & stats["mean"].le(100)',       's/d',                                          's/d',                                      'stats["mean"].ge(0.05)',                                'stats["mean"].ge(0.6)'],
                    'Clase4':       ['s/d',                                           'stats["mean"].ge(2) & stats["mean"].le(4)',    'stats["mean"].ge(100)',                             's/d',                                          's/d',                                      's/d',                                                  's/d']}

                umbrales_res222 = pd.DataFrame(data2)

                ## Cálculo de indicadores segun resolucion 222/02 de la SEAM


                df3 = pd.DataFrame()
                if data3['Clase1'][j] != 's/d':
                    exec('stats.loc[' + data3['Clase1'][j] + ', "Clase s/ res 222/02"] = "Clase1"')
                if data3['Clase2'][j] != 's/d':
                    exec('stats.loc[' + data3['Clase2'][j] + ', "Clase s/ res 222/02"] = "Clase2"')
                if data3['Clase3'][j] != 's/d':
                    exec('stats.loc[' + data3['Clase3'][j] + ', "Clase s/ res 222/02"] = "Clase3"')
                if data3['Clase4'][j] != 's/d':
                    exec('stats.loc[' + data3['Clase4'][j] + ', "Clase s/ res 222/02"] = "Clase4"')
                    #shp['valor'] = stats['valor']
                shp['Clase s/ res 222/02'] = stats['Clase s/ res 222/02']
                #shp.to_file(filename=path2 + años[i] + Param_label_ODS632[j] + '_Res222.shp')
                shp2 = shp[["cocursodag", "valor","Clase s/ res 222/02"]]
                shp2.to_csv(path_out + 'CEMIT_' + Param_label_ODS632[j] + '_' + años[i] + '.csv')

                ##  a puntaje
                stats.loc[stats["Clase s/ res 222/02"] == "Clase1", 'valor'] = 10
                stats.loc[stats["Clase s/ res 222/02"] == "Clase2", 'valor'] = 6.66
                stats.loc[stats["Clase s/ res 222/02"] == "Clase3", 'valor'] = 3.33
                stats.loc[stats["Clase s/ res 222/02"] == "Clase4", 'valor'] = 0

                shp['valor'] = stats['valor']
                shp2 = shp[["cocursodag", "valor"]]
                shp2.to_csv(path_out + 'CEMIT_ClasePuntaje_' + años[i] + '.csv')

    test = os.listdir(path_out)

    for item in test:
        if not item.endswith(".csv"):
            os.remove(path_out + item)