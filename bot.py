# ! Import
import math
import random
from sre_constants import GROUPREF_UNI_IGNORE
from threading import Thread
import requests
from pexels_api import API
from telebot import types
import telebot
from pymongo import MongoClient
from telethon import functions
from telethon.sync import TelegramClient
import time
from datetime import datetime

print('AVVIATO!')

api_id = 11029867
api_hash = '6662f2f9d722cd6ab5263dfa1d53cb0b'

# ! Client Mongodb
client = MongoClient(
    "mongodb+srv://jkdjxkkx:steenf385@cluster0.h1fnl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# ! Bot token
bot = telebot.TeleBot("5414774013:AAGrm2RFGc1KijttY35ON3WattdBM7RRc7Y")

# ! Variabili globali per la connessione al database
dbstato = client.get_database("status").stato
dbinfo = client.get_database("status").info
dbruoli = client.get_database("ruoli").ruoliagg
dbquiz = client.get_database("status").quiz
db_baby_name = client.get_database("status").babyname
db_baby_surname = client.get_database("status").babysurname
dboroscopo = client.get_database("oroscopo").inforoscopo
dbhaimai = client.get_database('newhaimai').newhaimaicoll
dbask = client.get_database('newask').newaskcoll
dbaskhot = client.get_database('newaskhot').askhotcoll
dbspoiler = client.get_database('spoiler').spoilers


def ottieniutente(utente: str):
    with TelegramClient('session_name', api_id, api_hash) as client:
        result = client(functions.users.GetFullUserRequest(
            id=utente
        ))
        print(result.stringify())


# ! FONT
def getfont(text: str):
    text.replace('Q', '𝐐').replace('W', '𝐖').replace('E', '𝐄').replace('R', '𝐑').replace('T',

                                                                                         '𝐓').replace(
        'Y', '𝐘').replace('U', '𝐔').replace('I', '𝐈').replace('O', '𝐎').replace('P', '𝐏').replace('A',
                                                                                                  '𝐀').replace(
        'S', '𝐒').replace('D', '𝐃').replace('F', '𝐅').replace('G', '𝐆').replace('H', '𝐇').replace('J',
                                                                                                  '𝐉').replace(
        'K', '𝐊').replace('L', '𝐋').replace('Z', '𝐙').replace('X', '𝐗').replace('C', '𝐂').replace('V',
                                                                                                  '𝐕').replace(
        'B', '𝐁').replace('N', '𝐍').replace('M', '𝐌').replace('q', '𝐪').replace('w', '𝐰').replace('e',
                                                                                                  '𝐞').replace(
        'r', '𝐫').replace('t', '𝐭').replace('y', '𝐲').replace('u', '𝐮').replace('i', '𝐢').replace('o',
                                                                                                  '𝐨').replace(
        'p', '𝐩').replace('a', '𝐚').replace('s', '𝐬').replace('d', '𝐝').replace('f', '𝐟').replace('g',
                                                                                                  '𝐠').replace(
        'h', '𝐡').replace('j', '𝐣').replace('k', '𝐤').replace('l', '𝐥').replace('z', '𝐳').replace('x',
                                                                                                  '𝐱').replace(
        'c', '𝐜').replace('v', '𝐯').replace('b', '𝐛').replace('n', '𝐧').replace('m', '𝐦').replace('1',
                                                                                                  '𝟏').replace(
        '2', '𝟐').replace('3', '𝟑').replace('4', '𝟒').replace('5', '𝟓').replace('6', '𝟔').replace('7',
                                                                                                  '𝟕').replace(
        '8', '𝟖').replace('9', '𝟗').replace('0', '𝟎').replace('!', '!').replace('$', '$').replace('%',
                                                                                                  '%').replace(
        '&', '&').replace('/', '/').replace('(', '(').replace(')', ')').replace('=', '=').replace('?',
                                                                                                  '?').replace(
        '_', '_').replace('-', '-').replace('.', '.').replace(',', ',').replace('[', '[').replace(']',
                                                                                                  ']').replace(
        '<', '<').replace('>', '>')
    return str(text)

    # ! Cerca ruolo


def cercaoperatore(message):
    trova = dbruoli.find_one({'id': message.reply_to_message.from_user.id, "ruolo": "operatore"})
    if trova is None:
        return None
    else:
        return trova


def cercaoperatoredaid(message):
    trova = dbruoli.find_one({'id': message.from_user.id, "ruolo": "operatore"})
    if trova is None:
        return None
    else:
        return trova


def cercaoperatoredaidcall(iddi):
    trova = dbruoli.find_one({'id': iddi, "ruolo": "operatore"})
    if trova is None:
        return None
    else:
        return trova


# ! Gestione errori

def salvaerrore(ex):
    try:
        if " A request to the Telegram API was unsuccessful. Error code: 429" in str(ex):
            bot.send_message(gruppo, "<i>⚡️» Troppe richieste, mandate i comandi più lentamente</i>", parse_mode="html")
        else:
            bot.send_message(1914266767, "Gestisci l'errore " + str(ex))
    except Exception as ex:
        print(ex)


# ! Variabili globali genearli
succhini_iniziali = float(100000)
punti_rispetto_iniziali = 0
likes_iniziali = 0
dislikes_iniziali = 0
diamanti = 10.0
soldi = 10.0
bestemmie_iniziali = 0
xp_iniziali = 0.0
entrate = 1
proprietario = 1914266767
gruppo = -1001434687578
canale_gruppo = -1001579720607
canale_artehub = -1001568212776
canale_log = -1001609514626
memory = -1001539169495
quizzes = []


# ! Nuovo uente nello status
def nuovo_utente_stato(nome, id):
    try:
        dbstato.insert_one({"id": id, "name": nome, "diamanti": diamanti, "soldi": soldi, "succhini": succhini_iniziali,
                            "bestemmie": bestemmie_iniziali,
                            "rispetto": punti_rispetto_iniziali,
                            "like": likes_iniziali,
                            "dislike": dislikes_iniziali,
                            "esperienza": xp_iniziali,
                            "seno": random.randint(0, 20), "cazzo": random.randint(0, 20), "entrate": entrate})
    except Exception as ex:
        salvaerrore(ex)


# ! Check se esiste
def controlla_e_crea(nome, id):
    try:
        trova = dbstato.find_one({"id": id})
        if trova is not None:
            return trova
        elif trova is None:
            nuovo_utente_stato(nome, id)
            trova = dbstato.find_one({"id": id})
            return trova
        else:
            print("errore")
    except Exception as ex:
        salvaerrore(ex)


# ! Incrementa e decrementa oggetti
def incrementa_decrementa_stato(nome, id, oggetto, segno):
    try:
        data = controlla_e_crea(nome, id)
        value = data[oggetto]
        if segno == "-":
            dbstato.find_one_and_update({'id': id}, {"$set": {oggetto: value - 1, "name": nome}}, upsert=True)
        elif segno == "togli":
            dbstato.find_one_and_update({'id': id}, {"$set": {oggetto: 0, "name": nome}}, upsert=True)
        else:
            dbstato.find_one_and_update({'id': id}, {"$set": {oggetto: value + 1, "name": nome}}, upsert=True)
        if oggetto == "bestemmie" and id == 1:
            return data['bestemmie']
        elif oggetto == 'entrate':
            return data['entrate'] + 1
        elif oggetto == 'esperienza':
            dbstato.find_one_and_update({'id': id}, {"$set": {oggetto: value + 10, "name": nome}}, upsert=True)
    except Exception as ex:
        salvaerrore(ex)


# ! Save info stato
def save_info_stato(nome, argomento, da, a, daname, segno):
    try:
        dbinfo.insert_one({'argomento': argomento, "da": da, "a": a, "aname": nome, "daname": daname})
        if argomento == "dislike" and dbinfo.find_one({"argomento": "like", "da": da, "a": a}) != None:
            dbinfo.delete_one({"argomento": "like", "da": da, "a": a})
            incrementa_decrementa_stato(nome, a, "like",
                                        "-")
            incrementa_decrementa_stato(
                nome, a, "dislike", "+")
        elif argomento == "like" and dbinfo.find_one({"argomento": "dislike", "da": da, "a": a}) != None:
            dbinfo.delete_one({"argomento": "dislike", "da": da, "a": a})
            incrementa_decrementa_stato(nome, a,
                                        "dislike",
                                        "-")
            incrementa_decrementa_stato(
                nome, a, " like", "+")
        else:
            incrementa_decrementa_stato(nome, a, argomento, segno)
    except Exception as ex:
        salvaerrore(ex)


# ! try to answer

def try_to(message, text):
    try:
        bot.reply_to(message, text, parse_mode="html")
    except Exception as ex:
        try:
            bot.send_message(message.chat.id, text, parse_mode="html")
        except Exception as ex:
            salvaerrore(ex)


def chatblacklist(chat: str):
    verifica = str(chat)
    if verifica[
        0] == '-' and chat != gruppo and chat != canale_artehub and chat != canale_gruppo and chat != canale_log and chat != -691548571 and chat != -1001599554760:
        bot.send_photo(chat, photo='https://telegra.ph/file/b6b04fe523e57d367326e.jpg',
                       caption='𝐂𝐡𝐚𝐭 𝐧𝐨𝐧 𝐚𝐮𝐭𝐨𝐫𝐢𝐳𝐳𝐚𝐭𝐚 ❌')
        bot.leave_chat(chat)
        return False
    else:
        return True


# ! try to answer

def try_to_two(message, text):
    try:
        bot.reply_to(message, text)
    except Exception as ex:
        try:
            bot.send_message(message.chat.id, text)
        except Exception as ex:
            salvaerrore(ex)


# ! Message id inesistente

def verifica_esistenza(message):
    try:
        return message.reply_to_message.from_user.id
    except:
        return False

    # ! Adatta i nomi al linguaggio html


def namechanger(name, id):
    return "<a href='tg://user?id=" + str(id) + "'>" + str(
        name.replace('<', "").replace(">", "").replace("$", "")) + "</a>"


# ! Comandi /cmd
# stato
# * Comando unrispetto /unrispetto al messaggio di un utente


@bot.edited_message_handler(commands=['unrispetto', 'UNRISPETTO'], chat_types='supergroup')
@bot.message_handler(commands=['unrispetto', 'UNRISPETTO'], chat_types='supergroup')
def startunrispett(message): Thread(target=unrispetto, args=[message]).start()


def unrispetto(message):
    try:
        if chatblacklist(message.chat.id) is True:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) == "administrator":
                if verifica_esistenza(message) == False:
                    bot.send_message(message.chat.id,
                                     "𝗥𝗶𝘀𝗽𝗼𝗻𝗱𝗶 𝗮𝗱 𝘂𝗻 𝘂𝘁𝗲𝗻𝘁𝗲 ✍️ \n 💬 »  <i>Ricordati di rispondere all'utente a cui vuoi togliere il punto rispetto</i>",
                                     parse_mode="html")

                elif message.from_user.id == message.reply_to_message.from_user.id:
                    try_to(message, "<i>🛠» Non puoi unrispettare te stesso </i>")
                else:
                    save_info_stato(message.reply_to_message.from_user.first_name, "rispetto", message.from_user.id,
                                    message.reply_to_message.from_user.id, message.from_user.first_name, "-")
                    bot.send_message(message.chat.id, "😡 𝗠𝗮𝗻𝗻𝗮𝗴𝗴𝗶𝗮 » <i> " + namechanger(
                        message.reply_to_message.from_user.first_name,
                        message.reply_to_message.from_user.id) + " Ti hanno tolto un punto di rispetto</i>",
                                     parse_mode="html")
    except Exception as ex:
        salvaerrore(ex)


# ^ get user

# * Comando di rispetto /rispetto al messaggio di un utente

@bot.edited_message_handler(commands=['rispetto', 'RISPETTO'], chat_types='supergroup')
@bot.message_handler(commands=['rispetto', 'RISPETTO'], chat_types='supergroup')
def startrispetto(message): Thread(target=rispetto, args=[message]).start()


def rispetto(message):
    try:
        if chatblacklist(message.chat.id) is True:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) == "administrator":
                if verifica_esistenza(message) == False:
                    bot.send_message(message.chat.id,
                                     "𝗥𝗶𝘀𝗽𝗼𝗻𝗱𝗶 𝗮𝗱 𝘂𝗻 𝘂𝘁𝗲𝗻𝘁𝗲 ✍️ \n 💬 » <i>Ricordati di rispondere all'utente a cui vuoi aggiungere il punto rispetto</i>",
                                     parse_mode="html")

                elif message.from_user.id == message.reply_to_message.from_user.id:
                    try_to(message, "<i>🛠» Non puoi rispettare te stesso </i>")
                else:
                    save_info_stato(message.reply_to_message.from_user.first_name, "rispetto", message.from_user.id,
                                    message.reply_to_message.from_user.id, message.from_user.first_name, "+")
                    bot.send_message(message.chat.id, "🎉 𝗖𝗼𝗺𝗽𝗹𝗶𝗺𝗲𝗻𝘁𝗶 »<i>" + namechanger(
                        message.reply_to_message.from_user.first_name,
                        message.reply_to_message.from_user.id) + " Hai ottenuto un punto di rispetto</i>",
                                     parse_mode="html")
            print(bot.get_chat_member(message.chat.id, message.from_user.id))
    except Exception as ex:
        salvaerrore(ex)


# * Comando di dislike /dislike al messaggio di un utente
@bot.edited_message_handler(commands=['dislike', 'DISLIKE'], chat_types='supergroup')
@bot.message_handler(commands=['dislike', 'DISLIKE'], chat_types='supergroup')
def startdislike(message): Thread(target=dislike, args=[message]).start()


def dislike(message):
    try:
        if chatblacklist(message.chat.id) is True:
            id = verifica_esistenza(message)
            if id == False:
                bot.send_message(message.chat.id,
                                 "𝗥𝗶𝘀𝗽𝗼𝗻𝗱𝗶 𝗮𝗱 𝘂𝗻 𝘂𝘁𝗲𝗻𝘁𝗲 ✍️ \n 💬 » <i>Ricordati di rispondere all'utente a cui vuoi mettere dislike</i>",
                                 parse_mode="html")

            elif message.from_user.id == message.reply_to_message.from_user.id:
                try_to(message, "<i>🛠» Non puo mettere dislike a te stesso </i>")
            else:
                find = dbinfo.find_one(
                    {"argomento": "dislike", "da": message.from_user.id, "a": message.reply_to_message.from_user.id})
                if find is None:
                    save_info_stato(message.reply_to_message.from_user.first_name, "dislike", message.from_user.id,
                                    message.reply_to_message.from_user.id, message.from_user.first_name, "+")
                    bot.send_message(message.chat.id, "👎 » <i>" + namechanger(message.from_user.first_name,
                                                                              message.from_user.id) + " ha messo dislike a " + namechanger(
                        message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.id) + "</i> ",
                                     parse_mode="html")
                else:
                    bot.send_message(message.chat.id, "🚫 » <i>" + namechanger(message.from_user.first_name,
                                                                              message.from_user.id) + " puoi mettere massimo un dislike alla stessa persona</i>",
                                     parse_mode="html")
    except Exception as ex:
        salvaerrore(ex)


# * Comando like
@bot.edited_message_handler(commands=['like', 'LIKE'], chat_types='supergroup')
@bot.message_handler(commands=['like', 'LIKE'], chat_types='supergroup')
def startlike(message): Thread(target=like, args=[message]).start()


def like(message):
    try:
        if chatblacklist(message.chat.id) is True:
            id = verifica_esistenza(message)
            if id == False:
                bot.send_message(message.chat.id,
                                 "𝗥𝗶𝘀𝗽𝗼𝗻𝗱𝗶 𝗮𝗱 𝘂𝗻 𝘂𝘁𝗲𝗻𝘁𝗲 ✍️ \n 💬 » <i>Ricordati di rispondere all'utente a cui vuoi mettere like</i>",
                                 parse_mode="html")
            elif message.from_user.id == message.reply_to_message.from_user.id:
                try_to(message, "<i>🛠» Non puoi mettere like a te stesso </i>")
            else:
                find = dbinfo.find_one(
                    {"argomento": "like", "da": message.from_user.id, "a": message.reply_to_message.from_user.id})
                if find is None:
                    save_info_stato(message.reply_to_message.from_user.first_name, "like", message.from_user.id,
                                    message.reply_to_message.from_user.id, message.from_user.first_name, "+")
                    bot.send_message(message.chat.id, "👍 » <i>" + namechanger(message.from_user.first_name,
                                                                              message.from_user.id) + " ha messo like a " + namechanger(
                        message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.id) + "</i> ",
                                     parse_mode="html")
                else:
                    bot.send_message(message.chat.id, "🚫 » <i>" + namechanger(message.from_user.first_name,
                                                                              message.from_user.id) + "puoi mettere "
                                                                                                      "massimo un like "
                                                                                                      "alla stessa "
                                                                                                      "persona </i>",
                                     parse_mode="html")
    except Exception as ex:
        salvaerrore(ex)


@bot.message_handler(commands=['ask', 'ASK'], chat_types='supergroup')
def startask(message): Thread(target=ask, args=[message]).start()


def ask(message):
    if chatblacklist(message.chat.id) is True:
        try:
            bot.send_message(message.chat.id,
                             dbask.find({}).limit(-1).skip(random.randint(1, dbask.count_documents({}))).next()['ask'],
                             reply_to_message_id=message.message_id)
        except Exception as ex:
            try:
                bot.send_message(message.chat.id,
                                 dbask.find({}).limit(-1).skip(random.randint(1, dbask.count_documents({}))).next()[
                                     'ask'])
            except Exception as ex:
                salvaerrore(ex)


@bot.message_handler(commands=['haimai', 'HAIMAI'], chat_types='supergroup')
def starthaimai(message): Thread(target=haimai, args=[message]).start()


def haimai(message):
    if chatblacklist(message.chat.id) is True:
        try:
            bot.send_message(message.chat.id,
                             dbhaimai.find({}).limit(-1).skip(random.randint(1, dbhaimai.count_documents({}))).next()[
                                 'haimai'], reply_to_message_id=message.message_id)
        except Exception as ex:
            try:
                bot.send_message(message.chat.id, dbhaimai.find({}).limit(-1).skip(
                    random.randint(1, dbhaimai.count_documents({}))).next()['haimai'])
            except Exception as ex:
                salvaerrore(ex)


@bot.message_handler(commands=['askhot', 'ASKHOT'], chat_types='supergroup')
def startaskhot(message): Thread(target=askhot, args=[message]).start()


def askhot(message):
    if chatblacklist(message.chat.id) is True:
        try:
            bot.send_message(message.chat.id,
                             dbaskhot.find({}).limit(-1).skip(random.randint(1, dbaskhot.count_documents({}))).next()[
                                 'askhot'], reply_to_message_id=message.message_id)
        except Exception as ex:
            try:
                bot.send_message(message.chat.id, dbaskhot.find({}).limit(-1).skip(
                    random.randint(1, dbaskhot.count_documents({}))).next()['askhot'])
            except Exception as ex:
                salvaerrore(ex)


# * addask
@bot.edited_message_handler(regexp='/addask', chat_types='supergroup')
@bot.edited_message_handler(regexp='/ADDASK', chat_types='supergroup')
@bot.message_handler(regexp='/addask', chat_types='supergroup')
@bot.message_handler(regexp='/ADDASK', chat_types='supergroup')
def startaddask(message): Thread(target=addask, args=[message]).start()


def addask(message):
    if chatblacklist(message.chat.id) is True:
        contenuto = verifysecond(message, 'addask')
        if contenuto == 'false':
            nontrovato(message, '/addask [domanda]')
        elif cercaoperatoredaid(message) is None:
            try_to(message, 'Devi essere operatore per svolgere questa operazione ❌')
        elif '?' not in contenuto:
            try_to(message, 'Nella domanda ci deve essere almeno un punto interrogativo ❌')
        else:
            dbask.insert_one({'ask': contenuto, 'autore': message.from_user.id})
            try_to(message, "✅ » <i>Ask aggiunta correttamente</i>")
            removeask = types.InlineKeyboardMarkup()
            btnElimina = types.InlineKeyboardButton(text='Cancella ❌', callback_data='delask')
            removeask.add(btnElimina)
            bot.send_message(canale_log, '#Addask\n• Ask: ' + str(contenuto), reply_markup=removeask)


def verificahaimai(domanda: str):
    if domanda[len(domanda)] != '?': return True


def secondaverifica(domanda: str):
    if 'hai mai' in domanda.lower():
        return False
    else:
        return True


# * addhaimai
@bot.edited_message_handler(regexp='/addhot', chat_types='supergroup')
@bot.edited_message_handler(regexp='/ADDHOT', chat_types='supergroup')
@bot.message_handler(regexp='/addhot', chat_types='supergroup')
@bot.message_handler(regexp='/ADDHOT', chat_types='supergroup')
def startaddaskhot(message): Thread(target=addaskhot, args=[message]).start()


def addaskhot(message):
    if chatblacklist(message.chat.id) is True:
        contenuto = verifysecond(message, 'addhot')
        if contenuto == 'false':
            nontrovato(message, '/addhot [ask hot]')
        elif cercaoperatoredaid(message) is None:
            try_to(message, 'Devi essere operatore per svolgere questa operazione ❌')
        elif '?' not in contenuto:
            try_to(message, "Nell'ask hot ci deve essere un punto di domanda ❌")
        else:
            dbaskhot.insert_one({'askhot': contenuto, 'autore': message.from_user.id})
            try_to(message, "✅ » <i>Ask hot aggiunta correttamente</i>")
            removehaimai = types.InlineKeyboardMarkup()
            btnElimina = types.InlineKeyboardButton(text='Cancella ❌', callback_data='delaskhot')
            removehaimai.add(btnElimina)
            bot.send_message(canale_log, '#Addaskhot\n• ask hot: ' + str(contenuto), reply_markup=removehaimai)
        # * addhaimai


