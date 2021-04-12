#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:50:31 2021

@author: erickrdz
Main para obtener sitios de interes utilizando la función definida como búsqueda
"""
#Programa de Python para obtener lugares 
#de acuerdo a las coordenadas utlizando
#Google Place API

##############################################################################
##  Importar librerias
##############################################################################
import requests, time, os
import numpy as np
import pandas as pd  


##############################################################################
##  Definicion Funcion
##############################################################################
def findPlaces(coor,query,rad):
    api_key = ''
    url= "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    Busqueda=[]
    pagetoken= None
    while True:
        if not pagetoken:
            ur=(url + 'location='+ coor + '&name='+ query
                 + '&radius=' + rad + '&key=' + api_key)
        else:
            ur=(url + 'location='+ coor + '&name='+ query
                 + '&radius=' + rad + '&key=' + api_key + '&pagetoken=' 
                 + pagetoken)
        
        r = requests.get(ur)
        x = r.json()
        y = x['results']
        pagetoken = x.get("next_page_token",None)
        Busqueda=Busqueda+y
        time.sleep(3)
        if not pagetoken:
            break

    return Busqueda

##############################################################################
##  Main
##############################################################################

dataPath = '/Users/erickrdz/Desktop/ProyectoHabi/el-algoritmo-es-correcto/'
trainPath = os.path.join(dataPath,'train_data.csv')
testPath = os.path.join(dataPath,'test_data.csv')
dfTrain = pd.read_csv(trainPath)
dfTest = pd.read_csv(testPath)

##########
##########
##  Borrar elementos de la la base de datos
##########
##########

#Poner los NaN en 0
dfTrainClean = dfTrain.fillna(0)

#Buscar y eliminar elementos donde el area sea menor a  50
x=np.where(dfTrainClean["area"] <= 50)[0]
dfTrainClean=dfTrainClean.drop(dfTrainClean.index[x])

#Buscar y eliminar elementos del sin info de baños 
x=np.where(dfTrainClean["banos"] == 0)[0]
dfTrainClean=dfTrainClean.drop(dfTrainClean.index[x])
##################################################
#NOTA, A LA MIERDA LOS BAÑOS QUE LA INFO ESTA MAL.
##################################################
dfTrainClean=dfTrainClean.drop(['banos'], axis=1)

#Buscar y eliminar elementos sin info de habitaciones
x=np.where(dfTrainClean["habitaciones"] == 0)[0]
dfTrainClean=dfTrainClean.drop(dfTrainClean.index[x])

#Buscar y eliminar elemtnos de estrato
x=np.where(dfTrainClean["estrato"] == 0)[0]
dfTrainClean=dfTrainClean.drop(dfTrainClean.index[x])

#Eliminar todas las columnas que creemos que no sirven para pura mierda
dfTrainClean=dfTrainClean.drop(['banoservicio'], axis=1)
dfTrainClean=dfTrainClean.drop(['conjuntocerrado'], axis=1)
dfTrainClean=dfTrainClean.drop(['deposito'], axis=1)
dfTrainClean=dfTrainClean.drop(['halldealcobas'], axis=1)
dfTrainClean=dfTrainClean.drop(['piso'], axis=1)
dfTrainClean=dfTrainClean.drop(['saloncomunal'], axis=1)
dfTrainClean=dfTrainClean.drop(['valoradministracion'], axis=1)
dfTrainClean=dfTrainClean.drop(['vista'], axis=1)
dfTrainClean=dfTrainClean.drop(['tiponegocio'], axis=1)
dfTrainClean=dfTrainClean.drop(['tiempodeconstruido'], axis=1)
dfTrainClean=dfTrainClean.drop(['porteria'], axis=1)
######################################################
#NOTA, EL TIEMPO DE CONSTRUIDO ES VALIOSO PERO EXISTEN 
#POCAS CASAS CON ESA INFORMACION
######################################################

#Cambiar el tipo de etiqueta por 1 y 2
dfTrainClean.tipoinmueble=dfTrainClean.tipoinmueble.replace("Casa",1)
dfTrainClean.tipoinmueble=dfTrainClean.tipoinmueble.replace("Apartamento",2)

del x
dfTrainClean=dfTrainClean.reset_index(drop=True) #Reset index



##########
##########
##  Obtener informacion de los lugares a 1 km a la redonda
##########
##########
rad='1000' #1km
query = 'Restaurantes', 'Escuelas', 'Hospitales', 'Centros comerciales', 'Parques'
Agregar=[[0 for i in range(1)] for j in range(len(query))]

for k in range(len(dfTrainClean)):
    Busqueda=[]
    index=[]
    lat=dfTrainClean.at[k,'latitud']
    long=dfTrainClean.at[k,'longitud']
    coor=str(lat) + '%2C' + str(long)

    for i in range(len(query)):
        x = findPlaces(coor,query[i],rad)
        index.append(len(x))
        Busqueda.append(x)

    for i in range(len(Busqueda)):
        # print('%%%%%%%%%%%%%%%%%%%%%')
        # print(query[i])
        # print('%%%%%%%%%%%%%%%%%%%%%')
        Agregar[i].append(len(Busqueda[i][:]))
        
#Al final para deshacerme del primer elemento que agregue
for i in range(len(query)):
    Agregar[i].pop(0)
    
    
#########################################################################
#   Esto es nuevo porque se corto y solo se tiene 1004 valores

cutdfTrainClean=dfTrainClean[0:1004]
cutdfTrainClean.loc[:,query[0]] = Agregar[0]
cutdfTrainClean.loc[:,query[1]] = Agregar[1]
cutdfTrainClean.loc[:,query[2]] = Agregar[2]
cutdfTrainClean.loc[:,query[3]] = Agregar[3]
cutdfTrainClean.loc[:,query[4]] = Agregar[4]

cutdfTrainClean.to_csv('BaseDatosTE.csv', index=False)
        
        




