#COMPARADOR V1
#Versión 1 del comparador que permite con un símbolo, precio y hace cuantas horas comprado, chequear las variaciones con 
#respecto a las demás monedas



import config
from binance.client import Client
from binance.enums import *
from pandas.core.frame import DataFrame
import pandas as pd
import time
#import vlc
#import threading
#import math
#import csv
#import itertools
import datetime
from scipy import stats
import numpy as np
from colorama import init
from colorama import Fore, Back, Style


#que funcione con un ingreso de fecha especifica y moneda especifica o precio especifioco y moneda para calcular con respecto a todos de una vez


#-----------------------------------------------------------------------------------------------------------
#CONEXIÓN
#-----------------------------------------------------------------------------------------------------------



client = Client(config.API_KEY, config.API_SECRET, tld='com')




#-----------------------------------------------------------------------------------------------------------
#VARIABLES GLOBALES
#-----------------------------------------------------------------------------------------------------------


#Moneda base que será analizada, comparada y quizá cambiada
#moneda_base = 'ETHUSDT'

#Cantidad de horas atras cuando se compró la moneda base
#cantidad_horas_atras = 14


#precio base con el que se compró la moneda, para que sirva de referencia en la comparativa
precio_base = 2120.99

#Cantidad comprada de moneda base, se utilizará  para hacer la transacción con otra moneda
cantidad_moneda_base = 0.01541


#Lista de monedas a analizar
listacoin = ['BTCUSDT',
'ETHUSDT',
'MATICUSDT',
'ADAUSDT',
'BNBUSDT',
'XRPUSDT',
'DOTUSDT',
'ICPUSDT',
'SOLUSDT',
'SHIBUSDT',
'LINKUSDT',
'LTCUSDT',
'THETAUSDT',
'DOGEUSDT',
'VETUSDT',
'EOSUSDT',
'TRXUSDT',
'BCHUSDT',
'NEOUSDT',
'COMPUSDT',
'UNIUSDT'
]
#listacoin = ['BTCUSDT','ETHUSDT','MATICUSDT']


#-----------------------------------------------------------------------------------------------------------
#FUNCIONES
#-----------------------------------------------------------------------------------------------------------



#Esta función proporciona el precio de mercado actual
def precio_mercado_actual(simbolo):

    try:
        list_of_tickers = client.get_all_tickers()

        for tick_2 in list_of_tickers:
            if tick_2['symbol'] == simbolo:
                symbolPrice = float(tick_2['price'])
                return float(symbolPrice)
    except:
        return 'null'



#-----------------------------------------------------------------------------------------------------------
#MAIN
#-----------------------------------------------------------------------------------------------------------



print('---------------------------------------------')
print('COMPARADOR V1')
print('---------------------------------------------')

r_moneda= input('Por favor ingrese la MONEDA base que compró: ')

r_precio= input('Por favor ingrese el PRECIO con el que compró: ')

r_dias= input('Por favor ingrese HACE CUANTAS HORAS lo ha comprado: ')

print('************************************************')

if (r_moneda=='') and (r_precio==''):

    moneda_base = 'NONE'

else:

    moneda_base = str(r_moneda)
    precio_base = float(r_precio)
    

cantidad_horas_atras = int(r_dias)
#agrupa para convertir en df
agrupador2=[]
fecha_referencia= str(cantidad_horas_atras)+' hour ago UTC'

for coin in listacoin:

    agrupador = []

    #Si moneda es igual a la moneda base, toma el precio base y no lo jala como el resto para la comparativa
    if coin == moneda_base:
        precio_referencia = precio_base
    
    else:
        precio_referencia = float(client.get_historical_klines(coin, Client.KLINE_INTERVAL_1MINUTE, fecha_referencia )[0][2])

    #precio actual de mercado para el coin en curso
    precio_actual = precio_mercado_actual(coin)
    

    print('trabajando: ',coin)
    #print(coin)
    #print(precio_referencia)
    #print(precio_actual)
    porcentaje=round(((precio_actual-precio_referencia)/precio_referencia)*100,2)
    #print(porcentaje,'%')
    #print("-------------")

    agrupador.append(coin)
    agrupador.append(precio_referencia)
    agrupador.append(precio_actual)
    agrupador.append(porcentaje)

    agrupador2.append(agrupador)


dfr = pd.DataFrame(agrupador2, columns = ['Symbol', 'precio_inicial','precio_actual','variacion'])
dfr_sorted = dfr.sort_values(by=['variacion'],ascending=True)
print(dfr_sorted)

#Seleccionando la moneda elegida
moneda_destino = dfr_sorted.iloc[0,0]
#Seleccionando precio de la moneda elegida
precio_ref_moneda_destino = dfr_sorted.iloc[0,1]

#Si la moneda a cambiar es la misma no se realiza ninguna transacción transacciòn
if moneda_destino==moneda_base:
    print('No se realizará la transacciòn, porque se trata de la misma moneda')
    transaccion = 0

else:
    transaccion = 1



#-------------------------------------TRANSACCIÒN-------------------------------------------------------