@bot.edited_message_handler(regexp='/addhaimai', chat_types='supergroup')
@bot.edited_message_handler(regexp='/ADDHAIMAI', chat_types='supergroup')
@bot.message_handler(regexp='/addhaimai', chat_types='supergroup')
@bot.message_handler(regexp='/ADDHAIMAI', chat_types='supergroup')
def startaddask(message): Thread(target=addhaimai, args=[message]).start()


def addhaimai(message):
    if chatblacklist(message.chat.id) is True:
        contenuto = verifysecond(message, 'addhaimai')
        if contenuto == 'false':
            nontrovato(message, '/addhaimai [haimai]')
        elif cercaoperatoredaid(message) is None:
            try_to(message, 'Devi essere operatore per svolgere questa operazione ❌')
        elif '?' not in contenuto:
            try_to(message, "Nell'hai mai ci deve essere un punto di domanda ❌")
        elif 'hai mai' not in contenuto.lower():
            try_to(message, "Nell'hai mai ci deve essere scritto almeno una volta hai mai ❌")
        else:
            dbhaimai.insert_one({'haimai': contenuto, 'autore': message.from_user.id})
            try_to(message, "✅ » <i>Hai mai aggiunta correttamente</i>")
            removehaimai = types.InlineKeyboardMarkup()
            btnElimina = types.InlineKeyboardButton(text='Cancella ❌', callback_data='delhaimai')
            removehaimai.add(btnElimina)
            bot.send_message(canale_log, '#Addhaimai\n• Hai mai: ' + str(contenuto), reply_markup=removehaimai)
        # ! Delask


@bot.callback_query_handler(func=lambda c: c.data == 'delask')
def delask(call):
    try:
        trova = dbask.find_one({'ask': call.message.text.replace('#Addask\n• Ask: ', '')})
        if trova is not None:
            if trova['autore'] == call.from_user.id or call.from_user.id == 1914266767:
                dbask.delete_many({'ask': call.message.text.replace('#Addask\n• Ask: ', '')})
                bot.answer_callback_query(call.id, '✅ Domanda cancellata correttamente')
                bot.edit_message_text(call.message.text + '\n\n❌ Cancellato', call.message.chat.id,
                                      call.message.message_id)
            else:
                bot.answer_callback_query(call.id, "❌ devi essere l'autore della domanda per cancellarla",
                                          show_alert=True)
        else:
            bot.answer_callback_query(call.id, "❌ Domanda non trovata ")

    except Exception as ex:
        salvaerrore(ex)


# ! Delask
@bot.callback_query_handler(func=lambda c: c.data == 'delhaimai')
def delask(call):
    try:
        trova = dbhaimai.find_one({'haimai': call.message.text.replace('#Addhaimai\n• Hai mai: ', '')})
        if trova is not None:
            if trova['autore'] == call.from_user.id or call.from_user.id == 1914266767:
                dbhaimai.delete_many({'haimai': call.message.text.replace('#Addhaimai\n• Hai mai: ', '')})
                bot.answer_callback_query(call.id, '✅ Hai mai cancellato correttamente')
                bot.edit_message_text(call.message.text + '\n\n❌ Cancellato', call.message.chat.id,
                                      call.message.message_id)
            else:
                bot.answer_callback_query(call.id, "❌ devi essere l'autore dell' hai mai per cancellarla",
                                          show_alert=True)
        else:
            bot.answer_callback_query(call.id, "❌ Hai mai non trovato")

    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'delaskhot')
def delaskhot(call):
    try:
        trova = dbaskhot.find_one({'askhot': call.message.text.replace('#Addaskhot\n• ask hot: ', '')})
        if trova is not None:
            if trova['autore'] == call.from_user.id or call.from_user.id == 1914266767:
                dbaskhot.delete_many({'askhot': call.message.text.replace('#Addaskhot\n• ask hot: ', '')})
                bot.answer_callback_query(call.id, '✅ ask hot cancellato correttamente')
                bot.edit_message_text(call.message.text + '\n\n❌ Cancellato', call.message.chat.id,
                                      call.message.message_id)
            else:
                bot.answer_callback_query(call.id, "❌ devi essere l'autore dell' ask hot per cancellarla",
                                          show_alert=True)
        else:
            bot.answer_callback_query(call.id, "❌ ask hot non trovato")

    except Exception as ex:
        salvaerrore(ex)


# * Comando arresta
# cazzeggio
@bot.edited_message_handler(commands=['arresta', 'ARRESTA'], chat_types='supergroup')
@bot.message_handler(commands=['arresta', 'ARRESTA'], chat_types='supergroup')
def startarresta(message): Thread(target=arresta, args=[message]).start()


def arresta(message):
    try:
        if chatblacklist(message.chat.id) is True:
            yos = [' è riuscito a sfuggire alla polizia 🏃 ', " è stato arrestato 🚓 "]
            id = verifica_esistenza(message)
            if id is not False:
                bot.send_message(message.chat.id, "🎲 » <i>" + namechanger(message.reply_to_message.from_user.first_name,
                                                                          message.reply_to_message.from_user.id) + str(
                    random.choice(yos)) + "</i>", reply_to_message_id=message.reply_to_message.message_id,
                                 parse_mode="html")
            else:
                bot.send_message(message.chat.id,
                                 "🎲 » <i>" + namechanger(message.from_user.first_name, message.from_user.id) + str(
                                     random.choice(yos)) + "</i>", parse_mode="html")
    except Exception as ex:
        salvaerrore(ex)


# * Omofobometro
@bot.edited_message_handler(commands=['omofobometro', 'OMOFOBOMETRO'], chat_types='supergroup')
@bot.message_handler(commands=['omofobometro', 'OMOFOBOMETRO'], chat_types='supergroup')
def startomofobometro(message): Thread(target=omofobometro, args=[message]).start()


def omofobometro(message):
    try:
        if chatblacklist(message.chat.id) is True:
            try_to(message,
                   "🎲 »<i> " + namechanger(message.from_user.first_name, message.from_user.id) + " è omofobo al " + str(
                       random.randint(0, 100)) + " % 🏳️‍🌈⃠</i>")
    except Exception as ex:
        salvaerrore(ex)


# * Nazimometro

@bot.edited_message_handler(commands=['nazimometro', 'NAZIMOMETRO'], chat_types='supergroup')
@bot.message_handler(commands=['nazimometro', 'NAZIMOMETRO'], chat_types='supergroup')
def startnazimometro(message): Thread(target=nazimometro, args=[message]).start()


def nazimometro(message):
    try:
        if chatblacklist(message.chat.id) is True:
            try_to(message,
                   "🎲 »<i> " + namechanger(message.from_user.first_name, message.from_user.id) + " è nazista al " + str(
                       random.randint(0, 100)) + " % 🔥</i>")
    except Exception as ex:
        salvaerrore(ex)


# * oroscopo
def creaoroscopo(message):
    try:
        amore = random.randint(0, 10)
        lavoro = random.randint(0, 10)
        benessere = random.randint(0, 10)
        fortuna = random.randint(0, 10)
        intelligenza = random.randint(0, 10)
        nerd = random.randint(0, 10)
        prossimo = time.time() + 86400.0
        bot.send_message(message.chat.id, "<b> Oroscopo di " + namechanger(message.from_user.first_name,
                                                                           message.from_user.id) + "</b>\n\n" +
                         "<i>💖 Amore: </i><code>" + str(amore) + "</code>\n" +
                         "<i>👷 Lavoro: </i><code>" + str(lavoro) + "</code>\n" +
                         "<i>🥗 Salute: </i><code>" + str(benessere) + "</code>\n" +
                         "<i>🎰 Fortuna: </i><code>" + str(fortuna) + "</code>\n" +
                         "<i>🧠 Intelligenza: </i><code>" + str(intelligenza) + "</code>\n" +
                         "<i>🤓 Nerd: </i><code>" + str(nerd) + "</code>\n", parse_mode="html"
                         )
        dboroscopo.insert_one({
            "amore": amore,
            "lavoro": lavoro,
            "salute": benessere,
            "fortuna": fortuna,
            "intelligenza": intelligenza,
            "nerd": nerd,
            "utente": message.from_user.id,
            "prossimo": prossimo
        })
    except Exception as ex:
        salvaerrore(ex)


def getoroscopo(message):
    try:
        oro = dboroscopo.find_one({'utente': message.from_user.id})
        if oro is None:
            creaoroscopo(message)
        elif oro["prossimo"] < time.time() and oro is not None:
            dboroscopo.delete_many({'utente': message.from_user.id})
            creaoroscopo(message)
        else:
            bot.send_message(message.chat.id, "<b> Oroscopo di " + namechanger(message.from_user.first_name,
                                                                               message.from_user.id) + "</b>\n\n" +
                             "<i>💖 Amore: </i><code>" + str(oro["amore"]) + "</code>\n" +
                             "<i>👷 Lavoro: </i><code>" + str(oro["lavoro"]) + "</code>\n" +
                             "<i>🥗 Salute: </i><code>" + str(oro["salute"]) + "</code>\n" +
                             "<i>🎰 Fortuna: </i><code>" + str(oro["fortuna"]) + "</code>\n" +
                             "<i>🧠 Intelligenza: </i><code>" + str(oro["intelligenza"]) + "</code>\n" +
                             "<i>🤓 Nerd: </i><code>" + str(oro["nerd"]) + "</code>\n", parse_mode="html"
                             )
    except Exception as ex:
        salvaerrore(ex)


@bot.edited_message_handler(commands=['oroscopo', 'OROSCOPO'], chat_types='supergroup')
@bot.message_handler(commands=['oroscopo', 'OROSCOPO'], chat_types='supergroup')
def startbagasciamometro(message): Thread(target=ori, args=[message]).start()


def ori(message):
    try:
        if chatblacklist(message.chat.id) is True:
            getoroscopo(message)
    except Exception as ex:
        salvaerrore(ex)


# * bagasciamometro
@bot.edited_message_handler(commands=['bagasciamometro', 'BAGASCIAMOMETRO'], chat_types='supergroup')
@bot.message_handler(commands=['bagasciamometro', 'BAGASCIAMOMETRO'], chat_types='supergroup')
def startbagasciamometro(message): Thread(target=bagasciamometro, args=[message]).start()


def bagasciamometro(message):
    try:
        if chatblacklist(message.chat.id) is True:
            try_to(message,
                   "🎲 »<i> " + namechanger(message.from_user.first_name,
                                           message.from_user.id) + " è bagascia al " + str(
                       random.randint(0, 100)) + " % 🙇‍♀️</i>")
    except Exception as ex:
        salvaerrore(ex)
    # * Maranzamometro


@bot.edited_message_handler(commands=['maranzamometro', 'MARANZAMOMETRO'], chat_types='supergroup')
@bot.message_handler(commands=['maranzamometro', 'MARANZAMOMETRO'], chat_types='supergroup')
def startmaranzamometro(message): Thread(target=maranzamometro, args=[message]).start()


def maranzamometro(message):
    try:
        if chatblacklist(message.chat.id) is True:
            try_to(message,
                   "🎲 »<i> " + namechanger(message.from_user.first_name, message.from_user.id) + " è maranza al " + str(
                       random.randint(0, 100)) + " % 🥷</i>")
    except Exception as ex:
        salvaerrore(ex)


# * Infamometro

@bot.edited_message_handler(commands=['infamometro', 'INFAMOMETRO'], chat_types='supergroup')
@bot.message_handler(commands=['infamometro', 'INFAMOMETRO'], chat_types='supergroup')
def startoinfamometro(message): Thread(target=infamometro, args=[message]).start()


def infamometro(message):
    try:
        if chatblacklist(message.chat.id) is True:
            try_to(message,
                   "🎲 »<i> " + namechanger(message.from_user.first_name, message.from_user.id) + " è infame al " + str(
                       random.randint(0, 100)) + " % 👿</i>")
    except Exception as ex:
        salvaerrore(ex)


@bot.message_handler(commands=['ritardometro', 'RITARDOMETRO'], chat_types='supergroup')
@bot.edited_message_handler(commands=['ritardometro', 'RITARDOMETRO'], chat_types='supergroup')
def startritardometro(message): Thread(target=ritardometro, args=[message]).start()


def ritardometro(message):
    try:
        if chatblacklist(message.chat.id):
            try_to(message,
                   f'🎲 » <i> {namechanger(message.from_user.first_name, message.from_user.id)} è ritardato al {str(random.randint(0, 100))}% 😳')

    except Exception as ex:
        salvaerrore(ex)

    # * Coglionometro


@bot.edited_message_handler(commands=['coglionometro', 'COGLIONOMETRO'], chat_types='supergroup')
@bot.message_handler(commands=['coglionometro', 'COGLIONOMETRO'], chat_types='supergroup')
def startocoglionometro(message): Thread(target=coglionometro, args=[message]).start()


def coglionometro(message):
    try:
        if chatblacklist(message.chat.id) is True:
            try_to(message,
                   "🎲 »<i> " + namechanger(message.from_user.first_name,
                                           message.from_user.id) + " è coglione al " + str(
                       random.randint(0, 100)) + " % 🌵</i>")
    except Exception as ex:
        salvaerrore(ex)


# * Bellometro

@bot.edited_message_handler(commands=['bellometro', 'BELLOMETRO'], chat_types='supergroup')
@bot.message_handler(commands=['bellometro', 'BELLOMETRO'], chat_types='supergroup')
def startbellometro(message): Thread(target=bellometro, args=[message]).start()


def bellometro(message):
    try:
        if chatblacklist(message.chat.id) is True:
            try_to(message,
                   "🎲 »<i> " + namechanger(message.from_user.first_name, message.from_user.id) + " è bello al " + str(
                       random.randint(0, 100)) + " % 😎</i>")
    except Exception as ex:
        salvaerrore(ex)


# * Cringiometro

@bot.edited_message_handler(commands=['cringiometro', 'CRINGIOMETRO'], chat_types='supergroup')
@bot.message_handler(commands=['cringiometro', 'CRINGIOMETRO'], chat_types='supergroup')
def startcringiometro(message): Thread(target=cringiometro, args=[message]).start()


def cringiometro(message):
    try:
        if chatblacklist(message.chat.id) is True:
            try_to(message,
                   "🎲 »<i> " + namechanger(message.from_user.first_name, message.from_user.id) + " è cringe al " + str(
                       random.randint(0, 100)) + " % 🥶</i>")
    except Exception as ex:
        salvaerrore(ex)


# * Albanemometro

@bot.edited_message_handler(commands=['albanemometro', 'ALBANEMOMETRO'], chat_types='supergroup')
@bot.message_handler(commands=['albanemometro', 'ALBANEMOMETRO'], chat_types='supergroup')
def startalbanemometro(message): Thread(target=albanemometro, args=[message]).start()


def albanemometro(message):
    try:
        if chatblacklist(message.chat.id) is True:
            try_to(message,
                   "🎲 »<i> " + namechanger(message.from_user.first_name,
                                           message.from_user.id) + " è albanese al " + str(
                       random.randint(0, 100)) + " % 🇦🇱</i>")
    except Exception as ex:
        salvaerrore(ex)


# * napolometro

@bot.edited_message_handler(commands=['napolometro', 'NAPOLOMETRO'], chat_types='supergroup')
@bot.message_handler(commands=['napolometro', 'NAPOLOMETRO'], chat_types='supergroup')
def startnapolometro(message): Thread(target=napolometro, args=[message]).start()


def napolometro(message):
    try:
        if chatblacklist(message.chat.id) is True:
            try_to(message,
                   "🎲 »<i> " + namechanger(message.from_user.first_name,
                                           message.from_user.id) + " è napoletano al " + str(
                       random.randint(0, 100)) + " % 🍕</i>")
    except Exception as ex:
        salvaerrore(ex)


# * crucconometro

@bot.edited_message_handler(commands=['crucconometro', 'CRUCCONOMETRO'], chat_types='supergroup')
@bot.message_handler(commands=['crucconometro', 'CRUCCONOMETRO'], chat_types='supergroup')
def startcrucconometro(message): Thread(target=crucconometro, args=[message]).start()


def crucconometro(message):
    try:
        if chatblacklist(message.chat.id) is True:
            try_to(message,
                   "🎲 »<i> " + namechanger(message.from_user.first_name, message.from_user.id) + " è crucco al " + str(
                       random.randint(0, 100)) + " % 🇩🇪</i>")
    except Exception as ex:
        salvaerrore(ex)


# * Orgia

@bot.message_handler(commands=['orgia', 'ORGIA'], chat_types='supergroup')
@bot.edited_message_handler(commands=['orgia', 'ORGIA'], chat_types='supergroup')
def startorgia(message): Thread(target=orgia, args=[message]).start()


def orgia(message):
    try:
        if chatblacklist(message.chat.id) is True:
            tastiera = types.InlineKeyboardMarkup()
            unisciti = types.InlineKeyboardButton(text='Unisciti 🚪', callback_data='uniscitiorgia')
            tastiera.add(unisciti)
            inizia = types.InlineKeyboardButton(text='Inizia 🏁', callback_data='startorgia')
            elimina = types.InlineKeyboardButton(text='Elimina 🗑', callback_data='eliminaorgia')
            tastiera.add(inizia, elimina)
            x = bot.send_message(message.chat.id,
                                 "Nuova orgia 🔞\n\n🫂 Membri:\n• " + namechanger(message.from_user.first_name,
                                                                                message.from_user.id),
                                 reply_markup=tastiera, parse_mode='html')
            dbinfo.insert_one(
                {'orgia': x.message_id, 'utente': message.from_user.id, 'nomeutente': message.from_user.first_name,
                 'ruolo': 'fondatore'})
    except Exception as ex:
        salvaerrore(ex)


def sforna_bambini(xid, xname, yid, yname, call):
    try:
        PEXELS_API_KEY = '563492ad6f91700001000001225b3fb640394047b89c432cab11ebbc'
        api = API(PEXELS_API_KEY)
        ser = "baby"
        api.search(str(ser), page=1, results_per_page=80)
        photos = api.get_entries()
        nome = random.randint(0, 1699)
        cognome = random.randint(0, 37205)
        name = db_baby_name.find_one({'id': nome})
        surname = db_baby_surname.find_one({'id': cognome})
        fota = str(photos[random.randint(0, 79)].original) + "?auto=compress&cs=tinysrgb&dpr=2&h=700&w=1200"
        bot.send_photo(call.message.chat.id, fota,
                       caption="👼 » <i>" + namechanger(xname, xid) + " ha fatto un bambino con " + namechanger(yname,
                                                                                                               yid) + "\n🏷 »  " + str(
                           name['name']) + " " + str(surname['name']) + "</i>", parse_mode="html")
        print('trurh: ' + str(fota))
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'startorgia')
def inziaorgia(call):
    try:
        cerca = dbinfo.find_one(
            {'orgia': call.message.message_id, 'utente': call.from_user.id, 'nomeutente': call.from_user.first_name,
             'ruolo': 'fondatore'})
        documents = dbinfo.find({'orgia': call.message.message_id})
        num = dbinfo.find({'orgia': call.message.message_id}).count()
        print(num)
        if cerca is None:
            bot.answer_callback_query(call.id, "❌ » Non puoi eseguire quest'azione perchè non hai creato te l'orgia",
                                      show_alert=True)
        elif num < 2:
            bot.answer_callback_query(call.id, "❌ » Ci devono essere almeno 3 persone per iniziare un'orgia",
                                      show_alert=True)
        else:
            id = []
            names = []
            for document in documents:
                id.append(str(document['utente']))
                names.append(str(document['nomeutente']))
            print(names)

            x = random.randint(0, len(id) - 1)
            y = random.randint(0, len(id) - 1)
            while x == y:
                y = random.randint(0, len(id) - 1)
            sforna_bambini(id[x], names[x], id[y], names[y], call)
            if num >= 4:
                x = random.randint(0, len(id) - 1)
                y = random.randint(0, len(id) - 1)
                while x == y:
                    y = random.randint(0, len(id) - 1)
                sforna_bambini(id[x], names[x], id[y], names[y], call)
            if num >= 5:
                x = random.randint(0, len(id) - 1)
                y = random.randint(0, len(id) - 1)
                while x == y:
                    y = random.randint(0, len(id) - 1)
                sforna_bambini(id[x], names[x], id[y], names[y], call)
            bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'eliminaorgia')
def eliminaorgia(call):
    try:
        cerca = dbinfo.find_one(
            {'orgia': call.message.message_id, 'utente': call.from_user.id, 'nomeutente': call.from_user.first_name,
             'ruolo': 'fondatore'})
        if cerca is None:
            bot.answer_callback_query(call.id, "❌ » Non puoi eseguire quest'azione perchè non hai creato te l'orgia",
                                      show_alert=True)
        else:
            bot.answer_callback_query(call.id, "❌ » Orgia eliminata", show_alert=True)
            bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'uniscitiorgia')
