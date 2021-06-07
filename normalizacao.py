# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 11:07:54 2021

@author: hamil
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv('data.csv', sep=";", quotechar='"', dtype='unicode')
todos_estados = data['UF do Produto'].unique().tolist()
todos_estados.sort()

estados = ['All']
for i in todos_estados:
    estados.append(i)

if estado == 'All':
    data_estado = data.copy()
else:
    data_estado = data[data['UF do Produto'] == estado]
anoValor = data_estado.groupby(['Ano'],as_index=False)['Valor FOB (US$)'].agg('sum')  