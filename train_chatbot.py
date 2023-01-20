import json

import pickle

import numpy as np

import emoji

import nltk
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense,Dropout
from tensorflow.keras.optimizers import SGD
from selenium.webdriver.common.keys import Keys

def guardar_json(datos, filename):
    '''creacion de funcion para guardar
    diccionario de conocimiento en formato json'''
    archivo=open(filename,"w")
    json.dump(datos,archivo,indent=4)


biblioteca = {"intents":
                  [{"tag": "saludos",
                    "patterns": ['hola', 'buenos dias', 'buenas tardes'],
                    "responses": [f'Hola soy Chick-BOT \u263A el ayudante N°1 de Productos MELO. ¿Como puedo ayudarte? \u2B50 \nPreguntame sobre mis usos!'],
                    "context": [""]
                    },

                   {"tag": "despedidas",
                    "patterns": ['Chao', 'Adios', 'Hasta luego', 'Nos vemos pronto', 'Hasta la proxima'],
                    "responses": ['Hasta luego! que tenga un buen dia \u2728', 'Chao. Muchas gracias por usar nuestros servicios! \u2728', 'Para servirle! \u2728'],
                    "context": [],
                    },

                    {"tag": "servicios",
                    "patterns": ['Que puedes hacer?', 'Cuales son tus funciones', 'Me puedes ayudar', 'Dime tus servicios', 'Dime tus usos'],
                    "responses": ['Puedo recomendarte servicios que entregamos a todos los productores del pais! Elije entre las siguientes opciones:' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '1. Proteccion para cultivos \u2618' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '2. Equipos y herramientas \u2692' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '3. Salud animal \u271A ' +
                                (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) +
                                  'Escriba su opcion *sin el número* a continuacion \u27A1' + (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) +
                                  'Recuerda que en todo momento puedes cambiar de opcion!'],
                    "context": [],
                    },

                    {"tag": "salud",
                    "patterns": ['Salud animal', 'Medicina', 'Animales', 'Farmacos'],
                    "responses": ['Empresas Melo tiene como objetivo cuidar de sus animales y ganado \u2764' +
                                  (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT) + 'Qué tipo de equipo farmaceutico necesita?' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '1. Antibioticos' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '2. Vacunas' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '3. Vitaminas' +
                                    (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '4. Higiene animal' +
                                    (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '5. Antiinflamatorios' +
                                    (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '6. Desparasitantes' +
                                    #(Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '7. Anabolicos' +
                                (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) +
                                  'Escriba su opcion *sin el número* a continuacion \u27A1'],
                    "context": [],
                    },

                    {"tag": "antibioticos",
                    "patterns": ['Antibioticos', 'antibioticos'],
                    "responses": ['Empresas MELO distribuye diversos tipos de antibioticos en todas sus sucursales \u27A1' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Seleccione el siguiente enlace para conocer más! https://almacenesagropecuarios.com/salud-animal/antibioticos' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Esperamos serle de ayuda'],
                    "context": [],
                    },

                    {"tag": "vacunas",
                    "patterns": ['Vacunas', 'vacunas'],
                    "responses": ['Empresas MELO distribuye diversas vacunas en todas sus sucursales \u27A1' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Seleccione el siguiente enlace para conocer más! https://almacenesagropecuarios.com/salud-animal/vacunas' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Esperamos serle de ayuda'],
                    "context": [],
                    },

                    {"tag": "vitaminas",
                    "patterns": ['Vitaminas', 'vitaminas'],
                    "responses": ['Empresas MELO distribuye diversas vitaminas en todas sus sucursales \u27A1' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Seleccione el siguiente enlace para conocer más! https://almacenesagropecuarios.com/salud-animal/vitaminas' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Esperamos serle de ayuda'],
                    "context": [],
                    },

                    {"tag": "higiene",
                    "patterns": ['Higiene animal', 'higiene', 'limpieza'],
                    "responses": ['Empresas MELO distribuye shampoos y equipos de limpieza en todas sus sucursales \u27A1' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Seleccione el siguiente enlace para conocer más! https://almacenesagropecuarios.com/salud-animal/higiene-animal' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Esperamos serle de ayuda'],
                    "context": [],
                    },

                    {"tag": "antiinflamatorios",
                    "patterns": ['Antiinflamatorios', 'antinflamatorios'],
                    "responses": ['Empresas MELO distribuye diversos inflamatorios en todas sus sucursales \u27A1' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Seleccione el siguiente enlace para conocer más! https://almacenesagropecuarios.com/salud-animal/antiinflamatorios' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Esperamos serle de ayuda'],
                    "context": [],
                    },

                    {"tag": "desparasitantes",
                    "patterns": ['Desparasitantes', 'parasitos', 'Parásitos'],
                    "responses": ['Empresas MELO distribuye diversos desparasitantes en todas sus sucursales \u27A1' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Seleccione el siguiente enlace para conocer más! https://almacenesagropecuarios.com/salud-animal/desparasitantes' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Esperamos serle de ayuda'],
                    "context": [],
                    },


                    #{"tag": "anabolicos",
                    #"patterns": ['Anabolicos', 'esteroides'],
                    #"responses": ['Empresas MELO distribuye diversos anabolicos en todas sus sucursales \u27A1' +
                    #              (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Seleccione el siguiente enlace para conocer más! https://almacenesagropecuarios.com/salud-animal/anabolicos' +
                    #              (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Esperamos serle de ayuda'],
                    #"context": [],
                    #},

                    {"tag": "herramientas",
                    "patterns": ['Equipos y herramientas', 'Equipos', 'Herramientas para construir'],
                    "responses": ['Empresas MELO busca entregar equipos de calidad para el cuidado del sector agropecuario \u2692' +
                                  (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT) + 'Qué tipo de equipo necesita?' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '1. Comederos y bebederos' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '2. Mallas y alambres' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '3. Accesorios' +
                                (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) +
                                  'Escriba su opcion *sin el número* a continuacion \u27A1' + (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) +
                                  'Recuerda que en todo momento puedes cambiar de opcion!'],
                    "context": [],
                    },

                    {"tag": "comederos",
                    "patterns": ['Comederos y bebederos', 'comederos', 'bebederos'],
                    "responses": ['Nuestras sucursales le pueden entregar bebederos automáticos, dispensadores y comederos '
                                  'con diferentes equipos prácticos para que pueda integrarlos a su ganado sin inconvenientes \u27A1' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Seleccione el siguiente enlace para conocer más! https://almacenesagropecuarios.com/equipos-y-accesorios/comederos-y-bebederos' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Esperamos serle de ayuda'],
                    "context": [],
                    },

                    {"tag": "mallas",
                    "patterns": ['Mallas y alambres', 'mallas', 'alambres', 'cercas', 'Cercar ganado'],
                    "responses": ['Nuestras sucursales pueden proveer mallas de diferentes formas, alambres con o sin puas, '
                                  'además de alambres de ciclon para que pueda mantener sus terrenos totalmente cercados! \u27A1' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Seleccione el siguiente enlace para conocer más! https://almacenesagropecuarios.com/equipos-y-accesorios/mallas-y-alambres' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Esperamos serle de ayuda'],
                    "context": [],
                    },

                    {"tag": "Accesorios",
                    "patterns": ['Accesorios', 'Botas', 'Bozal', 'Machetes', 'Tanques', 'Montura', 'Guantes', 'Herraduras'],
                    "responses": ['Nuestras sucursales tienen diversos equipos para su utilidad, vestimenta, herramientas, '
                                  'así como arreos para monturas \u27A1' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Seleccione el siguiente enlace para conocer más! https://almacenesagropecuarios.com/equipos-y-accesorios/accesorios' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Esperamos serle de ayuda'],
                    "context": [],
                    },

                   {"tag": "proteccion cultivos",
                    "patterns": ['Proteccion de cultivos', 'Mejorar cultivos', 'Cuidar cultivos'],
                    "responses": ['Buscamos proveer el mejor servicio para el cuidado de sus cultivos y productos \u2705' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Cual tipo de cultivo buscar mejorar:' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '1. Maiz' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '2. Banano' +
                                  (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + '3. Arroz' +
                                (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT) + 'Escriba su opcion *sin el número* a continuacion \u27A1'],
                    "context": [],
                    },

                   {"tag": "agradecimientos",
                    "patterns": ["gracias",
                                 "muchas gracias",
                                 "mil gracias",
                                 "muy amable",
                                 "se lo agradezco",
                                 "fue de ayuda",
                                 "gracias por la ayuda",
                                 "muy agradecido",
                                 "gracias por su tiempo"
                                 ],
                    "responses": ["De nada! \u2764",
                                  "Feliz por ayudarlo! \u2764",
                                  "Gracias a usted! \u2764",
                                  "Estamos para servirle! \u2764",
                                  "Fue un placer! \u2764"
                                  ],
                    "context": [""]
                    },

                    {"tag": "maiz",
                    "patterns": ['Maiz', 'maiz?'],
                    "responses": ['Recomendamos cultivar con el abono Nutrex Siembra 12-24-12 para estimular la germinación, la floración y mejora la calidad de la planta del maíz \u2618'],
                    "context": [],
                    },
                    {"tag": "banano",
                    "patterns": ['Banano', 'banano?'],
                    "responses": ['Recomendamos cultivar con el abono Abono Urea 46% por ser un producto aporta nitrógeno uréico a los cultivos, con lo cual favorece el desarrollo del follaje y el vigor en los tallos mejorando la calidad de la planta del banano \u2618'],
                    "context": [],
                    },
                    {"tag": "arroz",
                    "patterns": ['Arroz', 'arroz?'],
                    "responses": ['Recomendamos cultivar con el abono Nutrex Produccion 19-9-19 por alto contenido en nitrógeno, y medio en fósforo y potasio, es adecuado para cultivos sensibles, mejorando la calidad de la planta del arroz \u2618'],
                    "context": [],
                    },


                   {"tag": "norespuesta",
                    "patterns": [""],
                    "responses": ["No se detecto una respuesta \u2639"
                                  ],
                    "context": [""]
                    }
                   ]
              }
# Guardado de diccionario de conocimiento en formato json.
guardar_json(biblioteca, 'intents.json')

bolsadepalabras = [] # creación de lista vacia para guardar palabras
clases = []          # creacion de lista para guardar etiquetas de la conversación
documents = []       # creación de lista para guardar entrada y su correspondiente etiqueta.

for intent in biblioteca['intents']:

    clases.append(intent['tag'])

    for pattern in intent['patterns']:
        result = nltk.word_tokenize(pattern)
        bolsadepalabras.extend(result)

        documents.append((result, intent['tag']))

print(bolsadepalabras)
print(clases)

for elemento in documents:
    print('\n')
    print(elemento)

pickle.dump(bolsadepalabras, open("bolsadepalabras.pkl", "wb"))  # guarda bolsa de palabras como archivo .pkl
pickle.dump(clases, open("classes.pkl", "wb"))  # guarda lista de clases como archivo .pkl


l1 = 'buen dias'
l2 = 'buen tardes'
l3 = 'bienvenidos'

bagofwords= []                 # creación de lista vacia
bagofwords.extend(l1.split())  # agregar conversación l1 a bagofwords
bagofwords.extend(l2.split())  # agregar conversación l2 a bagofwords
bagofwords.extend(l3.split())  # agregar conversación l3 a bagofwords

bagofwords = list(set(bagofwords))

print("Bolsa de palabras")
print(bagofwords)

# se realiza la representación binaria respetando el orden de la bolsa de palabras
l1binario = [0, 1, 0 ,0 ,1] # creacion en forma manual de la representacion binaria de l1
l2binario = [1, 0, 0, 0, 1] # creacion en forma manual de la representacion binaria de l2
l3binario = [0, 0, 0, 1, 0] # creacion en forma manual de la representacion binaria de l3

print('\n')
print('l3 como string', '\t'*2,l3)
print('l3 como binario', '\t'*1, l3binario)

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
print(bolsadepalabras)


# ### Uso de la funcion split y join para eliminar espacios dobles.

# In[8]:


sentencia = 'HOLAA    como estas?'         # string de entrada
print(sentencia.split())                   # aplicacion del metodo split para obtener una lista de los elementos por separado.
sentencia= ' '.join(sentencia.split())     # aplicacion del metodo join para unir la lista anterior
print(sentencia)
sentencia = sentencia.lower()              # conversion a minusculas
print(sentencia)


def cleanString(words, ignore_words):
    '''uncion utilizada para limpiar lista de palabras,
     el uso de funciones, evita repetir la innecesaria de codigo'''
    words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
    return words


bolsadepalabras = cleanString(bolsadepalabras, ignore_words)
training = [] # Creacion de lista vacia de para agregar los vectores construidos en las siguientes lineas.

for doc in documents:

    interaccion = doc[0]  # obtencion del primer elemento guardado en cada posicion de la lista documents.
    interaccion = cleanString(interaccion, ignore_words)  # limpieza del strin "interaccion"

    entradacodificada = []  # creacion de la lista vacia llamada "entradacodificada"

    # codificacion de la entrada
    for palabra in bolsadepalabras:
        if palabra in interaccion:
            entradacodificada.append(1)
        else:
            entradacodificada.append(0)

            # codificacion de la etiqueta
    salidacodificada = [0] * len(clases)
    indice = clases.index(doc[1])
    salidacodificada[indice] = 1

    training.append([entradacodificada, salidacodificada])

training = np.array(training, dtype=list)

x_train = list(training[:, 0])

y_train = list(training[:, 1])

model = Sequential()

model.add(Dense(128, input_shape=(len(x_train[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu')) #capa oculta -> aprendizaje
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]),activation='softmax'))


# ## 9. Entrenamiento de nuestra red neuronal.

# In[11]:


sgd = SGD(learning_rate=0.01,momentum=0.9,nesterov=True) # ,decay=1e-6

model.compile(loss="categorical_crossentropy",optimizer=sgd,metrics=["accuracy"])

hist = model.fit(np.array(x_train),np.array(y_train),epochs=300,batch_size=5,verbose=True)
model.save("chatbot_model.h5",hist)
print("modelo creado")