def entraorgia(call):
    try:
        cerca = dbinfo.find_one(
            {'orgia': call.message.message_id, 'utente': call.from_user.id, 'nomeutente': call.from_user.first_name})
        if cerca != None:
            bot.answer_callback_query(call.id, "❌ » Sei già dentro questa orgia", show_alert=True)
        else:
            tastiera = types.InlineKeyboardMarkup()
            unisciti = types.InlineKeyboardButton(text='Unisciti 🚪', callback_data='uniscitiorgia')
            tastiera.add(unisciti)
            inizia = types.InlineKeyboardButton(text='Inizia 🏁', callback_data='startorgia')
            elimina = types.InlineKeyboardButton(text='Elimina 🗑', callback_data='eliminaorgia')
            tastiera.add(inizia, elimina)
            dbinfo.insert_one(
                {'orgia': call.message.message_id, 'utente': call.from_user.id, 'nomeutente': call.from_user.first_name,
                 'ruolo': 'utente'})
            bot.answer_callback_query(call.id, "✅ » Ti sei unito correttamente all'orgia", show_alert=True)
            bot.edit_message_text(
                call.message.text + "\n• " + namechanger(call.from_user.first_name, call.from_user.id),
                call.message.chat.id, call.message.message_id, parse_mode='html', reply_markup=tastiera)
    except Exception as ex:
        salvaerrore(ex)


# * Nazismo

@bot.edited_message_handler(commands=['nazismo', 'NAZISMO'], chat_types='supergroup')
@bot.message_handler(commands=['nazismo', 'NAZISMO'], chat_types='supergroup')
def startnazismo(message): Thread(target=nazismo, args=[message]).start()


def nazismo(message):
    try:
        if chatblacklist(message.chat.id) is True:
            try_to(message,
                   "🎲 »<i> " + namechanger(message.from_user.first_name, message.from_user.id) + " ha ucciso " + str(
                       random.randint(0, 10000)) + " ebrei 👨‍🦰</i>")
    except Exception as ex:
        salvaerrore(ex)


# * Intelligentemometro

@bot.edited_message_handler(commands=['intelligentemometro', 'INTELLIGENTEMOMETRO'], chat_types='supergroup')
@bot.message_handler(commands=['intelligentemometro', 'INTELLIGENTEMOMETRO'], chat_types='supergroup')
def startintelligentemometro(message): Thread(target=intelligentemometro, args=[message]).start()


def intelligentemometro(message):
    try:
        if chatblacklist(message.chat.id) is True:
            try_to(message, "🎲 »<i> " + namechanger(message.from_user.first_name,
                                                    message.from_user.id) + " è intelligente al " + str(
                random.randint(0, 100)) + " % 🧠</i>")
    except Exception as ex:
        salvaerrore(ex)


# * Friendzone

@bot.edited_message_handler(commands=['friendzone', 'FRIENDZONE'], chat_types='supergroup')
@bot.message_handler(commands=['friendzone', 'FRIENDZONE'], chat_types='supergroup')
def startfriendzone(message): Thread(target=friendzone, args=[message]).start()


def friendzone(message):
    if chatblacklist(message.chat.id) is True:
        yos = ['Cicciogamer', "una suora", "Giuseppe Simone", "Matteo Salvini", "Un frocio", "una prof", "un prof",
               "un'amica", "un'amico", "Follettina Creation", "un cane", "una cagnolina", "Elon Mask", "Greta Menchi"]
        try:
            try_to(message, "💔 » <i>" + namechanger(message.from_user.first_name,
                                                    message.from_user.id) + " è stato friendzonato da " + str(
                random.choice(yos)) + "</i>")
        except Exception as ex:
            salvaerrore(ex)


# * Silicone

@bot.edited_message_handler(commands=['silicone', 'SILICONE'], chat_types='supergroup')
@bot.message_handler(commands=['silicone', 'SILICONE'], chat_types='supergroup')
def startsilicone(message): Thread(target=silicone, args=[message]).start()


def silicone(message):
    if chatblacklist(message.chat.id) is True:
        lucky = random.randint(0, 10)
        if lucky == 10:
            incrementa_decrementa_stato(message.from_user.first_name, message.from_user.id, "seno", "togli")
            try_to(message, "🍐 » <i> a " + namechanger(message.from_user.first_name,
                                                       message.from_user.id) + " gli si sono ammosciate le tette")
        else:
            incrementa_decrementa_stato(message.from_user.first_name, message.from_user.id, "seno", "+")
            utente = controlla_e_crea(message.from_user.first_name, message.from_user.id)
            try_to(message, "🍐 » " + namechanger(message.from_user.first_name, message.from_user.id) + " ha una " + str(
                utente['seno']) + "°")


# * allunga

@bot.edited_message_handler(commands=['allunga', 'ALLUNGA'], chat_types='supergroup')
@bot.message_handler(commands=['allunga', 'ALLUNGA'], chat_types='supergroup')
def startsilicone(message): Thread(target=allunga, args=[message]).start()


def allunga(message):
    if chatblacklist(message.chat.id) is True:
        lucky = random.randint(0, 10)
        if lucky == 10:
            incrementa_decrementa_stato(message.from_user.first_name, message.from_user.id, "cazzo", "togli")
            try_to(message, "🍆 » <i> " + namechanger(message.from_user.first_name,
                                                     message.from_user.id) + " ti è caduto il cazzo</i>")
        else:
            incrementa_decrementa_stato(message.from_user.first_name, message.from_user.id, "cazzo", "+")
            utente = controlla_e_crea(message.from_user.first_name, message.from_user.id)
            try_to(message, "🍆 » <i>" + namechanger(message.from_user.first_name,
                                                    message.from_user.id) + " ha il cazzo che misura " + str(
                utente['cazzo']) + " cm </i>")


# * Operatore

@bot.edited_message_handler(commands=['operatore', 'OPERATORE'], chat_types='supergroup')
@bot.message_handler(commands=['operatore', 'OPERATORE'], chat_types='supergroup')
def startoperatore(message): Thread(target=operatore, args=[message]).start()


def operatore(message):
    if chatblacklist(message.chat.id) is True:
        if message.from_user.id == 1914266767:
            id = verifica_esistenza(message)
            try:
                if id == False:
                    try_to(message, "🧐 » <i>Deve rispondere al messaggio dell'utente che vuole rendere operatore</i>")
                else:
                    trova = cercaoperatore(message)
                    if trova != None:
                        try_to(message, "😅 » <i>L'operatore da lei selezionato esiste già</i>")
                    else:
                        dbruoli.insert_one({"id": id, "aggiunta": message.from_user.id, "ruolo": "operatore"})
                        try_to(message, "👮 » <i>" + namechanger(message.reply_to_message.from_user.first_name,
                                                                message.reply_to_message.from_user.id) + " aggiunto correttamente tra gli operatori</i>")
            except Exception as ex:
                salvaerrore(ex)


# * Unoperatore

@bot.edited_message_handler(commands=['unoperatore', 'UNOPERATORE'], chat_types='supergroup')
@bot.message_handler(commands=['unoperatore', 'UNOPERATORE'], chat_types='supergroup')
def startunoperatore(message): Thread(target=unoperatore, args=[message]).start()


def unoperatore(message):
    if chatblacklist(message.chat.id) is True:
        if message.from_user.id == 1914266767:
            id = verifica_esistenza(message)
            try:
                if id == False:
                    try_to(message,
                           "🧐 » <i>Deve rispondere al messaggio dell'utente a cui vuole togliere il ruolo di operatore</i>")
                else:
                    trova = cercaoperatore(message)
                    if trova != None:
                        dbruoli.delete_one({"id": id, "ruolo": "operatore"})
                        try_to(message, "👮 » <i>" + namechanger(message.reply_to_message.from_user.first_name,
                                                                message.reply_to_message.from_user.id) + " rimosso correttamente dal ruolo di operatore</i>")
                    else:
                        try_to(message, "😅 » <i>L'utente selezionato non è operatore</i>")

            except Exception as ex:
                salvaerrore(ex)


# * Sesso
@bot.edited_message_handler(commands=['sesso', 'SESSO'], chat_types='supergroup')
@bot.message_handler(commands=['sesso', 'SESSO'], chat_types='supergroup')
def startsesso(message): Thread(target=sesso, args=[message]).start()


def sesso(message):
    if chatblacklist(message.chat.id) is True:
        id = verifica_esistenza(message)
        if id == False:
            try_to(message, "🧐 » <i>Deve rispondere al messaggio dell'utente che vuoi scopare</i>")
        elif message.from_user.id == message.reply_to_message.from_user.id:
            try_to(message, "<i>🛠» Non puoi autoscoparti </i>")
        else:
            try:
                if random.randint(0, 4) < 4:
                    bot.send_message(message.chat.id, "👼 » <i>" + namechanger(message.from_user.first_name,
                                                                              message.from_user.id) + " ha scopato  " + namechanger(
                        message.reply_to_message.from_user.first_name,
                        message.reply_to_message.from_user.id) + " senza fare bambini</i>", parse_mode="html")
                else:
                    PEXELS_API_KEY = '563492ad6f91700001000001225b3fb640394047b89c432cab11ebbc'
                    api = API(PEXELS_API_KEY)
                    ser = "baby"
                    api.search(str(ser), page=1, results_per_page=80)
                    photos = api.get_entries()
                    nome = random.randint(0, 1699)
                    cognome = random.randint(0, 37205)
                    name = db_baby_name.find_one({'id': nome})
                    surname = db_baby_surname.find_one({'id': cognome})

                    fota = str(photos[random.randint(0, 79)].original) + "?auto=compress&cs=tinysrgb&dpr=2&h=700&w=1200"
                    bot.send_photo(message.chat.id, fota, caption="👼 » <i>" + namechanger(message.from_user.first_name,
                                                                                          message.from_user.id) + " ha fatto un bambino con " + namechanger(
                        message.reply_to_message.from_user.first_name,
                        message.reply_to_message.from_user.id) + "\n🏷 »  " + str(name['name']) + " " + str(
                        surname['name']) + "</i>", parse_mode="html")
            except Exception as ex:
                salvaerrore(ex)


@bot.edited_message_handler(commands=['sputainculo', 'SPUTAINCULO'], chat_types='supergroup')
@bot.message_handler(commands=['sputainculo', 'SPUTAINCULO'], chat_types='supergroup')
def startsputa(message): Thread(target=sputa, args=[message]).start()


def sputa(message):
    if chatblacklist(message.chat.id) is True:
        id = verifica_esistenza(message)
        if id == False:
            try_to(message, "🧐 » <i>Deve rispondere al messaggio dell'utente a cui vuoi sputare in culo</i>")
        else:
            try:
                bot.send_message(message.chat.id, "💦 » <i>" + namechanger(message.from_user.first_name,
                                                                          message.from_user.id) + " ha sputato in culo a " + namechanger(
                    message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.id) + "</i>",
                                 parse_mode="html")
            except Exception as ex:
                salvaerrore(ex)


@bot.edited_message_handler(commands=['leccafiga', 'LECCAFIGA'], chat_types='supergroup')
@bot.message_handler(commands=['leccafiga', 'LECCAFIGA'], chat_types='supergroup')
def startlecca(message): Thread(target=lecca, args=[message]).start()


def lecca(message):
    if chatblacklist(message.chat.id) is True:
        id = verifica_esistenza(message)
        if id == False:
            try_to(message, "🧐 » <i>Deve rispondere al messaggio dell'utente a cui vuoi leccare la figa</i>")
        else:
            try:
                bot.send_message(message.chat.id, "👅 » <i>" + namechanger(message.from_user.first_name,
                                                                          message.from_user.id) + " Ha leccato la figa di " + namechanger(
                    message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.id) + "</i>",
                                 parse_mode="html")
            except Exception as ex:
                salvaerrore(ex)


# * abusa
@bot.edited_message_handler(commands=['abusa', 'ABUSA'], chat_types='supergroup')
@bot.message_handler(commands=['abusa', 'ABUSA'], chat_types='supergroup')
def startabusa(message): Thread(target=abusa, args=[message]).start()


def abusa(message):
    if chatblacklist(message.chat.id) is True:
        id = verifica_esistenza(message)
        if not id:
            try_to(message, "🧐 » <i>Deve rispondere al messaggio dell'utente che vuoi abusare</i>")
        else:
            try:
                bot.send_message(message.chat.id, "😈 » <i>" + namechanger(message.from_user.first_name,
                                                                          message.from_user.id) + " ha abusato sessualmente di  " + namechanger(
                    message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.id) + "</i>",
                                 parse_mode="html")
            except Exception as ex:
                salvaerrore(ex)


# * Abbrraccio
@bot.edited_message_handler(commands=['abbraccio', 'ABBRACCIO'], chat_types='supergroup')
@bot.message_handler(commands=['abbraccio', 'ABBRACCIO'], chat_types='supergroup')
def startabbraccio(message): Thread(target=abbraccio, args=[message]).start()


def abbraccio(message):
    if chatblacklist(message.chat.id) is True:
        id = verifica_esistenza(message)
        if id == False:
            try_to(message, "🧐 » <i>Deve rispondere al messaggio dell'utente che vuoi abbracciare</i>")
        else:
            try:
                PEXELS_API_KEY = '563492ad6f91700001000001225b3fb640394047b89c432cab11ebbc'
                api = API(PEXELS_API_KEY)
                ser = "hug"
                api.search(str(ser), page=1, results_per_page=80)
                photos = api.get_entries()
                fota = str(photos[random.randint(0, 79)].original) + "?auto=compress&cs=tinysrgb&dpr=2&h=700&w=1200"
                bot.send_photo(message.chat.id, fota, caption="🤗 » <i>" + namechanger(message.from_user.first_name,
                                                                                      message.from_user.id) + " ha abbracciato " + namechanger(
                    message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.id) + "</i>",
                               parse_mode="html")
                print('trurh: ' + str(fota))
            except Exception as ex:
                salvaerrore(ex)


# * Abbrraccio
@bot.edited_message_handler(commands=['bacia', 'BACIA'], chat_types='supergroup')
@bot.message_handler(commands=['bacia', 'BACIA'], chat_types='supergroup')
def startabacia(message): Thread(target=bacia, args=[message]).start()


def bacia(message):
    if chatblacklist(message.chat.id) is True:
        id = verifica_esistenza(message)
        if id == False:
            try_to(message, "🧐 » <i>Deve rispondere al messaggio dell'utente che vuoi baciare</i>")
        else:
            try:
                PEXELS_API_KEY = '563492ad6f91700001000001225b3fb640394047b89c432cab11ebbc'
                api = API(PEXELS_API_KEY)
                ser = "kiss"
                api.search(str(ser), page=1, results_per_page=80)
                photos = api.get_entries()
                fota = str(photos[random.randint(0, 79)].original) + "?auto=compress&cs=tinysrgb&dpr=2&h=700&w=1200"
                bot.send_photo(message.chat.id, fota, caption="😘 » <i>" + namechanger(message.from_user.first_name,
                                                                                      message.from_user.id) + " ha baciato  " + namechanger(
                    message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.id) + "</i>",
                               parse_mode="html")
                print('trurh: ' + str(fota))
            except Exception as ex:
                salvaerrore(ex)


# * dog

@bot.edited_message_handler(commands=['dog', 'DOG'], chat_types='supergroup')
@bot.message_handler(commands=['dog', 'DOG'], chat_types='supergroup')
def startdog(message):
    Thread(target=dog, args=[message]).start()


def dog(message):
    if chatblacklist(message.chat.id) is True:
        try:
            response = requests.get('https://api.thedogapi.com/v1/images/search')
            risposta = response.json()
            foto = str(risposta[0]['url'])
            bot.send_photo(message.chat.id, foto)
        except Exception as ex:
            salvaerrore(ex)


# * calcolo livello
def calcolo_livello(esperienza):
    calcolo = math.floor(esperienza / 1000)
    prossimo = calcolo + 1
    return "<b>" + str(calcolo) + "</b>" + "(" + str(esperienza) + "/" + str(prossimo * 1000)


# * stato

@bot.edited_message_handler(commands=['stato', 'STATO'], chat_types='supergroup')
@bot.message_handler(commands=['stato', 'STATO'], chat_types='supergroup')
def startstato(message): Thread(target=stato, args=[message]).start()


def stato(message):
    try:
        if chatblacklist(message.chat.id) is True:
            recordo = controlla_e_crea(message.from_user.first_name, message.from_user.id)
            tastiera = types.InlineKeyboardMarkup()
            likes = types.InlineKeyboardButton(text=f"❤️ {recordo['like']}", callback_data='Laiks')
            dislikes = types.InlineKeyboardButton(text=f"👎 {recordo['dislike']}", callback_data='Dislaiks')
            tastiera.add(likes, dislikes)
            rispetto = types.InlineKeyboardButton(text=f"🎉 {recordo['rispetto']}", callback_data='Rispettus')
            bestemmie = types.InlineKeyboardButton(text=f"🐖 {recordo['bestemmie']}", callback_data='Bestemmius')
            tastiera.add(rispetto, bestemmie)

            bot.send_message(message.chat.id, "<b>Stato di " + namechanger(message.from_user.first_name,
                                                                           message.from_user.id) + "📊</b> \n" +
                             "<i>🌟 livello </i><code>" + str(calcolo_livello(recordo['esperienza'])).replace(".0",
                                                                                                             "") + ") </code>\n"
                             + "<i>💶 Soldi</i> » <code>" +
                             str(display(recordo['soldi'])) + " </code>\n" + "<i>💎 Diamanti</i> » <code>" +
                             str(display(recordo['diamanti'])) + " </code>\n" + "<i>🧃Succhini</i> » <code>" +
                             str(display(recordo['succhini'])) + " </code>"
                             , parse_mode='html', reply_markup=tastiera)


    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'Bestemmius')
def bestemmius(call):
    try:
        bot.answer_callback_query(call.id, "🐖 » Numero di bestemmie del tuo account", show_alert=True)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'Rispettus')
def rispettus(call):
    try:
        bot.answer_callback_query(call.id, "🎉 » Numero di rispetto del tuo account", show_alert=True)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'Laiks')
def laiks(call):
    try:
        bot.answer_callback_query(call.id, "❤️ » Numero di mi piace del tuo account", show_alert=True)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'Dislaiks')
def laiks(call):
    try:
        bot.answer_callback_query(call.id, "👎 » Numero di non mi piace del tuo account", show_alert=True)
    except Exception as ex:
        salvaerrore(ex)


@bot.message_handler(commands=['misure', 'MISURE'], chat_types='supergroup')
@bot.edited_message_handler(commands=['misure', 'MISURE'], chat_types='supergroup')
def startmisure(message): Thread(target=misure, args=[message]).start()


def misure(message):
    try:
        if chatblacklist(message.chat.id) is True:
            recordo = controlla_e_crea(message.from_user.first_name, message.from_user.id)
            try_to(message,
                   f"<b>Misure di {namechanger(message.from_user.first_name, message.from_user.id)} </b>\n\n🍆 <i>Cazzo </i><code>{recordo['cazzo']}</code>\n<i>🍐 Seno </i><code>{recordo['seno']}</code>"
                   )
    except Exception as ex:
        salvaerrore(ex)


# ! Comandi per il controllo dei dati generali della chat

# * Id dell'utente

@bot.edited_message_handler(commands=['myid', 'MYID'], chat_types='supergroup')
@bot.message_handler(commands=['myid', 'MYID'], chat_types='supergroup')
def startmyid(message): Thread(target=myid, args=[message]).start()


def myid(message):
    if chatblacklist(message.chat.id) is True:
        try:
            try_to(message, "🆔 »<i> " + namechanger(message.from_user.first_name,
                                                    message.from_user.id) + " ha l'id : </i><code> " + str(
                message.from_user.id) + "</code>")
        except Exception as ex:
            salvaerrore(ex)


# * Id della chat
@bot.edited_message_handler(commands=['chatid', 'chatid'], chat_types='supergroup')
@bot.message_handler(commands=['chatid', 'chatid'], chat_types='supergroup')
def startchatid(message): Thread(target=chatid, args=[message]).start()


def chatid(message):
    if chatblacklist(message.chat.id) is True:
        try_to(message, "🆔 »<i> Il gruppo ha l'id : </i><code>" + str(message.chat.id) + "</code>")


# * Membri : numero di membri nella chat

@bot.edited_message_handler(commands=['membri', 'MEMBRI'], chat_types='supergroup')
@bot.message_handler(commands=['membri', 'MEMBRI'], chat_types='supergroup')
def membri(message): Thread(target=membr, args=[message]).start()


def membr(message):
    if chatblacklist(message.chat.id) is True:
        try:
            try_to(message,
                   "🫂 » <i>Nel gruppo ci sono " + str(bot.get_chat_member_count(message.chat.id)) + " membri</i>")
        except Exception as ex:
            salvaerrore(ex)


# ! Comandi /cmd [text]  @bot.message_handler(regexp="SOME_REGEXP")
def verify(message, comando):
    try:
        if message.text[0:len(comando) + 2].lower() == "/" + comando + " ":
            return str(message.text[len(comando) + 2:len(message.text)])
        else:
            return False
    except Exception as ex:
        salvaerrore(ex)


def verifysecond(message, comando):
    try:
        if message.text[0:len(comando) + 2].lower() == "/" + comando + " ":
            return str(message.text[len(comando) + 2:len(message.text)])
        else:
            return 'false'
    except Exception as ex:
        salvaerrore(ex)


def nontrovato(message, formattazzione):
    try:
        try_to(message, "🎛 <i>Comando non trovato, forse intendevi </i>»<code>" + str(formattazzione) + "</code>")
    except Exception as ex:
        salvaerrore(ex)


# * Display
def display(value):
    return str(value).replace(".0", "")


# * verify value
def verifyvalue(message, contenuto):
    try:
        x = float(contenuto)
        return True

    except ValueError:
        return False


