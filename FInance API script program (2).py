
# coding: utf-8

# In[1]:


import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import datetime
from lxml import html
import os 
import csv
from random import randint


# On récupère les choix utilisatuer

# In[ ]:


print("\n \t $$$$$$$$$$$$$$\n\n      $$$  FINANCE APP     §§§\n \n \t $$$$$$$$$$$$$$\n \n ")


# In[ ]:


choix = input("\n 1 - SOPRA\n 2 - L'OREAL\n 3 - AIR LIQUIDE\n 4 - BIO-MERIEUX\n 5 - TECHNIP\n 6 - ATOS\n 7 - Quitter\n \n  Choisissez un titre: ")


# On choisi un titre en fonction du choix de l'utilisateur

# In[ ]:


if choix == '1':
    titre = "SOP.PA"
    url = "https://www.boursorama.com/cours/1rPSOP/"
    action = "sopra"
elif choix == '2':
    titre = "OR.PA"
    url = "https://www.boursorama.com/cours/1rPOR/"
    action = "loreal"
elif choix == '3':
    titre = "AI.PA"
    url = "https://www.boursorama.com/cours/1rPAI/"
    action = "airliquide"
elif choix == '4':
    titre = "BIM.PA"
    url = "https://www.boursorama.com/cours/1rPBIM/"
    action = "biomerieux"
elif choix == '5':
    titre = "FTI.PA"
    url = "https://www.boursorama.com/cours/1rPAI/"
    action = "technipfmc"
elif choix == '6':
    titre = "ATO.PA"
    url = "https://www.boursorama.com/cours/1rPATO/"
    action = "atos"
    
elif choix == '7':
    exit()
else:
    print("Le titre choisi n'est pas pris en compte. \n ")
    exit()
    

print(titre)


# Fonction pour changer le format des dates de AAAA-MM-JJ HH:MM:SS -> AAAA-MM-JJ HH:MM

# In[ ]:


def reformat_date(index):
    date = datetime.datetime.strptime(index, '%Y-%m-%d %H:%M:%S')
    date = datetime.datetime.strftime(date, '%Y-%m-%d %H:%M')
    
    return date


# On définit la fonction qui chargera les données pour un indicateur technique

# In[ ]:


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
    


# In[ ]:


titre


# FONTION POUR OBTENIR LES INDICATEURS TECHNIQUES

# In[ ]:


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

# In[ ]:


try:
    df_data = analyse_tech(titre)
except:
    print("\n La connexion semble lente, veuillez vérifier votre connexion internet :) ! \n")
    exit()


# Fontion pour obtenir les indicateurs financiers

# In[ ]:


def analyse_fin(url):
    
    analyse_fin = []
    
    #recupere le PER
    page = requests.get(url)
    tree = html.fromstring(page.content)
    per = tree.xpath('//*[@id="main-content"]/div/section/div[2]/article/div[2]/div[7]/div[2]/div[1]/div/table/tbody/tr[4]/td[2]/text()')
    s= per[0].split('        ')
    b = s[2][0:-1]
    analyse_fin.append(float(b))
    
    #Repcupere le dividende par action
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

# In[ ]:


finance = analyse_fin(url)


# In[ ]:


finance


# On supprime les NA

# In[ ]:


df_data = df_data.dropna()


# In[ ]:


df_data


# CALCUL DE LA NOTE DE L'ANALYSE TECHNIQUE ( sur 10 )

# Fonction pour la note du RSI

# In[ ]:


def calcul_rsi(rsi):
    if( rsi < 30 ):
        note_rsi = 10 
    elif( 30 <= rsi <= 70 ):
        note_rsi = 5
    else:
        note_rsi = 0
        
    return note_rsi


# Fonction pour la note du macd

# In[ ]:


def calcul_macd(macd):
    
    if (macd > 0):
        note_macd = 10
    elif(macd < 0):
        note_macd = 0
    else:
        note_macd = 5
        
    return note_macd


