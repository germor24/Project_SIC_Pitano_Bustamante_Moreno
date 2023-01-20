# Project_SIC_Pitano_Bustamante_Moreno

Es un chatbot interactivo basado en reconocimiento de lenguaje natural para mejorar los servicios de MELO. El ambiente de desarrollo del chatbot es la vía de conexión entre los clientes o productores que busquen algún tipo de servicio en la empresa MELO. Ya sea para sectores vacunos, o agrónomos, la herramienta proveerá una conexión directa con los usuarios para indicar el posible servicio que requieran.

# Setup de cada Script
1.	Train_chatbot: Script de entrenamiento del modelo a utilizar para recrear las conversaciones con el chatbot. Este posee la biblioteca de datos o palabras que dan como resultado el reconocimiento de patrones o contextos en la conversación.
2.	Chatbot: Script con funciones principales para la ejecución del chatbot. Las funciones utilizadas generan los procesamientos de respuestas comunes, donde se toma el contexto de los mensajes del usuario para ser analizados en el modelo del chatbot entrenado, de esta manera, produciendo una respuesta acertada.
3.	Weather: Script de redireccionamiento para el servidor de OpenWeatherMap. El script entrega la dirección url junto a las llaves de verificación que permiten dar el acceso al programa a toda la información o data del servidor, en este caso, verificando el clima de Panamá.
4.	Profiability: Script de data con una lista de los rangos de producción registrados con respecto a temperaturas captadas en territorio nacional. Este script es el encargado de dar las estimaciones de producción de un cultivo utilizando la data de un estudio realizado desde el año 2005 en Panamá con la producción en toneladas por hectárea de los cultivos del maíz, banano y arroz.
5.	Whatsapp: Script que genera el buscador para enlazar un número privado al sistema de respuestas del chatbot.

# Inicio del sistema
Para ejecutar el codigo, solo se debe inicializar el archivo whatsaap.py el cual expondrá un buscador para enlazar un numero de telefono al servidor de whatsapp el cual estara conectado a python. Luego de esto, el chatbot estara totalmente funcional.

# Vistas del funcionamiento
![image](https://user-images.githubusercontent.com/120022842/213750891-ba2e7e45-9197-44bc-9fc5-7bad4039b093.png)
![image](https://user-images.githubusercontent.com/120022842/213750975-9b9d3804-3d13-4072-ba39-bf6472ca4bc1.png)
![image](https://user-images.githubusercontent.com/120022842/213750985-cff96566-0fdd-4937-bc81-a449d5ce2515.png)