# * Sfera / palla
@bot.message_handler(regexp='sfera', chat_types='supergroup')
@bot.message_handler(regexp='SFERA', chat_types='supergroup')
@bot.edited_message_handler(regexp='sfera', chat_types='supergroup')
@bot.edited_message_handler(regexp='SFERA', chat_types='supergroup')
@bot.message_handler(regexp='palla', chat_types='supergroup')
@bot.message_handler(regexp='PALLA', chat_types='supergroup')
@bot.edited_message_handler(regexp='palla', chat_types='supergroup')
@bot.edited_message_handler(regexp='PALLA', chat_types='supergroup')
def startpalla(message): Thread(target=palla, args=[message]).start()


def palla(message):
    if chatblacklist(message.chat.id) is True:
        frasi = ['si', 'no', 'è molto probabile', 'è poco probabile', 'ovviamente no', 'ovviamente si', 'certo',
                 'per niente']
        try_to(message, '🔮 <i>La sfera magica dice</i> » ' + str(random.choice(frasi)))


# * pay
@bot.edited_message_handler(regexp='/pay', chat_types='supergroup')
@bot.edited_message_handler(regexp='/PAY', chat_types='supergroup')
@bot.message_handler(regexp='/pay', chat_types='supergroup')
@bot.message_handler(regexp='/PAY', chat_types='supergroup')
def startpay(message): Thread(target=pay, args=[message]).start()


def pay(message):
    if chatblacklist(message.chat.id) is True:
        contenuto = verify(message, 'pay')
        id = verifica_esistenza(message)
        if contenuto == False or verifyvalue(message, contenuto) == False:
            nontrovato(message, "/pay [n succhini]")
        else:
            if id == False:
                try_to(message, "💳 <b>Transizione non riuscita</b> » <i> Rispondi all'utente a cui vuoi donare</i>")
            else:
                record1 = controlla_e_crea(message.from_user.first_name, message.from_user.id)
                record2 = controlla_e_crea(message.reply_to_message.from_user.first_name,
                                           message.reply_to_message.from_user.id)
                if float(contenuto) > float(40000):
                    try_to(message, "💳 <b>Transizione non riuscita</b> » <i> puoi donare massimo 40000 succhini</i>")
                elif id == message.from_user.id:
                    try_to(message, "💳 <b>Transizione non riuscita</b> » <i> Non puoi donare a te stesso</i>")
                elif float(contenuto) < float(0):
                    try_to(message, "💳 <b>Transizione non riuscita</b> » <i> puoi donare minimo 0 succhini</i>")
                elif float(record1['succhini']) < float(40000):
                    try_to(message,
                           "💳 <b>Transizione non riuscita</b> » <i> Non hai abbastanza soldi (Devi avere almeno 40000 in banca) \n🏦Conto:</i><code>" + display(
                               record1['succhini']) + "</code>")
                else:
                    try:
                        dbstato.find_one_and_update({'id': message.from_user.id},
                                                    {"$set": {
                                                        'succhini': float(record1['succhini']) - float(contenuto)}},
                                                    upsert=True)
                        dbstato.find_one_and_update({'id': message.reply_to_message.from_user.id},
                                                    {"$set": {
                                                        'succhini': float(record2['succhini']) + float(contenuto)}},
                                                    upsert=True)
                    except Exception as ex:
                        salvaerrore(ex)
                    try_to(message, "💳 <b>Transizione riuscita</b> »<i> " + namechanger(message.from_user.first_name,
                                                                                        message.from_user.id) + " ha pagato " + namechanger(
                        message.reply_to_message.from_user.first_name,
                        message.reply_to_message.from_user.id) + "</i><code>" + display(contenuto) + "</code> succhini")


# * scommessa
@bot.edited_message_handler(regexp='/scommessa', chat_types='supergroup')
@bot.edited_message_handler(regexp='/SCOMMESSA', chat_types='supergroup')
@bot.message_handler(regexp='/scommessa', chat_types='supergroup')
@bot.message_handler(regexp='/SCOMMESSA', chat_types='supergroup')
def startscommessa(message): Thread(target=scommessa, args=[message]).start()


def scommessa(message):
    if chatblacklist(message.chat.id) is True:
        contenuto = verify(message, 'scommessa')
        if contenuto == False or verifyvalue(message, contenuto) == False:
            nontrovato(message, "/scommessa [n succhini]")
        else:

            record1 = controlla_e_crea(message.from_user.first_name, message.from_user.id)
            if record1['succhini'] < float(contenuto):
                try_to(message,
                       "🏦 <b>Scommessa non riuscita</b> » <i>Non hai abbastanza soldi per eseguire questa scommessa</i> "
                       "\n 🏦 Banca <code>" + display(
                           record1['succhini']) + "</code><i> succhini</i>")
            elif "." in str(contenuto) or "-" in str(contenuto) or "," in str(contenuto):
                try_to(message, " 🏦 <b>Scommessa non riuscita</b> » <i>Devi scommettere numeri interi positivi</i> ")
            else:
                if random.randint(0, 10) < 7:
                    dbstato.find_one_and_update({'id': message.from_user.id},
                                                {"$set": {'succhini': float(record1['succhini']) + float(contenuto)}},
                                                upsert=True)
                    try_to(message, "🥳 <b> complimenti </b> » <i>Hai vinto</i><code> " + display(
                        contenuto) + " </code> <i>succhini</i>")
                else:
                    dbstato.find_one_and_update({'id': message.from_user.id},
                                                {"$set": {'succhini': float(record1['succhini']) - float(contenuto)}},
                                                upsert=True)
                    try_to(message,
                           "😔 <b> cavolo </b> » <i>Hai perso</i><code> " + display(
                               contenuto) + " </code> <i>succhini</i>")


# * Meteo
@bot.edited_message_handler(regexp='/meteo', chat_types='supergroup')
@bot.edited_message_handler(regexp='/METEO', chat_types='supergroup')
@bot.message_handler(regexp='/meteo', chat_types='supergroup')
@bot.message_handler(regexp='/METEO', chat_types='supergroup')
def startmeteo(message): Thread(target=meteo, args=[message]).start()


def meteo(message):
    if chatblacklist(message.chat.id) is True:
        chatblacklist(message.chat.id)
        contenuto = verify(message, 'meteo')
        if contenuto == False:
            nontrovato(message, "/meteo [Luogo]")
        else:
            try:
                response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + contenuto.replace(" ","+") + '&units=Metric&APPID=cee33cf099c0cb10eb63d82dd1b47a18').json()
                if "city not found" in str(response):
                    try_to(message, "🗺 »<i> Luogo non trovato</i>")
                else:
                    meteodic = {
                        'Clear': "Sereno ☀️",
                        'Clouds': "Nuvoloso 🌤 ",
                        'Mist': 'Foschia ❗',
                        'Smoke': "Fumo nell'aria 🚬",
                        'Haze': "Caligine 💭",
                        'Dust': "Vortici di sabbia/polvere ⏳",
                        'Fog': "Nebbia 🌫",
                        'Ash': "cenere vulcanica 🌋",
                        'Squall': " Bufera ☃️",
                        'Tornado':'Tornado 🌪',
                        'Snow' : 'Nevicate ❄️',
                        "Rain" : "Pioggie 🌧",
                        "Drizzle": "Pioggerella 🌦",
                        "Thunderstorm" : "Temporali ⛈"
                    }
                    descrizione = meteodic[str(response['weather'][0]['main'])]
                    tastiera = types.InlineKeyboardMarkup()
                    bottone = types.InlineKeyboardButton(text="🗺 » Guarda su Google Maps",
                                                         url="https://www.google.com/maps/place/" + str(
                                                             response['coord']['lat']) + "," + str(
                                                             response['coord']['lon']) + "/")
                    tastiera.add(bottone)
                    bot.send_message(message.chat.id,
                                     "  🌥 Meteo <i>" + str(contenuto) + "</i> ☔️ \n🌍 descrizione: <i>" + str(
                                         descrizione) + " </i>\n🌡 Temperatura: <i>" + str(
                                         response['main']['temp']) + " °C</i> \n🤲 Temp. percepita: <i>" + str(
                                         response['main']['feels_like']) + " °C </i>\n🥵 Temp. massima: <i>" + str(
                                         response['main']['temp_max']) + " °C </i>\n🥶 Temp. minima: <i>" + str(
                                         response['main']['temp_min']) + " °C </i> \n💨 Vento: <i>" + str(
                                         response["wind"]["speed"]) + " m/s </i> \n👁‍🗨 Visibilità: <i>" + str(
                                         response['visibility']) + " m </i> \n💧Umidità: <i>" + str(
                                         response['main']['humidity']) + " % </i>\n💊 Pressione: <i>" + str(
                                         response['main']['pressure']) + " mb </i>", reply_markup=tastiera,
                                     parse_mode="html")
            except Exception as ex:
                salvaerrore(ex)


# * Bestemmie
@bot.edited_message_handler(regexp='dio', chat_types='supergroup')
@bot.edited_message_handler(regexp='DIO', chat_types='supergroup')
@bot.message_handler(regexp='dio', chat_types='supergroup')
@bot.message_handler(regexp='DIO', chat_types='supergroup')
@bot.edited_message_handler(regexp='madonna', chat_types='supergroup')
@bot.edited_message_handler(regexp='MADONNA', chat_types='supergroup')
@bot.message_handler(regexp='Madonna', chat_types='supergroup')
@bot.message_handler(regexp='MADONNA', chat_types='supergroup')
def startbestemmie(message): Thread(target=bestemmia, args=[message]).start()


def bestemmia(message):
    if chatblacklist(message.chat.id) is True:
        incrementa_decrementa_stato(message.from_user.first_name, message.from_user.id, 'bestemmie', "+")
        x = incrementa_decrementa_stato(gruppo, 1, 'bestemmie', "+")
        try_to(message, "🐖 <i>Robot ita conta </i>»<code>" + str(x) + "</code><i> bestemmie</i>")


# * top
@bot.edited_message_handler(commands=['top', 'TOP'], chat_types='supergroup')
@bot.message_handler(commands=['top', 'TOP'], chat_types='supergroup')
def starttop(message): Thread(target=top, args=[message]).start()


def top(message):
    if chatblacklist(message.chat.id) is True:
        tastiera = types.InlineKeyboardMarkup()
        succhini = types.InlineKeyboardButton(text="🧃Succhini", callback_data="top5succhini")
        rispetto = types.InlineKeyboardButton(text="🎉 Rispetto", callback_data="top5rispetto")
        tastiera.add(succhini, rispetto)
        like = types.InlineKeyboardButton(text="❤️ Like", callback_data="top5likes")
        dislike = types.InlineKeyboardButton(text="👎 Dislike", callback_data="top5dislike")
        tastiera.add(like, dislike)
        bestemmie = types.InlineKeyboardButton(text="🐷 Bestemmie", callback_data="top5bestemmie")
        tastiera.add(bestemmie)
        seno = types.InlineKeyboardButton(text="🍐 Seno", callback_data="top5seno")
        cazzo = types.InlineKeyboardButton(text="🍆 Cazzo", callback_data="top5cazzo")
        tastiera.add(seno, cazzo)
        bot.send_message(message.chat.id, "<b>🎖 »</b>" + "<i>Seleziona la categoria</i>", parse_mode="html",
                         reply_markup=tastiera)


@bot.callback_query_handler(func=lambda c: c.data == 'top5succhini')
def top5succhini(call):
    try:
        documents = dbstato.find({}).sort('succhini', -1).limit(10)
        classifica = "Top succhini 🧃\n"
        i = 0
        for document in documents:
            if str(document['name']) != str(-1001434687578):
                i = i + 1
                classifica = classifica + str(i) + ". " + str(
                    document['name'].replace('<', '').replace('>', '')) + " » <code>" + str(
                    display(document['succhini'])) + "</code>" + "\n"
        tastiera = types.InlineKeyboardMarkup()
        avanti = types.InlineKeyboardButton(text="▶️", callback_data='avantitopsucchiniuno')
        tastiera.add(avanti)
        indietro = types.InlineKeyboardButton(text="🔙 Indietro", callback_data='back')
        tastiera.add(indietro)
        bot.edit_message_text(classifica, call.message.chat.id, call.message.message_id, parse_mode="html",
                              reply_markup=tastiera)



    except:
        salvaerrore(Exception)


@bot.callback_query_handler(func=lambda c: c.data == 'avantitopsucchiniuno')
def top5succhini(call):
    global oggetto, classifica, callata, classifica
    try:
        if "Top succhini 🧃\n" in call.message.text[0:20]:
            classifica = "Top succhini 🧃\n"
            oggetto = 'succhini'
            callata = 'top5succhini'
        elif "Top rispetto 🎉\n" in call.message.text[0:20]:
            classifica = "Top rispetto 🎉\n"
            oggetto = 'rispetto'
            callata = 'top5rispetto'
        elif "Top like ❤️ \n" in call.message.text[0:20]:
            classifica = "Top like ❤️ \n"
            oggetto = 'like'
            callata = ' top5likes'
        elif "Top dislike 👎\n" in call.message.text[0:20]:
            classifica = "Top dislike 👎\n"
            oggetto = 'dislike'
            callata = 'top5dislike'
        elif "Top bestemmie 🐷\n" in call.message.text[0:20]:
            classifica = "Top bestemmie 🐷\n"
            oggetto = 'bestemmie'
            callata = 'top5bestemmie'
        elif "Top seno 🍐\n" in call.message.text[0:20]:
            classifica = "Top seno 🍐\n"
            oggetto = 'seno'
            callata = 'top5seno'
        elif "Top cazzo 🍆\n" in call.message.text[0:20]:
            classifica = "Top cazzo 🍆\n"
            oggetto = 'cazzo'
            callata = 'top5cazzo'
        documents = dbstato.find({}).sort(oggetto, -1).limit(20)
        i = 0
        for document in documents:
            if str(document['name']) != str(-1001434687578):
                i = i + 1
                if i > 10:
                    classifica = classifica + str(i) + ". " + str(
                        document['name'].replace('<', '').replace('>', '')) + " » <code>" + str(
                        display(document[oggetto])) + "</code>" + "\n"
        tastiera = types.InlineKeyboardMarkup()
        indietrodue = types.InlineKeyboardButton(text='◀️', callback_data=callata)
        avanti = types.InlineKeyboardButton(text="▶️", callback_data='avantitopsucchinidue')
        tastiera.add(indietrodue, avanti)
        indietro = types.InlineKeyboardButton(text="🔙 Indietro", callback_data='back')
        tastiera.add(indietro)
        bot.edit_message_text(classifica, call.message.chat.id, call.message.message_id, parse_mode="html",
                              reply_markup=tastiera)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'avantitopsucchinidue')
def top5succhini(call):
    try:
        start = time.perf_counter()
        if "Top succhini 🧃\n" in call.message.text[0:20]:
            classifica = "Top succhini 🧃\n"
            oggetto = 'succhini'
        elif "Top rispetto 🎉\n" in call.message.text[0:20]:
            classifica = "Top rispetto 🎉\n"
            oggetto = 'rispetto'
        elif "Top like ❤️ \n" in call.message.text[0:20]:
            classifica = "Top like ❤️ \n"
            oggetto = 'like'
        elif "Top dislike 👎\n" in call.message.text[0:20]:
            classifica = "Top dislike 👎\n"
            oggetto = 'dislike'
        elif "Top bestemmie 🐷\n" in call.message.text[0:20]:
            classifica = "Top bestemmie 🐷\n"
            oggetto = 'bestemmie'
        elif "Top seno 🍐\n" in call.message.text[0:20]:
            classifica = "Top seno 🍐\n"
            oggetto = 'seno'
        elif "Top cazzo 🍆\n" in call.message.text[0:20]:
            classifica = "Top cazzo 🍆\n"
            oggetto = 'cazzo'
        documents = dbstato.find({}).sort(oggetto, -1).limit(30)
        i = 0
        for document in documents:
            if str(document['name']) != str(-1001434687578):
                i = i + 1
                if i > 20:
                    classifica = classifica + str(i) + ". " + str(
                        document['name'].replace('<', '').replace('>', '')) + " » <code>" + str(
                        display(document[oggetto])) + "</code>" + "\n"
        tastiera = types.InlineKeyboardMarkup()
        indietrodue = types.InlineKeyboardButton(text='◀️', callback_data='avantitopsucchiniuno')
        avanti = types.InlineKeyboardButton(text="▶️", callback_data='avantitopsucchinitre')
        tastiera.add(indietrodue, avanti)
        indietro = types.InlineKeyboardButton(text="🔙 Indietro", callback_data='back')
        tastiera.add(indietro)
        bot.edit_message_text(classifica, call.message.chat.id, call.message.message_id, parse_mode="html",
                              reply_markup=tastiera)
        end = time.perf_counter()
        print(end - start)
    except:
        print(Exception)


@bot.callback_query_handler(func=lambda c: c.data == 'avantitopsucchinitre')
def top5succhini(call):
    try:
        start = time.perf_counter()
        if "Top succhini 🧃\n" in call.message.text[0:20]:
            classifica = "Top succhini 🧃\n"
            oggetto = 'succhini'
        elif "Top rispetto 🎉\n" in call.message.text[0:20]:
            classifica = "Top rispetto 🎉\n"
            oggetto = 'rispetto'
        elif "Top like ❤️ \n" in call.message.text[0:20]:
            classifica = "Top like ❤️ \n"
            oggetto = 'like'
        elif "Top dislike 👎\n" in call.message.text[0:20]:
            classifica = "Top dislike 👎\n"
            oggetto = 'dislike'
        elif "Top bestemmie 🐷\n" in call.message.text[0:20]:
            classifica = "Top bestemmie 🐷\n"
            oggetto = 'bestemmie'
        elif "Top seno 🍐\n" in call.message.text[0:20]:
            classifica = "Top seno 🍐\n"
            oggetto = 'seno'
        elif "Top cazzo 🍆\n" in call.message.text[0:20]:
            classifica = "Top cazzo 🍆\n"
            oggetto = 'cazzo'
        documents = dbstato.find({}).sort(oggetto, -1).limit(40)
        i = 0
        for document in documents:
            if str(document['name']) != str(-1001434687578):
                i = i + 1
                if i > 30:
                    classifica = classifica + str(i) + ". " + str(
                        document['name'].replace('<', '').replace('>', '')) + " » <code>" + str(
                        display(document[oggetto])) + "</code>" + "\n"
        tastiera = types.InlineKeyboardMarkup()
        indietrodue = types.InlineKeyboardButton(text='◀️', callback_data='avantitopsucchinidue')
        avanti = types.InlineKeyboardButton(text="▶️", callback_data='avantitopsucchiniquattro')
        tastiera.add(indietrodue, avanti)
        indietro = types.InlineKeyboardButton(text="🔙 Indietro", callback_data='back')
        tastiera.add(indietro)
        bot.edit_message_text(classifica, call.message.chat.id, call.message.message_id, parse_mode="html",
                              reply_markup=tastiera)
        end = time.perf_counter()
        print(end - start)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'avantitopsucchiniquattro')
def top5succhini(call):
    try:
        if "Top succhini 🧃\n" in call.message.text[0:20]:
            classifica = "Top succhini 🧃\n"
            oggetto = 'succhini'
        elif "Top rispetto 🎉\n" in call.message.text[0:20]:
            classifica = "Top rispetto 🎉\n"
            oggetto = 'rispetto'
        elif "Top like ❤️ \n" in call.message.text[0:20]:
            classifica = "Top like ❤️ \n"
            oggetto = 'like'
        elif "Top dislike 👎\n" in call.message.text[0:20]:
            classifica = "Top dislike 👎\n"
            oggetto = 'dislike'
        elif "Top bestemmie 🐷\n" in call.message.text[0:20]:
            classifica = "Top bestemmie 🐷\n"
            oggetto = 'bestemmie'
        elif "Top seno 🍐\n" in call.message.text[0:20]:
            classifica = "Top seno 🍐\n"
            oggetto = 'seno'
        elif "Top cazzo 🍆\n" in call.message.text[0:20]:
            classifica = "Top cazzo 🍆\n"
            oggetto = 'cazzo'
        documents = dbstato.find({}).sort(oggetto, -1).limit(50)
        i = 0
        for document in documents:
            if str(document['name']) != str(-1001434687578):
                i = i + 1
                if i > 40:
                    classifica = classifica + str(i) + ". " + str(
                        document['name'].replace('<', '').replace('>', '')) + " » <code>" + str(
                        display(document[oggetto])) + "</code>" + "\n"
        tastiera = types.InlineKeyboardMarkup()
        indietrodue = types.InlineKeyboardButton(text='◀️', callback_data='avantitopsucchinitre')
        tastiera.add(indietrodue)
        indietro = types.InlineKeyboardButton(text="🔙 Indietro", callback_data='back')
        tastiera.add(indietro)
        bot.edit_message_text(classifica, call.message.chat.id, call.message.message_id, parse_mode="html",
                              reply_markup=tastiera)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'top5rispetto')
def top5rispetto(call):
    try:
        documents = dbstato.find({}).sort('rispetto', -1).limit(10)
        classifica = "Top rispetto 🎉\n"
        i = 0
        for document in documents:

            if str(document['name']) != str(-1001434687578):
                i = i + 1
                classifica = classifica + str(i) + ". " + str(
                    document['name'].replace('<', '').replace('>', '')) + " » <code>" + str(
                    document['rispetto']) + "</code>" + "\n"
        tastiera = types.InlineKeyboardMarkup()
        avanti = types.InlineKeyboardButton(text="▶️", callback_data='avantitopsucchiniuno')
        tastiera.add(avanti)
        indietro = types.InlineKeyboardButton(text="🔙 Indietro", callback_data='back')
        tastiera.add(indietro)
        bot.edit_message_text(classifica, call.message.chat.id, call.message.message_id, parse_mode="html",
                              reply_markup=tastiera)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'top5likes')
