#!/usr/bin/env python
# coding: utf-8

# In[1]:

from chatbot import chatbotRespuesta
from selenium import webdriver                                     #
from selenium.webdriver.chrome.service import Service              #
from webdriver_manager.microsoft import EdgeChromiumDriverManager  # Importacion de controlador para navegador
from selenium.webdriver.common.by import By                        #
from selenium.webdriver.common.keys import Keys #
from selenium.webdriver.chrome.options import Options
import re                                                          # "re" para expresiones regulares
import time                                                        # Time para generar tiempos de espera

def checkMensajes(usuario):
    '''Funcion para verificar si existen mensajes por leer,
    en algunos casos la class=_1pJ9J, no se consigue,
    por eso se agrego la exception, y retorna verdadero (True)
    si el bloque que se esta verificando tiene mensajes sin leer'''
    try:
        numMens = usuario.find_element(By.CLASS_NAME,"_1pJ9J").text

        msleer = re.findall('\d+' ,numMens)

        if len(msleer) != 0:
            pending = True

        else:
            # Usuarios silenciados, el simbolo posee el mismo nombre de la clase pero no contiene decimales
            pending = False

    except:
        pending = False
    return pending

def getMsgPart(solicitud):
    mensaje = solicitud.text
    html = solicitud.get_attribute('outerHTML')#page_source
#     participante = re.findall(r'<span aria-label="(.+?)\:', html)
    participante = re.findall(r'data-pre-plain-text=.{1}\[.+](.+?):', html)
    return participante, mensaje


# In[2]:


# creacion de la instacia para el navegador EdgeChromium
# Pudes cambiar a otro navegador firrefox Chromium
options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)


# In[3]:


# El metodo "get" navega a la pagina de la url suministrada.
driver.get("https://web.whatsapp.com/")     # se debe escanear el codigo QR  y luego ejecutar la siquiente celda.


# ### Opcion 1: para desarrollar usando excepciones para verificar si existen mensajes sin leer.

# In[4]:


usuariomsg =''

while usuariomsg !='exit':        # Lazo infinito, solo se logra salir si la entra del usuario es "exit"
    print("#", end=" ")
    time.sleep(2)                 # Time sleep para realizar la verificacion de mensajes sin leer cada 2 seg

    # Busqueda de la clase "_10e6M", este bloque, incluye nombre del usuario, mensaje, verificador de mensajes.
    conversaciones = driver.find_elements(By.CLASS_NAME, "_1Oe6M") # a cada bloque encontrado le llamamos "conversaciones"

    # dentro de cada conversacion vamos a realizar la busqueda del nombre del
    # usuario y la veridficacion de mensajes sin leer.
    for usuario in conversaciones:

        # A cada conversasion (Bloque) le llamamos usuario.

        nombres = usuario.find_element(By.CLASS_NAME,"_21S-L") # Busqueda del nombre del usuario.

        porresponder = checkMensajes(usuario) # Verificar si existen mensajes por leer

        # Condicion para entrar en cada conversacion (Solo entra si existen mensajes sin leer)
        if porresponder:

            # Si existen mensajes sin responder debemos dar click sobre la conversacion.


            # busqueda del elemento conversacion,  esto se realiza dentro de cada bloque
            # al que hemos llamado usuarion en el loop iniciado en la linea 12.
            conversacion = usuario.find_element(By.CLASS_NAME,"_1pJ9J")
            conversacion.click()  # Se da click sobre la conversacion.
            time.sleep(3)

            # Buscar ultimos mensajes enviados por el usuario

            solicitudes = driver.find_elements(By.CLASS_NAME,"_27K43")
            for solicitud in solicitudes[-4:]:  # Solo para tomar los ultimos 4 elementos.
                participante, mensaje = getMsgPart(solicitud)
                usuariomsg = mensaje.lower()

            print("Cliente:", participante, "Mensaje:", usuariomsg, end=" ")

            result = chatbotRespuesta(usuariomsg)
            # Buscar box text y enviar respuesta
            textRespuesta = driver.find_element(By.CLASS_NAME,"_3Uu1_") # busqueda del cuadro de texto para enviar respuesta
            textRespuesta.send_keys(result)                   # Envio de mensaje.
            textRespuesta.send_keys(Keys.ENTER)                        # Envio de enter pare realizar envio.
            time.sleep(3)

            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform() # generar ESC para salir de la conversacion


# In[ ]:




