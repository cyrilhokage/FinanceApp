
# coding: utf-8

# In[123]:


import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import datetime
from lxml import html
import os 
import csv


# On récupère les choix utilisatuer

# In[140]:


choix = input("Choisissez un titre:\n 1 - SOPRA\n 2 - L'OREAL\n 3 - AIR LIQUIDE\n 4 - BIO-MERIEUX\n 5 - TECHNIP\n 6 - ATOS\n 7 - Quitter\n ")


# On choisi un titre en fonction du choix de l'utilisateur

# In[141]:


if choix == '1':
    titre = "SOP.PA"
    url = "https://www.boursorama.com/cours/1rPSOP/"
elif choix == '2':
    titre = "OR.PA"
    url = "https://www.boursorama.com/cours/1rPOR/"
elif choix == '3':
    titre = "AI.PA"
    url = "https://www.boursorama.com/cours/1rPAI/"
elif choix == '4':
    titre = "BIM.PA"
    url = "https://www.boursorama.com/cours/1rPBIM/"
elif choix == '5':
    titre = "FTI.PA"
    url = "https://www.boursorama.com/cours/1rPAI/"
elif choix == '6':
    titre = "ATO.PA"
    url = "https://www.boursorama.com/cours/1rPATO/"
elif choix == '7':
    exit()
else:
    print("Le titre choisi n'est pas pris en compte. \n ")
    exit()
    

print(titre)


# Fonction pour changer le format des dates de AAAA-MM-JJ HH:MM:SS -> AAAA-MM-JJ HH:MM

# In[142]:


def reformat_date(index):
    date = datetime.datetime.strptime(index, '%Y-%m-%d %H:%M:%S')
    date = datetime.datetime.strftime(date, '%Y-%m-%d %H:%M')
    
    return date


# On définit la fonction qui chargera les données pour un indicateur technique

# In[143]:


def analyse(titre ,fonction):
    periode = "20"
    
    #Les différentes parties de l'url
    part1_url_analyse = "https://www.alphavantage.co/query?function="
    part2_url_analyse = "&symbol="
    part3_url_analyse = "&interval=1min&time_period="
    part4_url_analyse = "&series_type=close&apikey=2FWTNAS6MFKAV1XH"
    
    #On construit l'url
    url_analyse = part1_url_analyse + fonction + part2_url_analyse + titre + part3_url_analyse + periode + part4_url_analyse
    
    #On exécute la requete
    response_an = requests.get(url_analyse)
    
    #On convertit le résultat de la requete en json puis en dataFrame
    data_an = json.loads(response_an.content)
    analyses = pd.DataFrame.from_dict(data_an["Technical Analysis: "+fonction], orient='index')
    
    return analyses
    


# FONTION POUR OBTENIR LES INDICATEURS TECHNIQUES

# In[156]:


def analyse_tech(titre):
    #On construit l'url de la requete API avec une concaténation de chaines de caractères
    
    #Mais avant on prépare les parties de l'url
    part1_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="
    part2_URL = "&interval=1min&outputsize=full&apikey=2FWTNAS6MFKAV1XH"
    
    #Maintenant on construit l'url pour l'action en bourse 
    url = part1_URL + titre + part2_URL
    
    #On exécute la requête
    response = requests.get(url)
    
    #On convertit la réponse au format json
    data = json.loads(response.content)
    
    #On convertit en dataFrame
    df_data = pd.DataFrame.from_dict(data['Time Series (1min)'], orient='index')
    
    #On change les index des dataframe au format AAAA-MM-JJ HH:MM
    df_data.index = list(map(reformat_date, df_data.index))
    
    #Liste qui va contenir les fonctions à analyser
    fonctions = ['BBANDS', 'RSI', 'MACD', 'STOCH']
    
    #On calcule tous les indicateurs techniques
    for fonction in fonctions:
        analyse_tech = analyse(titre, fonction)
    
        #on joint le resultat au dataframe
        df_data = pd.concat([df_data, analyse_tech], axis=1, join_axes=[analyse_tech.index])
        
    return df_data


# On appelle la fonction pour l'analyse technique

# In[157]:


df_data = analyse_tech(titre)


# Fontion pour obtenir les indicateurs financiers

# In[115]:


def analyse_fin(url):
    
    analyse_fin = []
    
    #recupere le PER
    page = requests.get(url)
    tree = html.fromstring(page.content)
    per = tree.xpath('//*[@id="main-content"]/div/section/div[2]/article/div[2]/div[7]/div[2]/div[1]/div/table/tbody/tr[4]/td[2]/text()')
    s= per[0].split('        ')
    b = s[2][0:-1]
    analyse_fin.append(float(b))
    
    #Repcupere le dividende
    div = tree.xpath('//*[@id="main-content"]/div/section/div[2]/article/div[2]/div[7]/div[2]/div[1]/div/table/tbody/tr[1]/td[4]/text()')
    div = div[0].split('        ')
    div = div[2][0:-1]
    analyse_fin.append(float(div))
    
    #recupere le BNA
    bna = tree.xpath('//*[@id="main-content"]/div/section/div[2]/article/div[2]/div[7]/div[2]/div[1]/div/table/tbody/tr[3]/td[3]/text()')
    bna = bna[0].split('        ')
    bna = bna[2][0:-1]
    analyse_fin.append(float(bna))
    
    #recupere le rendement
    rd = tree.xpath('//*[@id="main-content"]/div/section/div[2]/article/div[2]/div[7]/div[2]/div[1]/div/table/tbody/tr[2]/td[3]/text()')
    rd = rd[0].split('        ')
    rd = rd[2][0:-2]
    analyse_fin.append(float(rd))
    
    return analyse_fin
    
    
    
    
    
    
    


# On charge les indicateurs financiers dans une liste dans cet ordre : -------
#     1- PER , 
#     2- Dividende , 
#     3- BNA , 
#     4- Rendement , 

# In[120]:


liste = analyse_fin(url)