def top5like(call):
    try:
        documents = dbstato.find({}).sort('like', -1).limit(10)
        classifica = "Top like ❤️ \n"
        i = 0
        for document in documents:

            if str(document['name']) != str(-1001434687578):
                i = i + 1
                classifica = classifica + str(i) + ". " + str(
                    document['name'].replace('<', '').replace('>', '')) + " » <code>" + str(
                    document['like']) + "</code>" + "\n"
        tastiera = types.InlineKeyboardMarkup()
        avanti = types.InlineKeyboardButton(text="▶️", callback_data='avantitopsucchiniuno')
        tastiera.add(avanti)
        indietro = types.InlineKeyboardButton(text="🔙 Indietro", callback_data='back')
        tastiera.add(indietro)
        bot.edit_message_text(classifica, call.message.chat.id, call.message.message_id, parse_mode="html",
                              reply_markup=tastiera)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'top5dislike')
def top5dislike(call):
    try:
        documents = dbstato.find({}).sort('dislike', -1).limit(10)
        classifica = "Top dislike 👎\n"
        i = 0
        for document in documents:

            if str(document['name']) != str(-1001434687578):
                i = i + 1
                classifica = classifica + str(i) + ". " + str(
                    document['name'].replace('<', '').replace('>', '')) + " » <code>" + str(
                    document['dislike']) + "</code>" + "\n"
        tastiera = types.InlineKeyboardMarkup()
        avanti = types.InlineKeyboardButton(text="▶️", callback_data='avantitopsucchiniuno')
        tastiera.add(avanti)
        indietro = types.InlineKeyboardButton(text="🔙 Indietro", callback_data='back')
        tastiera.add(indietro)
        bot.edit_message_text(classifica, call.message.chat.id, call.message.message_id, parse_mode="html",
                              reply_markup=tastiera)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'top5bestemmie')
def top5bestemmie(call):
    try:
        documents = dbstato.find({}).sort('bestemmie', -1).limit(10)
        classifica = "Top bestemmie 🐷\n"
        i = 0
        for document in documents:

            if str(document['name']) != str(-1001434687578):
                i = i + 1
                classifica = classifica + str(i) + ". " + str(
                    document['name'].replace('<', '').replace('>', '')) + " » <code>" + str(
                    document['bestemmie']) + "</code>" + "\n"
        tastiera = types.InlineKeyboardMarkup()
        avanti = types.InlineKeyboardButton(text="▶️", callback_data='avantitopsucchiniuno')
        tastiera.add(avanti)
        indietro = types.InlineKeyboardButton(text="🔙 Indietro", callback_data='back')
        tastiera.add(indietro)
        bot.edit_message_text(classifica, call.message.chat.id, call.message.message_id, parse_mode="html",
                              reply_markup=tastiera)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'top5seno')
def top5seno(call):
    try:
        documents = dbstato.find({}).sort('seno', -1).limit(10)
        classifica = "Top seno 🍐\n"
        i = 0
        for document in documents:

            if str(document['name']) != str(-1001434687578):
                i = i + 1
                classifica = classifica + str(i) + ". " + str(
                    document['name'].replace('<', '').replace('>', '')) + " » <code>" + str(
                    document['seno']) + "</code>" + "\n"
        tastiera = types.InlineKeyboardMarkup()
        avanti = types.InlineKeyboardButton(text="▶️", callback_data='avantitopsucchiniuno')
        tastiera.add(avanti)
        indietro = types.InlineKeyboardButton(text="🔙 Indietro", callback_data='back')
        tastiera.add(indietro)
        bot.edit_message_text(classifica, call.message.chat.id, call.message.message_id, parse_mode="html",
                              reply_markup=tastiera)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'top5cazzo')
def top5cazzo(call):
    try:
        documents = dbstato.find({}).sort('cazzo', -1).limit(10)
        classifica = "Top cazzo 🍆\n"
        i = 0
        for document in documents:

            if str(document['name']) != str(-1001434687578):
                i = i + 1
                classifica = classifica + str(i) + ". " + str(
                    document['name'].replace('<', '').replace('>', '')) + " » <code>" + str(
                    document['cazzo']) + "</code>" + "\n"
        tastiera = types.InlineKeyboardMarkup()
        avanti = types.InlineKeyboardButton(text="▶️", callback_data='avantitopsucchiniuno')
        tastiera.add(avanti)
        indietro = types.InlineKeyboardButton(text="🔙 Indietro", callback_data='back')
        tastiera.add(indietro)
        bot.edit_message_text(classifica, call.message.chat.id, call.message.message_id, parse_mode="html",
                              reply_markup=tastiera)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'back')
def back(call):
    tastiera = types.InlineKeyboardMarkup()
    succhini = types.InlineKeyboardButton(text="🧃Succhini", callback_data="top5succhini")
    rispetto = types.InlineKeyboardButton(text="🎉 Rispetto", callback_data="top5rispetto")
    tastiera.add(succhini, rispetto)
    like = types.InlineKeyboardButton(text="❤️ Like", callback_data="top5likes")
    dislike = types.InlineKeyboardButton(text="👎 Dislike", callback_data="top5dislike")
    tastiera.add(like, dislike)
    bestemmie = types.InlineKeyboardButton(text="🐷 Bestemmie", callback_data="top5bestemmie")
    tastiera.add(bestemmie)
    seno = types.InlineKeyboardButton(text="🍐 Seno", callback_data="top5seno")
    cazzo = types.InlineKeyboardButton(text="🍆 Cazzo", callback_data="top5cazzo")
    tastiera.add(seno, cazzo)
    bot.edit_message_text("<b>🎖 »</b>" + "<i>Seleziona la categoria</i>", call.message.chat.id,
                          call.message.message_id, parse_mode="html", reply_markup=tastiera)


# * Comando tex []
@bot.edited_message_handler(regexp='/text', chat_types='supergroup')
@bot.edited_message_handler(regexp='/TEXT', chat_types='supergroup')
@bot.message_handler(regexp='/text', chat_types='supergroup')
@bot.message_handler(regexp='/TEXT', chat_types='supergroup')
def startext(message): Thread(target=texto, args=[message]).start()


