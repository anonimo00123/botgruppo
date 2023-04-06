
#? Librerie matematiche 
import math
import random
#? Librerie sconosciute
from sre_constants import GROUPREF_UNI_IGNORE
#? Libreria per gestire i thread del bot
from threading import Thread
#? Libreria per fare richieste Api con il bot 
import requests
#? Libreria che utilizza l'API di Pexels per trovare delle foto
from pexels_api import API
#? Librerie per gestire il bot 
import telebot
from telebot import types
#? Libreria per gestire il DB
from pymongo import MongoClient
#? Librerie per gestire il tempo
import time
from datetime import datetime
#? Import per l'intelligenza artificiale
import openai
import os
#? cerca da Youtube
from youtube_search import YoutubeSearch
#? Scarica da youtube 
import pytube
from pytube import YouTube

from flask import Flask, render_template, app

@app.route('/')
def index():
    return render_template('index,html')


#? Connettiamoci al db 
client = MongoClient("mongodb+srv://jkdjxkkx:steenf385@cluster0.h1fnl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

#? Connettiamoci al bot
Bot = telebot.TeleBot("5414774013:AAFMLODKuQiqg-3K31p8vz93a3C_nD9WX1E")

#? Aggiungi utenti 
def AggiungiUtenti(Id:int ,Nome:str,Cognome:str,Username:str):
    Utenti = client.get_database('RelazioniUtenti').Utenti
    Utenti.insert_one({
        'Id': Id, 
        'Nome': Nome, 
        'Cognome': Cognome, 
        'Username': Username
    })

def GetUtenti(): 
    return client.get_database('RelazioneUtenti').Utenti 

#? Ricerca utenti
def CercaUtente(Id:int): 
    Utenti = GetUtenti()
    return Utenti.find_one({'Id':Id})



#? Gestiamo le possibili eccezioni 
def GestisciEccezione(Eccezione: Exception): 
    return 0 

#? Aggiorniamo utenti 
def AggiornaUtenti(Campo:str, Valore, Id:int): 
    Utenti = GetUtenti()
    Utenti.find_one_and_update({'Id': Id},{"$set": {Campo: Valore}},upsert=True)

#? Creiamo un nuovo utente 
def CreaUtente(Id :int, Nome:str, Cognome:str, Username:str): 
    Utenti = GetUtenti().insert_one({
        'Id': Id, 
        'Nome' : Nome, 
        'Cognome' : Cognome,
        'Username' : Username
    })

#? Controlliamo se nella tabella utenti c'è l'utente scelto 
def ControllaCredenziali(Id:int, Nome:str, Cognome:str, Username:str) : 
    Utente = CercaUtente(Id) 
    if Utente is not None : 
        if Utente['Nome'] != Nome: 
            AggiornaUtenti('Nome', Nome, Id)
        if Utente['Cognome'] != Cognome: 
            AggiornaUtenti('Cognome',Cognome, Id)
        if Utente['Username'] != Username : 
            AggiornaUtenti('Username', Username, Id)
    else : 
        CreaUtente(Id, Nome, Cognome, Username)
        


    


#? Raccoglie un messaggio generico nel gruppo
@Bot.message_handler(content_types=['text'])
def IniziaMessaggioGenerico(message): 
    Thread(target=MessaggioGenerico, args=[message]).start()
def MessaggioGenerico(message): 
    ControllaCredenziali(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
    print(message.text)

    

    

# ! Controlla gli Update del bot
try:
    Bot.infinity_polling()
except Exception as Eccezione:
    GestisciEccezione(Eccezione)