# Fonction pour la note du stockastique

# In[ ]:


def calcul_stoch(stoch):
    if(stoch < 20 ):
        note_st = 10
    elif(20 <= stoch <80 ):
        note_st = 5
    else:
        note_st = 0
        
    return note_st


# Fonction qui calcule la note technique

# In[ ]:


def calcultech(rsi, macd, sto):
    note_tech = 0.35*5 + 0.25*calcul_rsi(float(rsi)) + 0.25*calcul_macd(float(macd)) + 0.15 *calcul_stoch(float(sto))
    
    return note_tech


# On calcule la note technique

# In[ ]:


note_tech = calcultech(df_data['RSI'][-1], df_data['MACD'][-1], df_data['SlowK'][-1])


# In[ ]:


note_tech


# Fonction pour evaluer l'analyse financiere

# In[ ]:


def note_fin(liste):
    if liste[0] <= 10:
        res=0
    elif liste[0] >= 17:
        res=5
    else:
        res=10
    if liste[1] >= 9:
        res+=10
    elif liste[1] >= 7:
        res+=9
    elif liste[1] >= 5:
        res+=8
    elif liste[1] >= 3:
        res+=7
    elif liste[1] >= 2:
        res+=6
    elif liste[1] >= 1:
        res+=5
    else:
        res+=3
    if liste[2] >= 5:
        res+=10
    elif liste[2] >= 3:
        res+=8
    elif liste[2] >= 2:
        res+=7
    elif liste[2] >= 1:
        res+=5
    else:
        res+=3
    if liste[3] >= 4:
        res+=10
    elif liste[3] >= 2:
        res+=5
    else:
        res+=0
    return float(res/4)


# On prends la note financiere

# In[ ]:


note_f = note_fin(finance) 


# In[ ]:


note_f 


# Fonction qui gère l'information en temps réel

# In[ ]:


def getInfo(action):
    cpt=0
    filename=os.environ["PUBLIC"]+'\\'+action+'Info.csv'
    with open(filename, 'r') as textfile:
        for row in reversed(list(csv.DictReader(textfile, fieldnames = ("date", "info", "pertinence", "note"), delimiter = ';'))):
            date = row['date']
            if date == "date":
                break
            info = row['info']
            pertinence = row['pertinence']
            note = row['note']
            datetime.datetime.strptime(row['date'], "%Y-%m-%d %H:%M")
            limit = datetime.datetime.now()
            limit = limit - datetime.timedelta(hours=2)
            if datetime.datetime.strptime(row['date'], "%Y-%m-%d %H:%M") < limit:
                if cpt==0:
                    tab=[date,info,pertinence,note]
                    cpt=1
                else:
                    tab=tab,[date,info,pertinence,note]
    cpt = 0
    res=[]
    res.append(0)
    res.append('')
    for i in tab:
        res[0]+=5 + float(i[3]) * float(i[2])
        res[1]+=i[1]+'\n'
        cpt+=1
    res[0]=res[0]/cpt
    
    return res


# In[ ]:


resultat_info = getInfo(action)


# In[ ]:


note_info = resultat_info[0]
note_info


# On genere le hazard

# In[ ]:


hazard = randint(1,8)
hazard


# on calcule la note finale

# In[ ]:


note_finale = 0.23 * note_f + 0.20 * note_tech + 0.5 * note_info + 0.07 * hazard
note_finale


# On emet une ecommandation en fonction de la note finale

# In[ ]:


if(note_finale < 3.33):
    recom = "VENDEZ !!!!"
elif( 3.33 <= note_finale < 7):
    recom = "NE FAITES RIEN! ATTENDEZ !!!"
else:
    recom = "ACHETEZ !!! "


# On affiche la recommandation à l'utilisateur et la raison

# In[ ]:


print("\n \n")
print("Notre conseil :" + recom)
print("\n \n RAISON: "+ resultat_info[1])