def texto(message):
    if chatblacklist(message.chat.id) is True:
        contenuto = verify(message, 'text')
        if contenuto == False:
            nontrovato(message, "/text [testo]")
        else:
            try:
                testo = ''
                ya = contenuto.replace('Q', '𝔔').replace('W', '𝔚').replace('E', '𝔈').replace('R', 'ℜ').replace('T',
                                                                                                               '𝔗').replace(
                    'Y', '𝔜').replace('U', '𝔘').replace('I', 'ℑ').replace('O', '𝔒').replace('P', '𝔓').replace('A',
                                                                                                              '𝔄').replace(
                    'S', '𝔖').replace('D', '𝔇').replace('F', '𝔉').replace('G', '𝔊').replace('H', 'ℌ').replace('J',
                                                                                                              '𝔍').replace(
                    'K', '𝔎').replace('L', '𝔏').replace('Z', 'ℨ').replace('X', '𝔛').replace('C', 'ℭ').replace('V',
                                                                                                              '𝔙').replace(
                    'B', '𝔅').replace('N', '𝔑').replace('M', '𝔐').replace('q', '𝔮').replace('w', '𝔴').replace('e',
                                                                                                              '𝔢').replace(
                    'r', '𝔯').replace('t', '𝔱').replace('y', '𝔶').replace('u', '𝔲').replace('i', '𝔦').replace('o',
                                                                                                              '𝔬').replace(
                    'p', '𝔭').replace('a', '𝔞').replace('s', '𝔰').replace('d', '𝔡').replace('f', '𝔣').replace('g',
                                                                                                              '𝔤').replace(
                    'h', '𝔥').replace('j', '𝔧').replace('k', '𝔨').replace('l', '𝔩').replace('z', '𝔷').replace('x',
                                                                                                              '𝔵').replace(
                    'c', '𝔠').replace('v', '𝔳').replace('b', '𝔟').replace('n', '𝔫').replace('m', '𝔪').replace('1',
                                                                                                              '1').replace(
                    '2', '2').replace('3', '3').replace('4', '4').replace('5', '5').replace('6', '6').replace('7',
                                                                                                              '7').replace(
                    '8', '8').replace('9', '9').replace('0', '0').replace('!', '!').replace('$', '$').replace('%',
                                                                                                              '%').replace(
                    '&', '&').replace('/', '/').replace('(', '(').replace(')', ')').replace('=', '=').replace('?',
                                                                                                              '?').replace(
                    '_', '_').replace('-', '-').replace('.', '.').replace(',', ',').replace('[', '[').replace(']',
                                                                                                              ']').replace(
                    '<', '<').replace('>', '>')
                yb = contenuto.replace('Q', '𝕼').replace('W', '𝖂').replace('E', '𝕰').replace('R', '𝕽').replace('T',
                                                                                                               '𝕿').replace(
                    'Y', '𝖄').replace('U', '𝖀').replace('I', '𝕴').replace('O', '𝕺').replace('P', '𝕻').replace('A',
                                                                                                              '𝕬').replace(
                    'S', '𝕾').replace('D', '𝕯').replace('F', '𝕱').replace('G', '𝕲').replace('H', '𝕳').replace('J',
                                                                                                              '𝕵').replace(
                    'K', '𝕶').replace('L', '𝕷').replace('Z', '𝖅').replace('X', '𝖃').replace('C', '𝕮').replace('V',
                                                                                                              '𝖁').replace(
                    'B', '𝕭').replace('N', '𝕹').replace('M', '𝕸').replace('q', '𝖖').replace('w', '𝖜').replace('e',
                                                                                                              '𝖊').replace(
                    'r', '𝖗').replace('t', '𝖙').replace('y', '𝖞').replace('u', '𝖚').replace('i', '𝖎').replace('o',
                                                                                                              '𝖔').replace(
                    'p', '𝖕').replace('a', '𝖆').replace('s', '𝖘').replace('d', '𝖉').replace('f', '𝖋').replace('g',
                                                                                                              '𝖌').replace(
                    'h', '𝖍').replace('j', '𝖏').replace('k', '𝖐').replace('l', '𝖑').replace('z', '𝖟').replace('x',
                                                                                                              '𝖝').replace(
                    'c', '𝖈').replace('v', '𝖛').replace('b', '𝖇').replace('n', '𝖓').replace('m', '𝖒').replace('1',
                                                                                                              '1').replace(
                    '2', '2').replace('3', '3').replace('4', '4').replace('5', '5').replace('6', '6').replace('7',
                                                                                                              '7').replace(
                    '8', '8').replace('9', '9').replace('0', '0').replace('!', '!').replace('$', '$').replace('%',
                                                                                                              '%').replace(
                    '&', '&').replace('/', '/').replace('(', '(').replace(')', ')').replace('=', '=').replace('?',
                                                                                                              '?').replace(
                    '_', '_').replace('-', '-').replace('.', '.').replace(',', ',').replace('[', '[').replace(']',
                                                                                                              ']').replace(
                    '<', '<').replace('>', '>')
                yc = contenuto.replace('Q', '𝓠').replace('W', '𝓦').replace('E', '𝓔').replace('R', '𝓡').replace('T',
                                                                                                               '𝓣').replace(
                    'Y', '𝓨').replace('U', '𝓤').replace('I', '𝓘').replace('O', '𝓞').replace('P', '𝓟').replace('A',
                                                                                                              '𝓐').replace(
                    'S', '𝓢').replace('D', '𝓓').replace('F', '𝓕').replace('G', '𝓖').replace('H', '𝓗').replace('J',
                                                                                                              '𝓙').replace(
                    'K', '𝓚').replace('L', '𝓛').replace('Z', '𝓩').replace('X', '𝓧').replace('C', '𝓒').replace('V',
                                                                                                              '𝓥').replace(
                    'B', '𝓑').replace('N', '𝓝').replace('M', '𝓜').replace('q', '𝓺').replace('w', '𝔀').replace('e',
                                                                                                              '𝓮').replace(
                    'r', '𝓻').replace('t', '𝓽').replace('y', '𝔂').replace('u', '𝓾').replace('i', '𝓲').replace('o',
                                                                                                              '𝓸').replace(
                    'p', '𝓹').replace('a', '𝓪').replace('s', '𝓼').replace('d', '𝓭').replace('f', '𝓯').replace('g',
                                                                                                              '𝓰').replace(
                    'h', '𝓱').replace('j', '𝓳').replace('k', '𝓴').replace('l', '𝓵').replace('z', '𝔃').replace('x',
                                                                                                              '𝔁').replace(
                    'c', '𝓬').replace('v', '𝓿').replace('b', '𝓫').replace('n', '𝓷').replace('m', '𝓶').replace('1',
                                                                                                              '1').replace(
                    '2', '2').replace('3', '3').replace('4', '4').replace('5', '5').replace('6', '6').replace('7',
                                                                                                              '7').replace(
                    '8', '8').replace('9', '9').replace('0', '0').replace('!', '!').replace('$', '$').replace('%',
                                                                                                              '%').replace(
                    '&', '&').replace('/', '/').replace('(', '(').replace(')', ')').replace('=', '=').replace('?',
                                                                                                              '?').replace(
                    '_', '_').replace('-', '-').replace('.', '.').replace(',', ',').replace('[', '[').replace(']',
                                                                                                              ']').replace(
                    '<', '<').replace('>', '>')
                yd = contenuto.replace('Q', '𝒬').replace('W', '𝒲').replace('E', '𝐸').replace('R', '𝑅').replace('T',
                                                                                                               '𝒯').replace(
                    'Y', '𝒴').replace('U', '𝒰').replace('I', '𝐼').replace('O', '𝒪').replace('P', '𝒫').replace('A',
                                                                                                              '𝒜').replace(
                    'S', '𝒮').replace('D', '𝒟').replace('F', '𝐹').replace('G', '𝒢').replace('H', '𝐻').replace('J',
                                                                                                              '𝒥').replace(
                    'K', '𝒦').replace('L', '𝐿').replace('Z', '𝒵').replace('X', '𝒳').replace('C', '𝒞').replace('V',
                                                                                                              '𝒱').replace(
                    'B', '𝐵').replace('N', '𝒩').replace('M', '𝑀').replace('q', '𝓆').replace('w', '𝓌').replace('e',
                                                                                                              '𝑒').replace(
                    'r', '𝓇').replace('t', '𝓉').replace('y', '𝓎').replace('u', '𝓊').replace('i', '𝒾').replace('o',
                                                                                                              '𝑜').replace(
                    'p', '𝓅').replace('a', '𝒶').replace('s', '𝓈').replace('d', '𝒹').replace('f', '𝒻').replace('g',
                                                                                                              '𝑔').replace(
                    'h', '𝒽').replace('j', '𝒿').replace('k', '𝓀').replace('l', '𝓁').replace('z', '𝓏').replace('x',
                                                                                                              '𝓍').replace(
                    'c', '𝒸').replace('v', '𝓋').replace('b', '𝒷').replace('n', '𝓃').replace('m', '𝓂').replace('1',
                                                                                                              '𝟣').replace(
                    '2', '𝟤').replace('3', '𝟥').replace('4', '𝟦').replace('5', '𝟧').replace('6', '𝟨').replace('7',
                                                                                                              '𝟩').replace(
                    '8', '𝟪').replace('9', '𝟫').replace('0', '𝟢').replace('!', '!').replace('$', '$').replace('%',
                                                                                                              '%').replace(
                    '&', '&').replace('/', '/').replace('(', '(').replace(')', ')').replace('=', '=').replace('?',
                                                                                                              '?').replace(
                    '_', '_').replace('-', '-').replace('.', '.').replace(',', ',').replace('[', '[').replace(']',
                                                                                                              ']').replace(
                    '<', '<').replace('>', '>')
                ye = contenuto.replace('Q', 'ℚ').replace('W', '𝕎').replace('E', '𝔼').replace('R', 'ℝ').replace('T',
                                                                                                               '𝕋').replace(
                    'Y', '𝕐').replace('U', '𝕌').replace('I', '𝕀').replace('O', '𝕆').replace('P', 'ℙ').replace('A',
                                                                                                              '𝔸').replace(
                    'S', '𝕊').replace('D', '𝔻').replace('F', '𝔽').replace('G', '𝔾').replace('H', 'ℍ').replace('J',
                                                                                                              '𝕁').replace(
                    'K', '𝕂').replace('L', '𝕃').replace('Z', 'ℤ').replace('X', '𝕏').replace('C', 'ℂ').replace('V',
                                                                                                              '𝕍').replace(
                    'B', '𝔹').replace('N', 'ℕ').replace('M', '𝕄').replace('q', '𝕢').replace('w', '𝕨').replace('e',
                                                                                                              '𝕖').replace(
                    'r', '𝕣').replace('t', '𝕥').replace('y', '𝕪').replace('u', '𝕦').replace('i', '𝕚').replace('o',
                                                                                                              '𝕠').replace(
                    'p', '𝕡').replace('a', '𝕒').replace('s', '𝕤').replace('d', '𝕕').replace('f', '𝕗').replace('g',
                                                                                                              '𝕘').replace(
                    'h', '𝕙').replace('j', '𝕛').replace('k', '𝕜').replace('l', '𝕝').replace('z', '𝕫').replace('x',
                                                                                                              '𝕩').replace(
                    'c', '𝕔').replace('v', '𝕧').replace('b', '𝕓').replace('n', '𝕟').replace('m', '𝕞').replace('1',
                                                                                                              '𝟙').replace(
                    '2', '𝟚').replace('3', '𝟛').replace('4', '𝟜').replace('5', '𝟝').replace('6', '𝟞').replace('7',
                                                                                                              '𝟟').replace(
                    '8', '𝟠').replace('9', '𝟡').replace('0', '𝟘').replace('!', '!').replace('$', '$').replace('%',
                                                                                                              '%').replace(
                    '&', '&').replace('/', '/').replace('(', '(').replace(')', ')').replace('=', '=').replace('?',
                                                                                                              '?').replace(
                    '_', '_').replace('-', '_').replace('.', '-').replace(',', '.').replace('[', ',').replace(']',
                                                                                                              '[').replace(
                    '<', ']').replace('>', '<')
                yf = contenuto.replace('Q', '𝙌').replace('W', '𝙒').replace('E', '𝙀').replace('R', '𝙍').replace('T',
                                                                                                               '𝙏').replace(
                    'Y', '𝙔').replace('U', '𝙐').replace('I', '𝙄').replace('O', '𝙊').replace('P', '𝙋').replace('A',
                                                                                                              '𝘼').replace(
                    'S', '𝙎').replace('D', '𝘿').replace('F', '𝙁').replace('G', '𝙂').replace('H', '𝙃').replace('J',
                                                                                                              '𝙅').replace(
                    'K', '𝙆').replace('L', '𝙇').replace('Z', '𝙕').replace('X', '𝙓').replace('C', '𝘾').replace('V',
                                                                                                              '𝙑').replace(
                    'B', '𝘽').replace('N', '𝙉').replace('M', '𝙈').replace('q', '𝙦').replace('w', '𝙬').replace('e',
                                                                                                              '𝙚').replace(
                    'r', '𝙧').replace('t', '𝙩').replace('y', '𝙮').replace('u', '𝙪').replace('i', '𝙞').replace('o',
                                                                                                              '𝙤').replace(
                    'p', '𝙥').replace('a', '𝙖').replace('s', '𝙨').replace('d', '𝙙').replace('f', '𝙛').replace('g',
                                                                                                              '𝙜').replace(
                    'h', '𝙝').replace('j', '𝙟').replace('k', '𝙠').replace('l', '𝙡').replace('z', '𝙯').replace('x',
                                                                                                              '𝙭').replace(
                    'c', '𝙘').replace('v', '𝙫').replace('b', '𝙗').replace('n', '𝙣').replace('m', '𝙢').replace('1',
                                                                                                              '1').replace(
                    '2', '2').replace('3', '3').replace('4', '4').replace('5', '5').replace('6', '6').replace('7',
                                                                                                              '7').replace(
                    '8', '8').replace('9', '9').replace('0', '0').replace('!', '!').replace('$', '$').replace('%',
                                                                                                              '%').replace(
                    '&', '&').replace('/', '/').replace('(', '(').replace(')', ')').replace('=', '=').replace('?',
                                                                                                              '?').replace(
                    '_', '_').replace('-', '-').replace('.', '.').replace(',', ',').replace('[', '[').replace(']',
                                                                                                              ']').replace(
                    '<', '<').replace('>', '>')
                yg = contenuto.replace('Q', 'Ｑ').replace('W', 'Ｗ').replace('E', 'Ｅ').replace('R', 'Ｒ').replace('T',
                                                                                                               'Ｔ').replace(
                    'Y', 'Ｙ').replace('U', 'Ｕ').replace('I', 'Ｉ').replace('O', 'Ｏ').replace('P', 'Ｐ').replace('A',
                                                                                                              'Ａ').replace(
                    'S', 'Ｓ').replace('D', 'Ｄ').replace('F', 'Ｆ').replace('G', 'Ｇ').replace('H', 'Ｈ').replace('J',
                                                                                                              'Ｊ').replace(
                    'K', 'Ｋ').replace('L', 'Ｌ').replace('Z', 'Ｚ').replace('X', 'Ｘ').replace('C', 'Ｃ').replace('V',
                                                                                                              'Ｖ').replace(
                    'B', 'Ｂ').replace('N', 'Ｎ').replace('M', 'Ｍ').replace('q', 'ｑ').replace('w', 'ｗ').replace('e',
                                                                                                              'ｅ').replace(
                    'r', 'ｒ').replace('t', 'ｔ').replace('y', 'ｙ').replace('u', 'ｕ').replace('i', 'ｉ').replace('o',
                                                                                                              'ｏ').replace(
                    'p', 'ｐ').replace('a', 'ａ').replace('s', 'ｓ').replace('d', 'ｄ').replace('f', 'ｆ').replace('g',
                                                                                                              'ｇ').replace(
                    'h', 'ｈ').replace('j', 'ｊ').replace('k', 'ｋ').replace('l', 'ｌ').replace('z', 'ｚ').replace('x',
                                                                                                              'ｘ').replace(
                    'c', 'ｃ').replace('v', 'ｖ').replace('b', 'ｂ').replace('n', 'ｎ').replace('m', 'ｍ').replace('1',
                                                                                                              '１').replace(
                    '2', '２').replace('3', '３').replace('4', '４').replace('5', '５').replace('6', '６').replace('7',
                                                                                                              '７').replace(
                    '8', '８').replace('9', '９').replace('0', '０').replace('!', '！').replace('$', '＄').replace('%',
                                                                                                              '％').replace(
                    '&', '＆').replace('/', '／').replace('(', '（').replace(')', '）').replace('=', '＝').replace('?',
                                                                                                              '？').replace(
                    '_', '＇').replace('-', '_').replace('.', '－').replace(',', '．').replace('[', '，').replace(']',
                                                                                                              '[').replace(
                    '<', ']').replace('>', '<')
                yh = contenuto.replace('Q', 'Q').replace('W', 'ᴡ').replace('E', 'ᴇ').replace('R', 'ʀ').replace('T',
                                                                                                               'ᴛ').replace(
                    'Y', 'ʏ').replace('U', 'ᴜ').replace('I', 'ɪ').replace('O', 'ᴏ').replace('P', 'ᴘ').replace('A',
                                                                                                              'ᴀ').replace(
                    'S', 'ꜱ').replace('D', 'ᴅ').replace('F', 'ꜰ').replace('G', 'ɢ').replace('H', 'ʜ').replace('J',
                                                                                                              'ᴊ').replace(
                    'K', 'ᴋ').replace('L', 'ʟ').replace('Z', 'ᴢ').replace('X', 'x').replace('C', 'ᴄ').replace('V',
                                                                                                              'ᴠ').replace(
                    'B', 'ʙ').replace('N', 'ɴ').replace('M', 'ᴍ').replace('q', 'Q').replace('w', 'ᴡ').replace('e',
                                                                                                              'ᴇ').replace(
                    'r', 'ʀ').replace('t', 'ᴛ').replace('y', 'ʏ').replace('u', 'ᴜ').replace('i', 'ɪ').replace('o',
                                                                                                              'ᴏ').replace(
                    'p', 'ᴘ').replace('a', 'ᴀ').replace('s', 'ꜱ').replace('d', 'ᴅ').replace('f', 'ꜰ').replace('g',
                                                                                                              'ɢ').replace(
                    'h', 'ʜ').replace('j', 'ᴊ').replace('k', 'ᴋ').replace('l', 'ʟ').replace('z', 'ᴢ').replace('x',
                                                                                                              'x').replace(
                    'c', 'ᴄ').replace('v', 'ᴠ').replace('b', 'ʙ').replace('n', 'ɴ').replace('m', 'ᴍ').replace('1',
                                                                                                              '1').replace(
                    '2', '2').replace('3', '3').replace('4', '4').replace('5', '5').replace('6', '6').replace('7',
                                                                                                              '7').replace(
                    '8', '8').replace('9', '9').replace('0', '0').replace('!', '!').replace('$', '$').replace('%',
                                                                                                              '%').replace(
                    '&', '&').replace('/', '/').replace('(', '(').replace(')', ')').replace('=', '=').replace('?',
                                                                                                              '?').replace(
                    '_', '_').replace('-', '_').replace('.', '-').replace(',', '.').replace('[', ',').replace(']',
                                                                                                              '[').replace(
                    '<', ']').replace('>', '<')
                yi = contenuto.replace('Q', '🅀').replace('W', '🅆').replace('E', '🄴').replace('R', '🅁').replace('T',
                                                                                                               '🅃').replace(
                    'Y', '🅈').replace('U', '🅄').replace('I', '🄸').replace('O', '🄾').replace('P', '🄿').replace('A',
                                                                                                              '🄰').replace(
                    'S', '🅂').replace('D', '🄳').replace('F', '🄵').replace('G', '🄶').replace('H', '🄷').replace('J',
                                                                                                              '🄹').replace(
                    'K', '🄺').replace('L', '🄻').replace('Z', '🅉').replace('X', '🅇').replace('C', '🄲').replace('V',
                                                                                                              '🅅').replace(
                    'B', '🄱').replace('N', '🄽').replace('M', '🄼').replace('q', '🅀').replace('w', '🅆').replace('e',
                                                                                                              '🄴').replace(
                    'r', '🅁').replace('t', '🅃').replace('y', '🅈').replace('u', '🅄').replace('i', '🄸').replace('o',
                                                                                                              '🄾').replace(
                    'p', '🄿').replace('a', '🄰').replace('s', '🅂').replace('d', '🄳').replace('f', '🄵').replace('g',
                                                                                                              '🄶').replace(
                    'h', '🄷').replace('j', '🄹').replace('k', '🄺').replace('l', '🄻').replace('z', '🅉').replace('x',
                                                                                                              '🅇').replace(
                    'c', '🄲').replace('v', '🅅').replace('b', '🄱').replace('n', '🄽').replace('m', '🄼').replace('1',
                                                                                                              '1').replace(
                    '2', '2').replace('3', '3').replace('4', '4').replace('5', '5').replace('6', '6').replace('7',
                                                                                                              '7').replace(
                    '8', '8').replace('9', '9').replace('0', '0').replace('!', '!').replace('$', '$').replace('%',
                                                                                                              '%').replace(
                    '&', '&').replace('/', '/').replace('(', '(').replace(')', ')').replace('=', '=').replace('?',
                                                                                                              '?').replace(
                    '_', '_').replace('-', '-').replace('.', '.').replace(',', ',').replace('[', '[').replace(']',
                                                                                                              ']').replace(
                    '<', '<').replace('>', '>')
                yl = contenuto.replace('Q', '🆀').replace('W', '🆆').replace('E', '🅴').replace('R', '🆁').replace('T',
                                                                                                               '🆃').replace(
                    'Y', '🆈').replace('U', '🆄').replace('I', '🅸').replace('O', '🅾').replace('P', '🅿').replace('A',
                                                                                                              '🅰').replace(
                    'S', '🆂').replace('D', '🅳').replace('F', '🅵').replace('G', '🅶').replace('H', '🅷').replace('J',
                                                                                                              '🅹').replace(
                    'K', '🅺').replace('L', '🅻').replace('Z', '🆉').replace('X', '🆇').replace('C', '🅲').replace('V',
                                                                                                              '🆅').replace(
                    'B', '🅱').replace('N', '🅽').replace('M', '🅼').replace('q', '🆀').replace('w', '🆆').replace('e',
                                                                                                              '🅴').replace(
                    'r', '🆁').replace('t', '🆃').replace('y', '🆈').replace('u', '🆄').replace('i', '🅸').replace('o',
                                                                                                              '🅾').replace(
                    'p', '🅿').replace('a', '🅰').replace('s', '🆂').replace('d', '🅳').replace('f', '🅵').replace('g',
                                                                                                              '🅶').replace(
                    'h', '🅷').replace('j', '🅹').replace('k', '🅺').replace('l', '🅻').replace('z', '🆉').replace('x',
                                                                                                              '🆇').replace(
                    'c', '🅲').replace('v', '🆅').replace('b', '🅱').replace('n', '🅽').replace('m', '🅼').replace('1',
                                                                                                              '1').replace(
                    '2', '2').replace('3', '3').replace('4', '4').replace('5', '5').replace('6', '6').replace('7',
                                                                                                              '7').replace(
                    '8', '8').replace('9', '9').replace('0', '0').replace('!', '!').replace('$', '$').replace('%',
                                                                                                              '%').replace(
                    '&', '&').replace('/', '/').replace('(', '(').replace(')', ')').replace('=', '=').replace('?',
                                                                                                              '?').replace(
                    '_', '_').replace('-', '-').replace('.', '.').replace(',', ',').replace('[', '[').replace(']',
                                                                                                              ']').replace(
                    '<', '<').replace('>', '>')
                ym = contenuto.replace('Q', 'Q').replace('W', 'ᵂ').replace('E', 'ᴱ').replace('R', 'ᴿ').replace('T',
                                                                                                               'ᵀ').replace(
                    'Y', 'ʸ').replace('U', 'ᵁ').replace('I', 'ᴵ').replace('O', 'ᴼ').replace('P', 'ᴾ').replace('A',
                                                                                                              'ᴬ').replace(
                    'S', 'ˢ').replace('D', 'ᴰ').replace('F', 'ᶠ').replace('G', 'ᴳ').replace('H', 'ᴴ').replace('J',
                                                                                                              'ᴶ').replace(
                    'K', 'ᴷ').replace('L', 'ᴸ').replace('Z', 'ᶻ').replace('X', 'ˣ').replace('C', 'ᶜ').replace('V',
                                                                                                              'ⱽ').replace(
                    'B', 'ᴮ').replace('N', 'ᴺ').replace('M', 'ᴹ').replace('q', 'q').replace('w', 'ʷ').replace('e',
                                                                                                              'ᵉ').replace(
                    'r', 'ʳ').replace('t', 'ᵗ').replace('y', 'ʸ').replace('u', 'ᵘ').replace('i', 'ⁱ').replace('o',
                                                                                                              'ᵒ').replace(
                    'p', 'ᵖ').replace('a', 'ᵃ').replace('s', 'ˢ').replace('d', 'ᵈ').replace('f', 'ᶠ').replace('g',
                                                                                                              'ᵍ').replace(
                    'h', 'ʰ').replace('j', 'ʲ').replace('k', 'ᵏ').replace('l', 'ˡ').replace('z', 'ᶻ').replace('x',
                                                                                                              'ˣ').replace(
                    'c', 'ᶜ').replace('v', 'ᵛ').replace('b', 'ᵇ').replace('n', 'ⁿ').replace('m', 'ᵐ').replace('1',
                                                                                                              '¹').replace(
                    '2', '²').replace('3', '³').replace('4', '⁴').replace('5', '⁵').replace('6', '⁶').replace('7',
                                                                                                              '⁷').replace(
                    '8', '⁸').replace('9', '⁹').replace('0', '⁰').replace('!', '!').replace('$', '$').replace('%',
                                                                                                              '%').replace(
                    '&', '&').replace('/', '/').replace('(', '⁽').replace(')', '⁾').replace('=', '⁼').replace('?',
                                                                                                              '?').replace(
                    '_', '_').replace('-', '⁻').replace('.', '.').replace(',', ',').replace('[', '[').replace(']',
                                                                                                              ']').replace(
                    '<', '<').replace('>', '>')
                yn = contenuto.replace('Q', 'Ⓠ').replace('W', 'Ⓦ').replace('E', 'Ⓔ').replace('R', 'Ⓡ').replace('T',
                                                                                                               'Ⓣ').replace(
                    'Y', 'Ⓨ').replace('U', 'Ⓤ').replace('I', 'Ⓘ').replace('O', 'Ⓞ').replace('P', 'Ⓟ').replace('A',
                                                                                                              'Ⓐ').replace(
                    'S', 'Ⓢ').replace('D', 'Ⓓ').replace('F', 'Ⓕ').replace('G', 'Ⓖ').replace('H', 'Ⓗ').replace('J',
                                                                                                              'Ⓙ').replace(
                    'K', 'Ⓚ').replace('L', 'Ⓛ').replace('Z', 'Ⓩ').replace('X', 'Ⓧ').replace('C', 'Ⓒ').replace('V',
                                                                                                              'Ⓥ').replace(
                    'B', 'Ⓑ').replace('N', 'Ⓝ').replace('M', 'Ⓜ').replace('q', 'ⓠ').replace('w', 'ⓦ').replace('e',
                                                                                                              'ⓔ').replace(
                    'r', 'ⓡ').replace('t', 'ⓣ').replace('y', 'ⓨ').replace('u', 'ⓤ').replace('i', 'ⓘ').replace('o',
                                                                                                              'ⓞ').replace(
                    'p', 'ⓟ').replace('a', 'ⓐ').replace('s', 'ⓢ').replace('d', 'ⓓ').replace('f', 'ⓕ').replace('g',
                                                                                                              'ⓖ').replace(
                    'h', 'ⓗ').replace('j', 'ⓙ').replace('k', 'ⓚ').replace('l', 'ⓛ').replace('z', 'ⓩ').replace('x',
                                                                                                              'ⓧ').replace(
                    'c', 'ⓒ').replace('v', 'ⓥ').replace('b', 'ⓑ').replace('n', 'ⓝ').replace('m', 'ⓜ').replace('1',
                                                                                                              '①').replace(
                    '2', '②').replace('3', '③').replace('4', '④').replace('5', '⑤').replace('6', '⑥').replace('7',
                                                                                                              '⑦').replace(
                    '8', '⑧').replace('9', '⑨').replace('0', '⓪').replace('!', '!').replace('$', '$').replace('%',
                                                                                                              '%').replace(
                    '&', '&').replace('/', '/').replace('(', '(').replace(')', ')').replace('=', '=').replace('?',
                                                                                                              '?').replace(
                    '_', '_').replace('-', '-').replace('.', '.').replace(',', ',').replace('[', '[').replace(']',
                                                                                                              ']').replace(
                    '<', '<').replace('>', '>')
                yp = contenuto.replace('Q', '𝐐').replace('W', '𝐖').replace('E', '𝐄').replace('R', '𝐑').replace('T',

                                                                                                               '𝐓').replace(
                    'Y', '𝐘').replace('U', '𝐔').replace('I', '𝐈').replace('O', '𝐎').replace('P', '𝐏').replace('A',
                                                                                                              '𝐀').replace(
                    'S', '𝐒').replace('D', '𝐃').replace('F', '𝐅').replace('G', '𝐆').replace('H', '𝐇').replace('J',
                                                                                                              '𝐉').replace(
                    'K', '𝐊').replace('L', '𝐋').replace('Z', '𝐙').replace('X', '𝐗').replace('C', '𝐂').replace('V',
                                                                                                              '𝐕').replace(
                    'B', '𝐁').replace('N', '𝐍').replace('M', '𝐌').replace('q', '𝐪').replace('w', '𝐰').replace('e',
                                                                                                              '𝐞').replace(
                    'r', '𝐫').replace('t', '𝐭').replace('y', '𝐲').replace('u', '𝐮').replace('i', '𝐢').replace('o',
                                                                                                              '𝐨').replace(
                    'p', '𝐩').replace('a', '𝐚').replace('s', '𝐬').replace('d', '𝐝').replace('f', '𝐟').replace('g',
                                                                                                              '𝐠').replace(
                    'h', '𝐡').replace('j', '𝐣').replace('k', '𝐤').replace('l', '𝐥').replace('z', '𝐳').replace('x',
                                                                                                              '𝐱').replace(
                    'c', '𝐜').replace('v', '𝐯').replace('b', '𝐛').replace('n', '𝐧').replace('m', '𝐦').replace('1',
                                                                                                              '𝟏').replace(
                    '2', '𝟐').replace('3', '𝟑').replace('4', '𝟒').replace('5', '𝟓').replace('6', '𝟔').replace('7',
                                                                                                              '𝟕').replace(
                    '8', '𝟖').replace('9', '𝟗').replace('0', '𝟎').replace('!', '!').replace('$', '$').replace('%',
                                                                                                              '%').replace(
                    '&', '&').replace('/', '/').replace('(', '(').replace(')', ')').replace('=', '=').replace('?',
                                                                                                              '?').replace(
                    '_', '_').replace('-', '-').replace('.', '.').replace(',', ',').replace('[', '[').replace(']',
                                                                                                              ']').replace(
                    '<', '<').replace('>', '>')
                yq = contenuto.replace('Q', '㔿').replace('W', '山').replace('E', '乇').replace('R', '尺').replace('T',
                                                                                                                   '丅').replace(
                    'Y', '丫').replace('U', '凵').replace('I', '工').replace('O', '口').replace('P', '尸').replace('A',
                                                                                                                   '卂').replace(
                    'S', '丂').replace('D', '刀').replace('F', '下').replace('G', '厶').replace('H', '卄').replace('J',
                                                                                                                   '丁').replace(
                    'K', '长').replace('L', '乚').replace('Z', '乙').replace('X', '乂').replace('C', '匚').replace('V',
                                                                                                                   'リ').replace(
                    'B', '乃').replace('N', '𠘨').replace('M', '从').replace('q', '㔿').replace('w', '山').replace('e',
                                                                                                                  '乇').replace(
                    'r', '尺').replace('t', '丅').replace('y', '丫').replace('u', '凵').replace('o', '口').replace('p',
                                                                                                                   '尸').replace(
                    'a', '卂').replace('s', '丂').replace('d', '刀').replace('f', '下').replace('g', '厶').replace('h',
                                                                                                                   '卄').replace(
                    'j', '丁').replace('k', '长').replace('l', '乚').replace('z', '乙').replace('x', '乂').replace('c',
                                                                                                                   '匚').replace(
                    'v', 'リ').replace('b', '乃').replace('n', '𠘨').replace('m', '从').replace('1', '1').replace('2',
                                                                                                                '2').replace(
                    '3', '3').replace('4', '4').replace('5', '5').replace('6', '6').replace('7', '7').replace('8',
                                                                                                              '8').replace(
                    '9', '9').replace('0', '0').replace('!', '!').replace('$', '$').replace('&', '&').replace('/',
                                                                                                              '/').replace(
                    '(', '(').replace(')', ')').replace('=', '=').replace('?', '?').replace('_', '_').replace('-',
                                                                                                              '-').replace(
                    '.', '.').replace(',', ',').replace('[', '[').replace(']', ']').replace('<', '<').replace('>', '>')
                ga = contenuto.replace('Q', '𝑸').replace('W', '𝑾').replace('E', '𝑬').replace('R', '𝑹').replace('T',
                                                                                                               '𝑻').replace(
                    'Y', '𝒀').replace('U', '𝑼').replace('I', '𝑰').replace('O', '𝑶').replace('P', '𝑷').replace('A',
                                                                                                              '𝑨').replace(
                    'S', '𝑺').replace('D', '𝑫').replace('F', '𝑭').replace('G', '𝑮').replace('H', '𝑯').replace('J',
                                                                                                              '𝑱').replace(
                    'K', '𝑲').replace('L', '𝑳').replace('Z', '𝒁').replace('X', '𝑿').replace('C', '𝑪').replace('V',
                                                                                                              '𝑽').replace(
                    'B', '𝑩').replace('N', '𝑵').replace('M', '𝑴').replace('q', '𝒒').replace('w', '𝒘').replace('e',
                                                                                                              '𝒆').replace(
                    'r', '𝒓').replace('t', '𝒕').replace('y', '𝒚').replace('u', '𝒖').replace('o', '𝒐').replace('p',
                                                                                                              '𝒑').replace(
                    'a', '𝒂').replace('s', '𝒔').replace('d', '𝒅').replace('f', '𝒇').replace('g', '𝒈').replace('h',
                                                                                                              '𝒉').replace(
                    'j', '𝒋').replace('k', '𝒌').replace('l', '𝒍').replace('z', '𝒛').replace('x', '𝒙').replace('c',
                                                                                                              '𝒄').replace(
                    'v', '𝒗').replace('b', '𝒃').replace('n', '𝒏').replace('m', '𝒎').replace('1', '𝟏').replace('2',
                                                                                                              '𝟐').replace(
                    '3', '𝟑').replace('4', '𝟒').replace('5', '𝟓').replace('6', '𝟔').replace('7', '𝟕').replace('8',
                                                                                                              '𝟖').replace(
                    '9', '𝟗').replace('0', '𝟎').replace('!', '!').replace('$', '$').replace('&', '&').replace('/',
                                                                                                              '/').replace(
                    '(', '(').replace(')', ')').replace('=', '=').replace('?', '?').replace('_', '_').replace('-',
                                                                                                              '-').replace(
                    '.', '.').replace(',', ',').replace('[', '[').replace(']', ']').replace('<', '<').replace('>', '>')

                fonts = [ya, yb, yc, yd, ye, yf, yg, yh, yi, yl, ym, yn, yp, yq, ga]
                for x in range(0, len(fonts)):
                    testo = testo + fonts[x] + '\n'
                try_to_two(message, testo)
            except Exception as ex:
                salvaerrore(ex)


# * Nuovo utente
@bot.message_handler(content_types=["new_chat_members"])
def startnuovoutente(message): Thread(target=nuovoutente, args=[message]).start()


def nuovoutente(message):
    if chatblacklist(message.chat.id) is True:
        entrateone = incrementa_decrementa_stato(message.from_user.first_name, message.from_user.id, 'entrate', '+')
        if int(entrateone) > 1: bot.send_message(canale_log, "#UTENTEANCORAENTRATO \n• <b>Di: </b>" + namechanger(
            message.from_user.first_name, message.from_user.id) + "\n• <b>Entrate: </b><code>" + str(
            entrateone) + "</code>", parse_mode="html")


