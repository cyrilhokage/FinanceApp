
# coding: utf-8

# In[11]:


import requests
import json


# On récupère les choix utilisatuer

# In[2]:


choix = input("Choisissez un titre:\n 1 - SOPRA\n 2 - L'OREAL\n 3 - AIR LIQUIDE\n 4 - BIO-MERIEUX\n 5 - TECHNIP\n 6 - ATOS\n ")


# On choisi un titre en fonction du choix de l'utilisateur

# In[3]:


if choix == '1':
    titre = "SOP.PA"
elif choix == '2':
    titre = "OR.PA"
elif choix == '3':
    titre = "AI.PA"
elif choix == '4':
    titre = "BIM.PA"
elif choix == '5':
    titre = "FTI.PA"
elif choix == '6':
    titre = "ATO.PA"
else:
    print("Le titre choisi n'est pas pris en compte. ")
    

print(titre)


# On construit l'url de la requete API avec une concaténation de chaines de caractères

# Mais avant on prépare les parties de l'url

# In[5]:


part1_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="
part2_URL = "&interval=1min&outputsize=full&apikey=2FWTNAS6MFKAV1XH&fbclid=IwAR2dsBhcQlzv3D97mT7yFWAEzfP331l_X_umYLPpfUiCkV9QpOpy-uwuVds"


# Maintenant on construit l'url

# In[6]:


url = part1_URL + titre + part2_URL


# In[7]:


url


# PROTOTYPE URL

# url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AL&interval=1min&outputsize=full&apikey=2FWTNAS6MFKAV1XH&fbclid=IwAR2dsBhcQlzv3D97mT7yFWAEzfP331l_X_umYLPpfUiCkV9QpOpy-uwuVds"

# On exécute la requête 

# In[8]:


response = requests.get(url)


# In[14]:


response.content


# In[15]:


data = json.loads(response.content)


# In[16]:


data

