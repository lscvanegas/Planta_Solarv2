#import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbn
import numpy as np
#from sklearn.preprocessing import MinMaxScaler
#from sklearn.preprocessing import LabelEncoder
#from sklearn.neural_network import MLPRegressor

#from keras.models import Sequential
#from keras.layers import Dense
#from keras.layers import Softmax
#from keras.layers import LSTM

#from sklearn import metrics
#import math
#import keras

import settings
import tools
#import ml_tools


def data_prep():	
    files_name = tools.ls2(settings.path)
    full_data= pd.DataFrame()
    for i in files_name:
        full_data =tools.add_data_month(full_data, settings.path +'/' + i)
    full_data = full_data.sort_index(axis=0)
    full_data = tools.neg_irrad_2_zero(full_data)
    full_data = tools.negative_to_positive(full_data, 'ENERGY')
    full_data = tools.change_outliers_values(full_data, 'ENERGY')
    #full_data = tools.full_data_sun_hours(full_data, 'ENERGY')
    full_data = tools.delete_cols(full_data, settings.cols2delete)
    full_data = full_data.astype(float)
    return full_data

full_data = data_prep()
full_data.to_excel('full_data.xlsx', sheet_name='data')
#
#full_data contiene los datos con frecuencia de una hora.
#full_data en distintas frecuencias
daily = full_data.resample('D').mean()
weekly = full_data.resample('W').mean()
monthly = full_data.resample('M').mean()



#dataset con el que se va a trabaja
dataset = full_data
#dataset = dataset.loc['12-1-2019':'12-31-2019']

##------------------------------------------------
##Gráficos
##------------------------------------------------
#
#
#grafico para series temporales
sbn.set(rc={'figure.figsize':(15, 5)})
dataset['ENERGY'].plot(linewidth=1)
#
##Graficarlas todas en el mismo graph no buena
##fig,eje= plt.subplots()
##for i in ['WS1','IRRAD1','TEMP1','WANG', 'ENERGY']:
##    eje.plot(dataset[i],label=i)
##    eje.set_ylim(0,7000)
##    eje.legend()
##    eje.set_ylabel('Producción (GWh)')
##    eje.set_title('Tendencias en la Producción de electricidad')
#
##grafica varias juntas con el modo de una de area.
##fig,eje = plt.subplots()
##eje.plot(dataset['ENERGY'],color='black',label='Consumo')
##dataset[['IRRAD1','WS1']].plot.area(ax=eje,linewidth=0)
##eje.legend()
##eje.set_ylabel('Total Mensual (GWh)')
#


##graficar todas por separado
#
values = dataset.values
# specify columns to plot
groups = [0, 1, 2, 3, 4]
i = 1
# plot each column
plt.figure()
for group in groups:
	plt.subplot(len(groups), 1, i)
	plt.plot(values[:, group])
	plt.title(dataset.columns[group], y=0.5, loc='right')
	i += 1
plt.show()


#
#
# fig,eje = plt.subplots()
# eje.plot(dataset['ENERGY'],color='black',label='Energy')
# eje2 = eje.twinx()
# eje2.plot(dataset['IRRAD1'],color='red',label='Solar Rad')
# eje.legend()
# eje.set_ylabel('Relacion Radiacion- Energía')

#Análisis de Correlación
f, ax = plt.subplots(figsize=(10, 8))
cor = dataset.astype(float).corr(method = 'pearson')
print(cor)
#sbn.heatmap(cor, cmap='coolwarm',
#               square=True, ax=ax)
sbn.heatmap(cor, mask=np.zeros_like(cor, dtype=np.bool), cmap=sbn.diverging_palette(200, 20, as_cmap=True),
               square=True, ax=ax)
#sbn.heatmap(cor, mask=np.zeros_like(cor, dtype=np.bool), cmap=sbn.light_palette((100, 90, 60), input="husl"),
#               square=True, ax=ax)