# * Link accettazione
@bot.chat_join_request_handler()
def startaccettazione(message: telebot.types.ChatJoinRequest): Thread(target=accettazione, args=[message]).start()


def accettazione(message):
    try:
        bot.send_video(message.from_user.id, open('sending.mp4', 'rb'),
                       caption='𝙍𝙞𝙘𝙝𝙞𝙚𝙨𝙩𝙖 𝙖 𝙂𝙧𝙪𝙥𝙥𝙤 𝙞𝙩𝙖 𝙞𝙣𝙫𝙞𝙖𝙩𝙖 📫\n\n❌ 𝐍𝐨 𝐝𝐜 𝟏 (𝐕𝐨𝐈𝐏)\n\n⏳ 𝐒𝐞 𝐧𝐨𝐧 𝐡𝐚𝐢 𝐥𝐚 𝐩𝐢𝐜 𝐝𝐞𝐯𝐢 𝐚𝐭𝐭𝐞𝐧𝐝𝐞𝐫𝐞 𝐚𝐜𝐜𝐞𝐭𝐭𝐚𝐳𝐢𝐨𝐧𝐞 𝐝𝐚𝐠𝐥𝐢 𝐚𝐝𝐦𝐢𝐧',
                       parse_mode='html')

        if int(bot.get_user_profile_photos(message.from_user.id).total_count > 0):
            bot.approve_chat_join_request(gruppo, message.from_user.id)
            bot.send_message(canale_log,
                             "#UTENTECERCADIENTRARE \n <b>•Di: </b>" + namechanger(message.from_user.first_name,
                                                                                   message.from_user.id) + " [<code>" + str(
                                 message.from_user.id) + "</code>]" + "\n <i>Utente approvato automaticamente 🤖</i>",
                             parse_mode='html')
            tastiera = types.InlineKeyboardMarkup()
            regole = types.InlineKeyboardButton(text='Regole 🚔', callback_data='regole')
            tastiera.add(regole)
            canale = types.InlineKeyboardButton(text='Canale 🧸', url='https://t.me/canale_gruppoita')
            inno = types.InlineKeyboardButton(text=' Inno 🎸', url='https://t.me/canale_gruppoita/388')
            tastiera.add(canale, inno)
            chatta = types.InlineKeyboardButton(text='Inizia a chattare 💬', url='https://t.me/+8wk5E8JndRM4N2Ux')
            tastiera.add(chatta)
            bot.send_photo(message.from_user.id, 'https://telegra.ph/file/7b9242b74ff493f7ceecf.jpg',
                           caption=namechanger(message.from_user.first_name,
                                               message.from_user.id) + " <i>Benvenuto su Gruppo ita comportati bene 😊</i>",
                           reply_markup=tastiera, parse_mode='html')
            bot.send_message(gruppo, "<i>Date il benvenuto a </i> " + str(
                namechanger(message.from_user.first_name, message.from_user.id)) + " 🥳\n<i>è il " + str(
                bot.get_chat_member_count(gruppo)) + "° membro del gruppo</i>", parse_mode='html')

            # https://telegra.ph/file/7b9242b74ff493f7ceecf.jpg
        else:
            bot.send_video(message.from_user.id, open('nopic.mp4', 'rb'),
                           caption="𝙉𝙤𝙣 𝙝𝙖𝙞 𝙪𝙣𝙖 𝙛𝙤𝙩𝙤 𝙥𝙧𝙤𝙛𝙞𝙡𝙤 !\n\n🕔 𝐀𝐭𝐭𝐞𝐧𝐝𝐢 𝐜𝐡𝐞 𝐠𝐥𝐢 𝐚𝐝𝐦𝐢𝐧 𝐭𝐢 𝐚𝐜𝐜𝐞𝐭𝐭𝐢𝐧𝐨 \n\n✅🔒  𝐏𝐞𝐫𝐦𝐞𝐭𝐭𝐢 𝐚𝐥 𝐛𝐨𝐭 𝐝𝐢 𝐯𝐢𝐬𝐮𝐚𝐥𝐢𝐳𝐳𝐚𝐫𝐞 𝐥𝐚 𝐟𝐨𝐭𝐨 𝐩𝐫𝐨𝐟𝐢𝐥𝐨 𝐬𝐮𝐥𝐥𝐞 𝐢𝐦𝐩𝐨𝐬𝐭𝐚𝐳𝐢𝐨𝐧𝐢 𝐩𝐫𝐢𝐯𝐚𝐜𝐲 \n\n🔄 𝐌𝐞𝐭𝐭𝐢 𝐮𝐧𝐚 𝐟𝐨𝐭𝐨 𝐩𝐫𝐨𝐟𝐢𝐥𝐨 𝐞 𝐫𝐢𝐦𝐚𝐧𝐝𝐚 𝐥𝐚 𝐫𝐢𝐜𝐡𝐢𝐞𝐬𝐭𝐚 \n\n🗑 𝐔𝐧𝐚 𝐯𝐨𝐥𝐭𝐚 𝐩𝐚𝐬𝐬𝐚𝐭𝐢 𝐢 𝐜𝐨𝐧𝐭𝐫𝐨𝐥𝐥𝐢 𝐩𝐨𝐭𝐫𝐚𝐢 𝐭𝐨𝐠𝐥𝐢𝐞𝐫𝐞 𝐥𝐚 𝐟𝐨𝐭𝐨 𝐩𝐫𝐨𝐟𝐢𝐥𝐨",
                           parse_mode="html")
            tastiera = types.InlineKeyboardMarkup()
            accetta = types.InlineKeyboardButton(text='Accetta ✅', callback_data='accettazione')
            rifiuta = types.InlineKeyboardButton(text='Rifiuta ❌', callback_data='rifiuto')
            tastiera.add(accetta, rifiuta)
            x = bot.send_message(canale_log,
                                 "#UTENTECERCADIENTRARE \n <b>•Di: </b>" + namechanger(message.from_user.first_name,
                                                                                       message.from_user.id) + " [<code>" + str(
                                     message.from_user.id) + "</code>]", reply_markup=tastiera, parse_mode='html')
            y = bot.send_message(gruppo, namechanger(message.from_user.first_name,
                                                     message.from_user.id) + " 𝐜𝐞𝐫𝐜𝐚 𝐝𝐢 𝐞𝐧𝐭𝐫𝐚𝐫𝐞 🚪", parse_mode="html",
                                 reply_markup=tastiera)
            dbinfo.insert_one({'argomento': 'accettazione', 'message': x.message_id, 'chat': canale_log,
                               'utente': message.from_user.id, 'nome': message.from_user.first_name,
                               'groupmsg': y.message_id})
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'regole')
def regolamento(call):
    try:
        tastiera = types.InlineKeyboardMarkup()
        full = types.InlineKeyboardButton(text='Leggi di più 🎓', url='https://telegra.ph/Regole-del-gruppo-10-07')
        tastiera.add(full)
        indietro = types.InlineKeyboardButton(text='Indietro 🔙', callback_data='backbenvenuto')
        tastiera.add(indietro)
        bot.edit_message_caption(
            "📜 𝗥𝗲𝗴𝗼𝗹𝗲 :<i> \n\n🔞 No porno\n🧟‍♂️ No gore\n📩 No spam\n🔒 No privati senza consenso</i>",
            call.message.chat.id, call.message.message_id, parse_mode="html", reply_markup=tastiera)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'rugole')
def rugolamento(call):
    try:
        tastiera = types.InlineKeyboardMarkup()
        full = types.InlineKeyboardButton(text='Leggi di più 🎓', url='https://telegra.ph/Regole-del-gruppo-10-07')
        tastiera.add(full)
        indietro = types.InlineKeyboardButton(text='Indietro 🔙', callback_data='indietro')
        tastiera.add(indietro)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="📜 𝗥𝗲𝗴𝗼𝗹𝗲 :<i> \n\n🔞 No porno\n🧟‍♂️ No gore\n📩 No spam\n🔒 No privati senza consenso</i>",
                              message_id=call.message.message_id, parse_mode="html", reply_markup=tastiera)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'indietro')
def indietroz(call):
    try:
        eliminaspoiler(call.from_user.id)
        x = bot.get_chat_member(gruppo, call.from_user.id)
        if x.status == 'member' or x.status == 'administrator':
            tastiera = types.InlineKeyboardMarkup()
            spoilera = types.InlineKeyboardButton(text="Spoiler 🔒", callback_data="spoiler")
            regole = types.InlineKeyboardButton(text='Regole 📏', callback_data='rugole')
            if cercaoperatoredaidcall(call.from_user.id) != None:
                quiz = types.InlineKeyboardButton(text='Aggiungi quiz 🧠', callback_data='aggiungiquiz')
                tastiera.add(quiz,
                             spoilera)
                tastiera.add(regole)
            else:
                tastiera.add(spoilera, regole)
            bot.edit_message_text(chat_id=call.message.chat.id, text="👋 » <i>" + namechanger(call.from_user.first_name,
                                                                                             call.from_user.id) + " grazie per avermi avviato!</i>",
                                  message_id=call.message.message_id, parse_mode="html", reply_markup=tastiera)
        else:
            bot.send_message(chat_id=call.message.chat.id, text="👋 » <i>" + namechanger(call.from_user.first_name,
                                                                                        call.from_user.id) + " grazie per avermi avviato!</i>",
                             message_id=call.message.message_id, parse_mode="html")
    except Exception as ex:
        salvaerrore(ex)
        print(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'backbenvenuto')
def backbenvenuto(call):
    tastiera = types.InlineKeyboardMarkup()
    regole = types.InlineKeyboardButton(text='Regole 🚔', callback_data='regole')
    tastiera.add(regole)
    canale = types.InlineKeyboardButton(text='Canale 🧸', url='https://t.me/canale_gruppoita')
    inno = types.InlineKeyboardButton(text=' Inno 🎸', url='https://t.me/canale_gruppoita/388')
    tastiera.add(canale, inno)
    chatta = types.InlineKeyboardButton(text='Inizia a chattare 💬', url='https://t.me/+8wk5E8JndRM4N2Ux')
    tastiera.add(chatta)
    bot.edit_message_caption(namechanger(call.from_user.first_name,
                                         call.from_user.id) + " <i>Benvenuto su Gruppo ita comportati bene 😊</i>",
                             call.message.chat.id, call.message.message_id, reply_markup=tastiera, parse_mode='html')


@bot.callback_query_handler(func=lambda c: c.data == 'accettazione')
def accetto(call):
    try:
        if bot.get_chat_member(gruppo, call.from_user.id).status == 'administrator':
            trova = dbinfo.find_one(
                {'argomento': 'accettazione', 'message': call.message.message_id, 'chat': call.message.chat.id})
            group = dbinfo.find_one({'argomento': 'accettazione', 'groupmsg': call.message.message_id})
            if trova is not None:
                bot.approve_chat_join_request(gruppo, trova['utente'])
                bot.answer_callback_query(call.id, "✅ » utente approvato", show_alert=True)
                bot.edit_message_text(
                    call.message.text + "\n\n✅ » 𝐮𝐭𝐞𝐧𝐭𝐞 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐭𝐨 𝐝𝐚 " + namechanger(call.from_user.first_name,
                                                                                     call.from_user.id),
                    gruppo, trova['groupmsg'], parse_mode="html")
                bot.edit_message_text(
                    call.message.text + "\n\n ✅ » 𝐮𝐭𝐞𝐧𝐭𝐞 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐭𝐨 𝐝𝐚 " + namechanger(call.from_user.first_name,
                                                                                      call.from_user.id),
                    canale_log, trova['message'], parse_mode="html")
                tastiera = types.InlineKeyboardMarkup()
                regole = types.InlineKeyboardButton(text='Regole 🚔', callback_data='regole')
                tastiera.add(regole)
                canale = types.InlineKeyboardButton(text='Canale 🧸', url='https://t.me/canale_gruppoita')
                inno = types.InlineKeyboardButton(text=' Inno 🎸', url='https://t.me/canale_gruppoita/388')
                tastiera.add(canale, inno)
                chatta = types.InlineKeyboardButton(text='Inizia a chattare 💬', url='https://t.me/+8wk5E8JndRM4N2Ux')
                tastiera.add(chatta)
                bot.send_message(gruppo, "<i>Date il benvenuto a </i> " + str(
                    namechanger(trova['nome'], trova['utente'])) + " 🥳\n<i>è il " + str(
                    bot.get_chat_member_count(gruppo)) + "° membro del gruppo</i>", parse_mode='html')
                bot.send_photo(trova['utente'], 'https://telegra.ph/file/7b9242b74ff493f7ceecf.jpg',
                               caption=" <i>Benvenuto su Gruppo ita comportati bene 😊</i>", reply_markup=tastiera,
                               parse_mode='html')
                dbinfo.delete_many({'argomento': 'accettazione', 'utente': trova['utente']})
            elif group is not None:
                bot.approve_chat_join_request(gruppo, group['utente'])
                bot.answer_callback_query(call.id, "✅ » utente approvato", show_alert=True)
                bot.edit_message_text(
                    call.message.text + "\n\n ✅ » 𝐮𝐭𝐞𝐧𝐭𝐞 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐭𝐨 𝐝𝐚 " + namechanger(call.from_user.first_name,
                                                                                      call.from_user.id),
                    gruppo, group['groupmsg'], parse_mode="html")
                bot.edit_message_text(
                    call.message.text + "\n\n ✅ » 𝐮𝐭𝐞𝐧𝐭𝐞 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐭𝐨 𝐝𝐚 " + namechanger(call.from_user.first_name,
                                                                                      call.from_user.id),
                    canale_log, group['message'], parse_mode="html")
                tastiera = types.InlineKeyboardMarkup()
                regole = types.InlineKeyboardButton(text='Regole 🚔', callback_data='regole')
                tastiera.add(regole)
                canale = types.InlineKeyboardButton(text='Canale 🧸', url='https://t.me/canale_gruppoita')
                inno = types.InlineKeyboardButton(text=' Inno 🎸', url='https://t.me/canale_gruppoita/388')
                tastiera.add(canale, inno)
                chatta = types.InlineKeyboardButton(text='Inizia a chattare 💬', url='https://t.me/+8wk5E8JndRM4N2Ux')
                tastiera.add(chatta)
                bot.send_message(gruppo, "<i>Date il benvenuto a </i> " + str(
                    namechanger(group['nome'], group['utente'])) + " 🥳\n<i>è il " + str(
                    bot.get_chat_member_count(gruppo)) + "° membro del gruppo</i>", parse_mode='html')
                bot.send_photo(group['utente'], 'https://telegra.ph/file/7b9242b74ff493f7ceecf.jpg',
                               caption=" <i>Benvenuto su Gruppo ita comportati bene 😊</i>", reply_markup=tastiera,
                               parse_mode='html')
                dbinfo.delete_many({'argomento': 'accettazione', 'utente': trova['utente']})
            else:
                bot.answer_callback_query(call.id, "👥 » utente non trovato", show_alert=True)

        else:
            bot.answer_callback_query(call.id, "👮 » Devi essere admin per svolgere questa azione", show_alert=True)


    except Exception as ex:
        salvaerrore(ex)
        bot.answer_callback_query(call.id, "👥 » utente non trovato", show_alert=True)
        print(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'rifiuto')
def inaccettazione(call):
    try:
        if bot.get_chat_member(gruppo, call.from_user.id).status == 'administrator':
            trova = dbinfo.find_one(
                {'argomento': 'accettazione', 'message': call.message.message_id, 'chat': call.message.chat.id})
            group = dbinfo.find_one({'argomento': 'accettazione', 'groupmsg': call.message.message_id})
            if trova is not None:
                bot.decline_chat_join_request(gruppo, trova['utente'])
                bot.answer_callback_query(call.id, "❌ » utente non approvato", show_alert=True)
                bot.edit_message_text(
                    call.message.text + "\n\n❌ » 𝐮𝐭𝐞𝐧𝐭𝐞 𝐧𝐨𝐧 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐭𝐨 𝐝𝐚  " + namechanger(call.from_user.first_name,
                                                                                          call.from_user.id),
                    gruppo, trova['groupmsg'], parse_mode="html")
                bot.edit_message_text(
                    call.message.text + "\n\n ❌ » 𝐮𝐭𝐞𝐧𝐭𝐞 𝐧𝐨𝐧 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐭𝐨 𝐝𝐚 " + namechanger(call.from_user.first_name,
                                                                                          call.from_user.id),
                    canale_log, trova['message'], parse_mode="html")
                bot.send_video(trova['utente'], open('decline.mp4', 'rb'),
                               caption="<b>Non sei stato approvato su Gruppo ita ❌</b>", parse_mode='html')
                dbinfo.delete_many({'argomento': 'accettazione', 'utente': trova['utente']})
            elif group is not None:
                bot.decline_chat_join_request(gruppo, group['utente'])
                bot.answer_callback_query(call.id, "❌ » utente non approvato", show_alert=True)
                bot.edit_message_text(
                    call.message.text + "\n\n❌ » 𝐮𝐭𝐞𝐧𝐭𝐞 𝐧𝐨𝐧 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐭𝐨 𝐝𝐚  " + namechanger(call.from_user.first_name,
                                                                                          call.from_user.id),
                    gruppo, group['groupmsg'], parse_mode="html")
                bot.edit_message_text(
                    call.message.text + "\n\n ❌ » 𝐮𝐭𝐞𝐧𝐭𝐞 𝐧𝐨𝐧 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐭𝐨 𝐝𝐚 " + namechanger(call.from_user.first_name,
                                                                                          call.from_user.id),
                    canale_log, group['message'], parse_mode="html")
                bot.send_video(group['utente'], open('decline.mp4', 'rb'),
                               caption="<b>𝐍𝐨𝐧 𝐬𝐞𝐢 𝐬𝐭𝐚𝐭𝐨 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐭𝐨 ❌</b>", parse_mode='html')
                dbinfo.delete_many({'argomento': 'accettazione', 'utente': group['utente']})
            else:
                bot.answer_callback_query(call.id, "👥 » utente non trovato", show_alert=True)

        else:
            bot.answer_callback_query(call.id, "👮 » Devi essere admin per svolgere questa azione", show_alert=True)

    except Exception as ex:
        salvaerrore(ex)
        bot.answer_callback_query(call.id, "👥 » utente non trovato", show_alert=True)
        print(ex)


# ! Avvio del bot in privato
# * Elimina actspoiler
def eliminaspoiler(id):
    trova = dbinfo.find({'argomento': 'act_spoiler', 'di': id})
    if trova != None: dbinfo.delete_many({'argomento': 'act_spoiler', 'di': id})
    cerca = dbinfo.find({'argomento': 'addtraccia', 'di': id})
    if cerca != None: dbinfo.delete_many({'argomento': 'addtraccia', 'di': id})


@bot.message_handler(commands=['pr'], chat_types='private')
def prova(message):
    print('prova')


@bot.edited_message_handler(commands=['start', 'START'], chat_types='private')
@bot.message_handler(commands=['start', 'START'], chat_types='private')
def startstart(message): Thread(target=startpvt, args=[message]).start()


def startpvt(message):
    try:
        eliminaspoiler(message.from_user.id)
        x = bot.get_chat_member(gruppo, message.from_user.id)
        if x.status == 'member' or x.status == 'administrator':
            tastiera = types.InlineKeyboardMarkup()
            spoilera = types.InlineKeyboardButton(text="Spoiler 🔒", callback_data="spoiler")
            regole = types.InlineKeyboardButton(text='Regole 📏', callback_data='rugole')
            if cercaoperatoredaid(message) != None:
                quiz = types.InlineKeyboardButton(text='Aggiungi quiz 🧠', callback_data='aggiungiquiz')
                tastiera.add(quiz,
                             spoilera)
                tastiera.add(regole)

            else:
                tastiera.add(spoilera, regole)

            bot.send_message(message.chat.id, "👋 » <i>" + namechanger(message.from_user.first_name,
                                                                      message.from_user.id) + " grazie per avermi avviato!</i>",
                             parse_mode="html", reply_markup=tastiera)
        else:
            bot.send_message(message.chat.id, "👋 » <i>" + namechanger(message.from_user.first_name,
                                                                      message.from_user.id) + " grazie per avermi avviato!</i>",
                             parse_mode="html")
    except Exception as ex:
        salvaerrore(ex)
        print(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'aggiungiquiz')
def aggiungiquiz(call):
    tastiera = types.InlineKeyboardMarkup()
    indietro = types.InlineKeyboardButton(text="🔙 Indietro", callback_data="indietro")
    tastiera.add(indietro)
    try:
        msg = bot.send_message(call.message.chat.id, '❓ <i>Invia la traccia </i> ', reply_markup=tastiera,
                               parse_mode='html')
        if dbinfo.find({'argomento': 'addtraccia', "di": call.from_user.id}) != None:  dbinfo.delete_many(
            {'argomento': 'addtraccia', "di": call.from_user.id})
        dbinfo.insert_one({'argomento': 'addtraccia', "di": call.from_user.id, "step": 1})
    except Exception as ex:
        salvaerrore(ex)
        print(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'primarisp')
