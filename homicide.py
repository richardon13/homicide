# Histórico de homicidios reales en Estados Unidos

import pandas as pd
import numpy as np
import requests
import kaggle
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi



# La DB pesa mas de 100 Mb, entonces la traigo mediante la api de kaggle
#df = pd.read_csv('./in/database.csv')
#print(df.head())


api = KaggleApi()
api.authenticate()

#api.competition_download_file('homicide-reports', 'database.csv')

api.dataset_download_file('murderaccountability/homicide-reports', file_name= 'database.csv')

with zipfile.ZipFile('database.csv.zip', 'r') as zipref:
    zipref.extractall()

df = pd.read_csv('database.csv')
print(df.head())

# 1) listar las cinco primeras ciudades con el mayor número de agencias

city_may = df.groupby('City')['Agency Name'].nunique().sort_values(ascending = False).head()
cities = []
for city in city_may.index:    
    cities += [city]

print(f'Las 5 ciudades con el mayor numero de agencias son : {cities}')

# 2) Forma 1: de los tipos de agencia, determinar las de tipo Sheriff y mostrar el nombre

sheriff = df[df['Agency Type'] == 'Sheriff']['Agency Name'].unique()
df_sheriff = pd.DataFrame(sheriff, columns= ['Agency Name'])
print(df_sheriff)

# 2) Forma 2: de los tipos de agencia, determinar las de tipo Sheriff y mostrar el nombre

df_sheriff = df[df['Agency Type'].str.contains('Sheriff')][['Agency Type', 'Agency Name']]['Agency Name'].unique()
print(df_sheriff)

# 3) listar los estados más afectados por crímenes perpetrados por mujeres

perp_woman = df[df['Perpetrator Sex'] == 'Female']['State'].value_counts().head()
print(perp_woman)

# 4) listar los estados más afectados por crímenes perpetrados por hombres

perp_male = df[df['Perpetrator Sex'] == 'Male']['State'].value_counts().head()
print(perp_male)

# 5) determinar el número exacto del número de crímenes hechos por mujeres de raza Asian/Pacific Islander. R/= 7127

perp_fem_asia = df[(df['Perpetrator Race'] == 'Asian/Pacific Islander') & (df['Perpetrator Sex'] == 'Female')]
T_perp_fem_asia = perp_fem_asia['Incident'].sum()
print(T_perp_fem_asia)

# 6) determinar la raza más criminal           ********             

gr = df.groupby(['Perpetrator Race'])[['Incident']].count().sort_values('Incident', ascending=False).head(1)
print(gr)  

# 7) determinar el número exacto de hispanos que han asesinado mediante la estrangulación. R/= 5135

num_hisp = df[(df['Victim Ethnicity'] == 'Hispanic') & (df['Weapon'] == 'Strangulation')]['Incident'].sum()
print(num_hisp)

# 8) determinar el tipo de relación más peligrosa, el cual comete más homicidios con armas de tipo Shotgun=escopeta R/= Acquaintance            

rel_pel = df[df['Weapon'] == 'Shotgun']['Relationship'].value_counts().head(1)
print(rel_pel)

# 9) cuál es el sexo que más homicidios ha cometido con Veneno= Poison

sex_ven = df[df['Weapon'] == 'Poison']['Perpetrator Sex'].value_counts().head(1)
print(sex_ven)

# 10) cuántos asesinos de raza negra atrapó el FBI ***************

ase_black = df[df['Perpetrator Race'].str.contains('Black')][['Record Source']].value_counts().head(1)
print(ase_black)

# 11) cuántas víctimas de tipo hispanas han muerto y porque tipo de medio (arma blanca, arma de fuego, etc) R/= 72652

df[df['Victim Ethnicity'] == 'Hispanic']['Weapon'].value_counts().sum() 
hisp = df[df['Victim Ethnicity'] == 'Hispanic']['Weapon'].value_counts()
print(hisp)

# 12) cuál ha sido el asesino más viejo *************

df['Perpetrator Age'] = pd.to_numeric(df['Perpetrator Age'],errors = 'coerce')
old = df[['Record ID','Perpetrator Age']]['Perpetrator Age'].sort_values(ascending = False).head(1)  
print(old)

# 13) cuál ha sido el asesino más joven *******************

young = df.iloc[[df[df["Perpetrator Age"] > 5]["Perpetrator Age"].idxmin()]][['Record ID', 'Perpetrator Age']]
print(young)

# 14) cuál es el total de homicidios desde el año 1995 hasta el año 2000 (ADVERTENCIA – META CONSULTAS DE TIPO KILLER) R/=

ran_hom = df[(df['Year'] >= 1995) & (df['Year'] <= 2000)][['Incident']].sum()
print(ran_hom)

# 15)	#cuál es el total de homicidios desde el año 1995 hasta el año 2000 perpetrado por hombres de raza negra por sofocacion=Suffocation R/= 1082

ran_hom2 = df[(df['Year'] >= 1995) & (df['Year'] <= 2000) & (df['Perpetrator Race'] == 'Black') & (df['Weapon'] == 'Suffocation')][['Incident']].sum()
print(ran_hom2)

# 16) determinar los homicidios anteriores a 1980 perpetrados por hombres del estado de Alaska de raza negra 
#R/= No hay registro de muertes para ANTES de 1980

bef_80 = df[(df['Year'] < 1980) & (df['Perpetrator Race'] == 'Black') & (df['Perpetrator Sex'] == 'Male') & (df['State'] == 'Alaska')][['Record ID', 'Incident']]
print(bef_80)

# 17) determinar los homicidios de la policía municipal de la ciudad de Nueva York del cual hayan sido por relaciones de tipo Ex-Wife, 
# y además que su arma haya sido la estrangulacion=Strangulation. R/= 35

ny = df[(df['City'] == 'New York') & (df['Agency Type'] == 'Municipal Police') & (df['Relationship'] == 'Ex-Wife') & (df['Weapon'] == 'Strangulation')][['Record ID', 'Incident']]
print(ny)

# 18) listar todos los homicidios que hayan ocurrido desde 1980 hasta 1970 en el estado de Illinois del cual el grupo étnico de la víctima 
# no es hispano=Not Hispanic y la relación con el asesino fue de amigos=Friend y el arma utilizada fue una escopeta=Shotgun

range = df[(df['Year'] >= 1970) & (df['Year'] <= 1980) & (df['State'] == 'Illinois') & (df['Victim Ethnicity'] == 'Not Hispanic') & (df['Weapon'] == 'Shotgun') & (df['Relationship'] == 'Friend')][['Record ID', 'Incident']]
print(range)