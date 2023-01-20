import numpy as np

import json
import pickle
import nltk

from tensorflow.keras.models import load_model
from profitability import get_profitability
from weather import get_weather
from selenium.webdriver.common.keys import Keys

model = load_model("chatbot_model.h5")
biblioteca = json.loads(open("intents.json").read())
#words = pickle.load(open("words.pkl", "rb"))
#classes = pickle.load(open("classes.pkl", "rb"))


# ## 11. Creación de funciones: limpieza de entrada y binarización de la entrada.

# In[13]:


# definir funcion para aplicar tokenization, stemming sobre el string suministrado por el usuario.
bolsadepalabras = [] # creación de lista vacia para guardar palabras
clases = []          # creacion de lista para guardar etiquetas de la conversación
documents = []       # creación de lista para guardar entrada y su correspondiente etiqueta.
for intent in biblioteca['intents']:

    clases.append(intent['tag'])

    for pattern in intent['patterns']:
        result = nltk.word_tokenize(pattern)
        bolsadepalabras.extend(result)

        documents.append((result, intent['tag']))

pickle.dump(bolsadepalabras, open("bolsadepalabras.pkl", "wb"))  # guarda bolsa de palabras como archivo .pkl
pickle.dump(clases, open("classes.pkl", "wb"))  # guarda lista de clases como archivo .pkl


from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer('spanish')

ignore_words = ["?", "¿", "!", "¡", "."]  # Lista de simbolos que se desean eliminar.

bolsadepalabras2 = []  # definicion de variable auxiliar para guardar el resultado limpio

for w in bolsadepalabras:  # iteracion sobre la lista de palabras "bolsadepalabras"
    if w not in ignore_words:
        wprocesada = w.lower()  # convertir a minuscula
        wprocesada = stemmer.stem(wprocesada)  # para stemmer
        bolsadepalabras2.append(wprocesada)  # agregar a la lista.

print("bolsadepalabras2:", bolsadepalabras2)


bolsadepalabras = [stemmer.stem(w.lower()) for w in bolsadepalabras if w not in ignore_words]

def cleanEntrada(entradaUsuario):
    entradaUsuario = nltk.word_tokenize(entradaUsuario)
    entradaUsuario = [stemmer.stem(w.lower()) for w in entradaUsuario if w not in ignore_words]
    return entradaUsuario


def convVector(entradaUsuario, bolsadepalabras):
    entradaUsuario = cleanEntrada(entradaUsuario)

    vectorentrada = [0] * len(bolsadepalabras)  # colocar vector de entrada como ceros
    for palabra in entradaUsuario:  # loop sobre la entrada del usuario

        if palabra in bolsadepalabras:  # verificación si la palabra esta dentro de la bolsa de palabras.

            indice = bolsadepalabras.index(
                palabra)  # obtanción del indice de la palabra actual, en la bolsa de palabras
            vectorentrada[indice] = 1  # asignación de 1 en el vector de entrada para el indice correspondiente.

    vectorentrada = np.array(vectorentrada)  # conversión a un arreglo numpy
    return vectorentrada


entradausuario = "buenos dias gracias hasta luego"
vectorentrada = convVector(entradausuario, bolsadepalabras)
vectorentrada


# ## 12. Prueba de nuestra red neuronal sobre la entra del usuario binarizada.

# In[14]:


def gettag(vectorentrada, LIMITE=0):
    vectorsalida = model.predict(np.array([vectorentrada]))[0]

    # cargar los indices y los valores retornados por el modelo
    vectorsalida = [[i, r] for i, r in enumerate(vectorsalida) if r > LIMITE]

    # ordenar salida en funcion de la probabilidad, valor que está contenido en el segundo termino de cada uno de sus elementos.
    vectorsalida.sort(key=lambda x: x[1], reverse=True)
    print(vectorsalida)

    listEtiquetas = []
    for r in vectorsalida:
        listEtiquetas.append({"intent": clases[r[0]], "probability": str(r[1])})
    return listEtiquetas


listEtiquetas = gettag(vectorentrada, LIMITE=0.1)
listEtiquetas

# ## 13. Función para retornar respuesta.

# In[15]:


import random

crops = ['maiz', 'banano', 'arroz']



def getResponse(listEtiquetas, biblioteca):
    response = ''
    etiqueta = listEtiquetas[0]['intent']
    if etiqueta in crops:
        temperature, weatherValue = get_weather()
        profitabilityValue, bestValue = get_profitability(temperature, etiqueta)
        response = "\nLa temperatura actual es " + "{:.2f}".format(temperature) + "°C \u2602 y el clima es " +\
                   weatherValue + (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + "La estimacion de produccion del cultivo " + etiqueta +\
                   " es de " + str(profitabilityValue) + " ton/ha \u2692 \n" + "Si el clima se mantiene se producirá el " + "{:.1f}".format(profitabilityValue*100/bestValue) + \
                   "% del producto como resultado del cambio climático \u2757 recuerda contribuir con pequeñas obras para mejorar el planeta \u267B"
    else:
        response = ''

    #print(etiqueta)
    listadediccionarios = biblioteca['intents']

    for dicionario in listadediccionarios:

        if etiqueta == dicionario['tag']:
            listaDeRespuestas = dicionario['responses']
            respuesta = random.choice(listaDeRespuestas)
            break
    return respuesta + response


respuesta = getResponse(listEtiquetas, biblioteca)
respuesta


# ## 14. ChatbotRespuesta (integración en una función).

# In[16]:


def chatbotRespuesta(entradaUsuario):
    vectorentrada = convVector(entradaUsuario, bolsadepalabras)
    listEtiquetas = gettag(vectorentrada, LIMITE=0)
    respuesta = getResponse(listEtiquetas, biblioteca)
    return respuesta


# ## 15. Interacción con el usuario.

# In[17]:


#entradaUsuario = ''

#while entradaUsuario != 'exit':
#    entradaUsuario = input()
#    respuesta = chatbotRespuesta(entradaUsuario)
#    print(respuesta)