@bot.callback_query_handler(func=lambda c: c.data == 'secondarisp')
@bot.callback_query_handler(func=lambda c: c.data == 'terzarisp')
def corretta(call):
    try:
        if call.data == 'primarisp':
            if dbinfo.find_one({'argomento': 'addtraccia', "di": call.from_user.id}) != None:
                dbinfo.find_one_and_update({'argomento': 'addtraccia', "di": call.from_user.id},
                                           {"$set": {'corretta': 'a'}}, upsert=True)
        if call.data == 'secondarisp':
            if dbinfo.find_one({'argomento': 'addtraccia', "di": call.from_user.id}) != None:
                dbinfo.find_one_and_update({'argomento': 'addtraccia', "di": call.from_user.id},
                                           {"$set": {'corretta': 'b'}}, upsert=True)
        if call.data == 'terzarisp':
            if dbinfo.find_one({'argomento': 'addtraccia', "di": call.from_user.id}) != None:
                dbinfo.find_one_and_update({'argomento': 'addtraccia', "di": call.from_user.id},
                                           {"$set": {'corretta': 'c'}}, upsert=True)
        trova = dbinfo.find_one({'argomento': 'addtraccia', "di": call.from_user.id})
        nquiz = dbinfo.find_one({'trova': 1})
        ricerca = dbinfo.find_one({'argomento': 'cancellato'})
        if ricerca != None:
            dbinfo.delete_many({'id': ricerca['id']})
            iddi = ricerca['id']
        else:
            n = dbinfo.find_one({'trova': 1})
            dbinfo.find_one_and_update({'trova': 1}, {"$set": {'nquiz': n['nquiz'] + 1}}, upsert=True)
            iddi = nquiz['nquiz'] + 1
        dbquiz.insert_one({'traccia': trova['traccia'], 'a': trova['a'], 'b': trova['b'], 'c': trova['c'],
                           'corretta': trova['corretta'], 'id': iddi})

        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
            bot.send_message(call.from_user.id, '🧠 » <i>quiz aggiunto correttamente</i>', parse_mode='html')
            tastiera = types.InlineKeyboardMarkup()
            cancella = types.InlineKeyboardButton(text='Rimuovi quiz 🧠', callback_data='rimuoviquiz')
            tastiera.add(cancella)
            x = bot.send_message(canale_log, "🧠 #ADD_QUIZ \n<b>•Di:</b> " + namechanger(call.from_user.first_name,
                                                                                        call.from_user.id) + " [<code>" + str(
                call.from_user.id) + "</code>]\n<b>Domanda: </b>" + str(trova['traccia']).replace("<", "").replace(">",
                                                                                                                   "") + "\n<b>•Id domanda: </b>" + str(
                iddi), reply_markup=tastiera, parse_mode="html")
            dbinfo.insert_one({'argomento': 'adding', 'message': x.message_id, 'di': call.from_user.id, 'number': iddi})
        except Exception as ex:
            salvaerrore(ex)
            print(ex)

    except Exception as ex:
        salvaerrore(ex)
        print(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'rimuoviquiz')
def rimuoviqyuzzi(call):
    ricerca = dbinfo.find_one({'argomento': 'adding', 'message': call.message.message_id})

    if ricerca != None:
        if ricerca['di'] == call.from_user.id:
            n = dbinfo.find_one({'trova': 1})
            dbinfo.find_one_and_update({'trova': 1}, {"$set": {'nquiz': n['nquiz'] - 1}}, upsert=True)
            dbquiz.delete_one({'id': ricerca['number']})
            dbinfo.insert_one({'argomento': 'cancellato', 'id': ricerca['number']})
            bot.edit_message_text(call.message.text + "\n\n<i>Cancellato 🗑</i>", canale_log, call.message.message_id,
                                  parse_mode="html")
            bot.answer_callback_query(call.id, "🧠»  quiz rimosso", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "🧠»  Non sei l'autore del quiz", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "🧠»  quiz non trovato", show_alert=True)


@bot.callback_query_handler(func=lambda c: c.data == 'spoiler')
def spoiler(call):
    tastiera = types.InlineKeyboardMarkup()
    indietro = types.InlineKeyboardButton(text="🔙 Indietro", callback_data="indietro")
    tastiera.add(indietro)
    try:
        bot.edit_message_text('Invia il contenuto che vuoi mandare come spoiler 🔒', call.message.chat.id,
                              call.message.message_id, reply_markup=tastiera)
        dbinfo.insert_one({'argomento': 'act_spoiler', "di": call.from_user.id})
    except Exception as ex:
        salvaerrore(ex)
        print(ex)


@bot.message_handler(
    content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'animation'],
    chat_types='private')
def startmemor(message): Thread(target=memor, args=[message]).start()


def memor(message):
    try:
        trova = dbinfo.find_one({'argomento': 'act_spoiler', 'di': message.from_user.id})
        cercastep = dbinfo.find_one({'argomento': 'addtraccia', 'di': message.from_user.id})
        if trova != None:
            dbinfo.delete_one({'id': message.from_user.id, "argomento": "act_spoiler"})
            x = bot.forward_message(memory, message.from_user.id, message.message_id)
            tastiera = types.InlineKeyboardMarkup()
            invia = types.InlineKeyboardButton(text='Guarda spoiler 👀', callback_data='lookspoiler')
            tastiera.add(invia)
            y = bot.send_message(gruppo, namechanger(message.from_user.first_name,
                                                     message.from_user.id) + " ha inviato uno spoiler 🔒",
                                 reply_markup=tastiera, parse_mode="html")
            bot.send_message(message.chat.id, "<b>🔒» Spoiler inviato</b>", parse_mode='html')
            dbspoiler.insert_one(
                {'di': message.from_user.id, 'name': message.from_user.first_name, 'message': y.message_id,
                 'messageone': x.message_id, 'visualizzazioni': 0})
            eliminaspoiler(message.from_user.id)
        if cercastep != None:
            if cercastep['step'] == 1:
                if message.text != None:
                    dbinfo.find_one_and_update({'argomento': 'addtraccia', 'di': message.from_user.id},
                                               {"$set": {'traccia': message.text, 'step': 2}}, upsert=True)
                    try_to(message, "💬»<i> Invia la prima risposta</i>")
            elif cercastep['step'] == 2:
                dbinfo.find_one_and_update({'argomento': 'addtraccia', 'di': message.from_user.id},
                                           {"$set": {'a': message.text, 'step': 3}}, upsert=True)
                try_to(message, "💬»<i> Invia la seconda risposta</i>")
            elif cercastep['step'] == 3:
                dbinfo.find_one_and_update({'argomento': 'addtraccia', 'di': message.from_user.id},
                                           {"$set": {'b': message.text, 'step': 4}}, upsert=True)
                try_to(message, "💬»<i> Invia la terza risposta</i>")
            elif cercastep['step'] == 4:
                dbinfo.find_one_and_update({'argomento': 'addtraccia', 'di': message.from_user.id},
                                           {"$set": {'c': message.text, 'step': 5}}, upsert=True)
                try:
                    tastiera = types.InlineKeyboardMarkup()
                    uno = types.InlineKeyboardButton(text="a", callback_data='primarisp')
                    due = types.InlineKeyboardButton(text="b", callback_data='secondarisp')
                    tre = types.InlineKeyboardButton(text="c", callback_data='terzarisp')
                    tastiera.add(uno, due, tre)
                    bot.send_message(message.chat.id, "✅ » <i>Selezione quale delle risposte è corretta </i>",
                                     parse_mode='html', reply_markup=tastiera)
                except Exception as ex:
                    salvaerrore(ex)
                    print(ex)




    except Exception as ex:
        salvaerrore(ex)
        print(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'lookspoiler')
def guardaspoiler(call):
    trova = dbspoiler.find_one({'message': call.message.message_id})
    try:
        if trova is None:
            bot.answer_callback_query(call.id, "🔒» Spoiler non trovato", show_alert=True)
        else:
            x = bot.forward_message(call.from_user.id, memory, trova['messageone'])

            bot.answer_callback_query(call.id, "✅ Spoiler inviato in privato", show_alert=True)
            bot.send_message(trova['di'], namechanger(call.from_user.first_name,
                                                      call.from_user.id) + " ha visualizzato il tuo spoiler 👀",
                             parse_mode="html")
            visual = dbspoiler.find_one_and_update({'message': trova['message']},
                                                   {"$set": {'visualizzazioni': trova['visualizzazioni'] + 1}},
                                                   upsert=True)
            trova = dbspoiler.find_one({'message': call.message.message_id})
            tastiera = types.InlineKeyboardMarkup()
            invia = types.InlineKeyboardButton(text='Guarda spoiler 👀', callback_data='lookspoiler')
            tastiera.add(invia)
            bot.edit_message_text(
                f"{namechanger(trova['name'], trova['di'])} ha inviato uno spoiler 🔒 \n visualizzazioni: {trova['visualizzazioni']}",
                gruppo, trova['message'], reply_markup=tastiera, parse_mode='html')
    except Exception as ex:
        if "bot was blocked by the user" in str(ex):
            bot.answer_callback_query(call.id, "🔒» Per visualizzare lo spoiler avvia il bot in privato",
                                      show_alert=True)
        else:
            salvaerrore(ex);
            print(ex)

    # * Handler post sul canale


@bot.channel_post_handler(
    content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'animation'])
def canalestart(message): Thread(target=canale, args=[message]).start()


def canale(message):
    try:
        if message.chat.id == canale_gruppo: bot.forward_message(gruppo, canale_gruppo, message.message_id)
        if message.chat.id == canale_artehub: bot.forward_message(gruppo, canale_artehub, message.message_id)
        if message.chat.id == -1001599554760: bot.forward_message(gruppo, -1001599554760, message.message_id)
    except Exception as ex:
        salvaerrore(ex)


# ! quiz

def quiz(message):
    try:
        n = dbinfo.find_one({'trova': 1})
        numero = random.randint(1, n['nquiz'])
        if dbinfo.find_one({'argomento': 'rimosso', 'id': n['nquiz']}) != None:
            quiz(message)
        cerca = dbquiz.find_one({'id': numero})
        if cerca is None:
            quiz(message)
        else:
            tastiera = types.InlineKeyboardMarkup()
            a = types.InlineKeyboardButton(text='a', callback_data='primarisposta')
            b = types.InlineKeyboardButton(text='b', callback_data='secondarisposta')
            c = types.InlineKeyboardButton(text='c', callback_data='terzarisposta')
            tastiera.add(a, b, c)
            x = bot.send_message(message.chat.id,
                                 "❓Traccia »<i>" + str(cerca['traccia']) + "</i>\n\n<i>💬 Risposte: \n A. " + str(
                                     cerca['a']) + "\n B. " + str(cerca['b']) + "\n C. " + str(cerca['c']) + "</i>",
                                 parse_mode='html', reply_markup=tastiera)
            quizzes.append(x.message_id)
            dbinfo.insert_one({'argomento': 'quiz', 'quizid': x.message_id, 'corretta': cerca['corretta']})

    except Exception as ex:
        salvaerrore(ex)


def gtlvl(esperienza: int):
    return math.floor(esperienza / 1000)





@bot.callback_query_handler(func=lambda c: c.data == 'primarisposta')
def rispostaprima(call):
    try:
        cerca = dbinfo.find_one({'quizid': call.message.message_id})
        if cerca is None or quizzes.count(call.message.message_id) == 0:
            bot.answer_callback_query(call.id, "❌ » Hanno già risposto a questo quiz", show_alert=True)
        else:
            if (dbinfo.find_one(
                    {'argomento': 'rispostascorretta', 'quiz': cerca['quizid'], 'id': call.from_user.id}) is None):
                if cerca['corretta'] == 'a':
                    quizzes.remove(call.message.message_id)
                    bot.edit_message_text('<i>🏆 » Quiz indovinato da ' + namechanger(call.from_user.first_name,
                                                                                     call.from_user.id) + "</i>",
                                          call.message.chat.id, call.message.message_id, parse_mode='html')
                    won = random.randint(10, 250)
                    event_plus(call.from_user.id,call.from_user.first_name, won)
                    bot.answer_callback_query(call.id, "🏆 Complimenti hai indovinato! \n 🌟 Hai vinto " + str(
                        won) + " punti esperienza", show_alert=True)
                    info = controlla_e_crea(call.from_user.first_name, call.from_user.id)
                    niu = gtlvl(info['esperienza'])
                    vecc = gtlvl(info['esperienza'] + won)
                    if (niu < vecc):
                        bot.send_message(gruppo,
                                         f"<b>⭐️ {namechanger(call.from_user.first_name, call.from_user.id)} Hai raggiunto il livello</b> {vecc}",
                                         parse_mode='html')
                    dbstato.find_one_and_update({'id': call.from_user.id}, {
                        "$set": {"esperienza": info['esperienza'] + won, "name": call.from_user.first_name}},
                                                upsert=True)

                else:
                    dbinfo.insert_one(
                        {'argomento': 'rispostascorretta', 'quiz': cerca['quizid'], 'id': call.from_user.id})
                    bot.answer_callback_query(call.id, "❌ » Risposta errata", show_alert=True)
            else:
                bot.answer_callback_query(call.id, "❌ » Puoi rispondere solo una volta", show_alert=True)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'secondarisposta')
def rispostaprima(call):
    try:
        cerca = dbinfo.find_one({'quizid': call.message.message_id})
        if cerca is None or quizzes.count(call.message.message_id) == 0:
            bot.answer_callback_query(call.id, "❌ » Hanno già risposto a questo quiz", show_alert=True)
        else:
            if (dbinfo.find_one(
                    {'argomento': 'rispostascorretta', 'quiz': cerca['quizid'], 'id': call.from_user.id}) is None):
                if cerca['corretta'] == 'b':
                    quizzes.remove(call.message.message_id)
                    bot.edit_message_text('<i>🏆 » Quiz indovinato da ' + namechanger(call.from_user.first_name,
                                                                                     call.from_user.id) + "</i>",
                                          call.message.chat.id, call.message.message_id, parse_mode='html')
                    won = random.randint(10, 250)
                    bot.answer_callback_query(call.id, "🏆 Complimenti hai indovinato! \n 🌟 Hai vinto " + str(
                        won) + " punti esperienza", show_alert=True)
                    event_plus(call.from_user.id,call.from_user.first_name, won)
                    info = controlla_e_crea(call.from_user.first_name, call.from_user.id)
                    niu = gtlvl(info['esperienza'])
                    vecc = gtlvl(info['esperienza'] + won)
                    if (niu < vecc):
                        bot.send_message(gruppo,
                                         f"<b>⭐️ {namechanger(call.from_user.first_name, call.from_user.id)} Hai raggiunto il livello</b> {vecc}",
                                         parse_mode='html')
                    dbstato.find_one_and_update({'id': call.from_user.id}, {
                        "$set": {"esperienza": info['esperienza'] + won, "name": call.from_user.first_name}},
                                                upsert=True)
                else:
                    dbinfo.insert_one(
                        {'argomento': 'rispostascorretta', 'quiz': cerca['quizid'], 'id': call.from_user.id})
                    bot.answer_callback_query(call.id, "❌ » Risposta errata", show_alert=True)
            else:
                bot.answer_callback_query(call.id, "❌ » Puoi rispondere solo una volta", show_alert=True)
    except Exception as ex:
        salvaerrore(ex)


@bot.callback_query_handler(func=lambda c: c.data == 'terzarisposta')
def rispostaprima(call):
    try:
        cerca = dbinfo.find_one({'quizid': call.message.message_id})
        if cerca is None or quizzes.count(call.message.message_id) == 0:
            bot.answer_callback_query(call.id, "❌ » Hanno già risposto a questo quiz", show_alert=True)
        else:
            if (dbinfo.find_one(
                    {'argomento': 'rispostascorretta', 'quiz': cerca['quizid'], 'id': call.from_user.id}) is None):
                if cerca['corretta'] == 'c':
                    quizzes.remove(call.message.message_id)
                    bot.edit_message_text('<i>🏆 » Quiz indovinato da ' + namechanger(call.from_user.first_name,
                                                                                     call.from_user.id) + "</i>",
                                          call.message.chat.id, call.message.message_id, parse_mode='html')
                    won = random.randint(10, 250)
                    event_plus(call.from_user.id,call.from_user.first_name, won)
                    bot.answer_callback_query(call.id, "🏆 Complimenti hai indovinato! \n 🌟 Hai vinto " + str(
                        won) + " punti esperienza", show_alert=True)
                    info = controlla_e_crea(call.from_user.first_name, call.from_user.id)
                    niu = gtlvl(info['esperienza'])
                    vecc = gtlvl(info['esperienza'] + won)
                    if (niu < vecc):
                        bot.send_message(gruppo,
                                         f"<b>⭐️ {namechanger(call.from_user.first_name, call.from_user.id)} Hai raggiunto il livello</b> {vecc}",
                                         parse_mode='html')
                    dbstato.find_one_and_update({'id': call.from_user.id}, {
                        "$set": {"esperienza": info['esperienza'] + won, "name": call.from_user.first_name}},
                                                upsert=True)
                else:
                    dbinfo.insert_one(
                        {'argomento': 'rispostascorretta', 'quiz': cerca['quizid'], 'id': call.from_user.id})
                    bot.answer_callback_query(call.id, "❌ » Risposta errata", show_alert=True)
            else:
                bot.answer_callback_query(call.id, "❌ » Puoi rispondere solo una volta", show_alert=True)
    except Exception as ex:
        salvaerrore(ex)





#! Events 

receventuser = client.get_database('events').UserCollection
receventinfo= client.get_database('events').info 
def create_new_event(): 
    titolo = "esperienza"
    receventinfo.insert_one({ 
        "title " : titolo,
        "ttl" : time.time() + 604800
    })
    bot.send_message(canale_gruppo, f"🏆Nuovo Evento {titolo}")
    bot.send_message(gruppo, f"🏆Nuovo Evento {titolo}")
def close_event():
    ris = receventinfo.find_one({})
    if ris is not None :
        classifica = ""
        i = 0 
        documents = receventuser.find({}).sort('punti', -1).limit(10)
        for document in documents : 
            i = i + 1 
            classifica = classifica + str(i)+". "+document['name'].replace('<', '').replace('>', '') + " " + str(document['punti'])+" ⭐️\n"
        bot.send_message(canale_gruppo,f"🏆 Vincitori dell'evento 🏆\n" + classifica ,parse_mode='html') 
        bot.send_message(gruppo,f"🏆 Vincitori dell'evento  🏆\n" + classifica ,parse_mode='html') 
        receventuser.delete_many({})
        receventinfo.delete_many({})
        checkevent()


def checkevent() : 
    ris = receventinfo.find_one({})
    if receventinfo.count_documents({}) > 1 : 
        receventinfo.delete_many({}) 
        create_new_event()
        return False 
    elif ris == None : 
        create_new_event()
        return False 
    elif ris != None : 
        if time.time() > ris['ttl']: 
            close_event()
            return False 
        else : return True 
    else : 
        return True

        
    

@bot.edited_message_handler(commands=['evento', 'EVENTO'], chat_types='supergroup')
@bot.message_handler(commands=['evento', 'EVENTO'], chat_types='supergroup')
def startrankevneto(message): Thread(target=rankevento, args=[message]).start()
def rankevento(message): 
    ris = receventinfo.find_one({})
    if ris is not None :
        classifica = ""
        i = 0 
        documents = receventuser.find({}).sort('punti', -1).limit(10)
        for document in documents : 
            i = i + 1 
            classifica = classifica + str(i)+". "+document['name'].replace('<', '').replace('>', '') + " " +str(document['punti']) +" ⭐️\n"
        bot.send_message(gruppo,f"🏆 Classifica dell'evento 🏆\n" + classifica + " \n⏳ <i>"+gettime(time.time(), ris['ttl'])  +"</i>",parse_mode='html') 



@bot.message_handler(content_types=['text'])
def startmess(message): Thread(target=mess, args=[message]).start()


def mess(message):
    if chatblacklist(message.chat.id) is True:
        record = dbstato.find_one({'id': message.from_user.id})
        old = record['esperienza']
        bf = gtlvl(old)
        incrementa_decrementa_stato(message.from_user.first_name, message.from_user.id, "esperienza", "+")
        rec = dbstato.find_one({'id': message.from_user.id})
        new = rec['esperienza']
        aft = gtlvl(new)
        event_plus(message.from_user.id, message.from_user.first_name, 1)
        if (bf < aft):
            try_to(message,
                   f"<b>⭐️ {namechanger(message.from_user.first_name, message.from_user.id)} Hai raggiunto il livello</b> {aft}")
        cerca = dbinfo.find_one({'argomento': 'quiza'})
        if cerca['messa'] + 1 >= cerca['randoma']:
            dbinfo.find_one_and_update({'argomento': 'quiza'},
                                       {"$set": {'messa': 0, 'randoma': random.randint(100, 250)}},
                                       upsert=True)
            quiz(message)
        else:
            dbinfo.find_one_and_update({'argomento': 'quiza'}, {"$set": {'messa': cerca['messa'] + 1}}, upsert=True)

def event_plus (id,utente,aumento): 
    if checkevent() : 
        old = receventuser.find_one({'id':id})
        if old is None : 
            receventuser.insert_one({'name': utente, 'id': id, 'punti' : aumento})
        else : 
            receventuser.find_one_and_update({'id': id},{"$set": {'name': utente, 'punti': old['punti'] + aumento}},upsert=True)
def gettime(now, future): 
    rimanenti = future - now
    continua = True
    g = 0
    h = 0
    m = 0
    while continua == True  : 
        if rimanenti > 86400.0 : 
            rimanenti = rimanenti - 86400 
            g = g + 1 
        elif rimanenti > 3600.0 : 
            rimanenti = rimanenti - 3600
            h = h + 1
        elif rimanenti > 60.0 : 
            rimanenti = rimanenti - 60 
            m = m + 1 
        else: 
            continua = False 
    return   str(g) + " Giorni " + str(h) + " ore "+ str(m) + " minuti " + str(round(rimanenti,0)) + " secondi"
# ! Avvio del bot
try:
    bot.infinity_polling()
except Exception as ex:
    salvaerrore(ex)
