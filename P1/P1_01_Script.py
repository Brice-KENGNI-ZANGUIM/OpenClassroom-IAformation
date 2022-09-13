# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 22:17:59 2021
@author: kenza
"""
import requests, uuid, json , linecache
import numpy as np
from confidential import subscription_key, endpoint, location

path = '/detect'
constructed_url = endpoint + path
texte_manuel = False
file_languages , file_sentences = "y_test.txt" , "x_test.txt"  # nom des file contenant l'abreviation des langues et les phrases
langues_recherchees = np.array(['fra',"wol", 'eng', "jam", "ita", "ibo", "rus" , "spa", "jpn" ])  # List de langues chercherchées dans le fichier

def extraction ( langues ) :
    """
    La fonction a pour but d'extraire au hasard une liste de phrase dans un fichier à partir d'une liste de 
    langue qui lui est fournie dans la variable 'langue'
    
    Parameters
    ----------
    langues :  
        DESCRIPTION.
            Liste des codes de toutes les langues des phrases à éxtraire de la base de donnée
    Returns
    -------
    type <dict> : 
        DESCRIPTION.
            Le dictionnaire est de la forme { Code de la langue : Phrase choisie au hasard dans cette langue }
    """
    initial_values = '1'
    pick_lines  , n = { k:initial_values for k in langues }  , 0
    b = np.array(list(pick_lines.values()) )
    with open( file_languages , 'r' ) as f : file_lenght = len(f.read().splitlines())  # extractiion de la taille du fichier
    while any( b[b==initial_values] ) :
        n = np.random.randint(1,file_lenght)   # choix au hasard d'une ligne parmi les nombreuses lignes du fichier
        languages_get = linecache.getline(file_languages , n).splitlines()[0]  # extraction de la phrase correspondante dans le file
        if languages_get  in pick_lines.keys()  :
            pick_lines[languages_get ] = linecache.getline( file_sentences , n).splitlines()[0] # update des values du dictionnaire
        b = np.array(list(pick_lines.values()) )  
    return pick_lines  # retourne un dictionnaire avec ( KEYS:VALUES == Langues : contenu des lignes choisies dans le fichier )

def detection( text = "Bonjour" ):
    """
    Détecter ou prédire la langue dans laquelle est écrite la phrase transmise dans la variable 'text'

    Parameters
    ----------
    text : <str>  - default value is "Bonjour"
        DESCRIPTION. La variable "text" contient la phrase qu'on doit envoyer à l'API afin de déterminer la langue dans laquelle elle est écrite 

    Returns
    -------
    <dict>
        DESCRIPTION. La fonction retourne un dictionnaire dont les clés les plus pertinantes pourle projet sont "language" et "score"

    """
    params = {  'api-version': '3.0'  }
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())     }
    body = [ {'text': text} ]    # texte à analyser par l'API
    request = requests.post(constructed_url, params=params, headers=headers, json=body)  
    response = request.json()
    return response[0] #json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))

############---------################---------###############---------###############---------###############---------##############
############   Excécution du programme pour detection de la langue des phrases extraites du fichier "file_sentences"  ##############

if __name__ == "__main__" :
    if texte_manuel :
        langues_recherchee = input("Dans quelle langue écrivez vous ? : ")
        #result_lines = input("Veiller écrire un texte : ")
        result_lines = { langues_recherchee: input("Veiller écrire un texte : ")} 
    else :
        result_lines = extraction( langues_recherchees )
    i = 1
    print("####------####------####------####------####------####------####------####")
    print("####------####     RESULTAT DE LA DETECTION DE LANGUE       ####------####\n")
    for k,v in result_lines.items() :
        response = detection(v)
        language , score = response['language'] , response['score']
        print(f"{i} - TEXTE : {v} \n\t A - Exact Language       : {k.upper()} \n\t"+ \
              f" B - Predicted language   : {language.upper()}\n\t C - Confiance/Precision  : {score*100} % \n")
        i += 1
        