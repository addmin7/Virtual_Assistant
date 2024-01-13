import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# opcion de voz / idioma
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
id3 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


# escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_Texto():
    # almacenar el reconocedor en una variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzo la grabacion
        print("Ya puedes hablar.")

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language="es-mex")

            # prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            # devolver pedido
            return pedido

        # en caso de que no comprenda el audio
        except sr.UnknownValueError:

            # prueba de que no entendio el audio
            print("Ups, no entendi")

            # devolver error
            return "sigo esperando"

        # en caso de no poder resolver el pedido
        except sr.RequestError:

            # prueba de que no entendio el audio
            print("Ups, no hay servicio")

            # devolver error
            return "sigo esperando"

        # error inesperado
        except:

            # prueba de que no entendio el audio
            print("Ups, algo ha salido mal")

            # devolver error
            return "sigo esperando"


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el dia de la semana
def pedir_dia():
    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario con nombres de dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}

    # el dia de la semnaa
    hablar(f'hoy es {calendario[dia_semana]}')


# informar hora
def pedir_hora():
    # crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    # decir la hora
    hablar(hora)


# saludo inicial
def saludo_inicial():
    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'

    else:
        momento = "buenas tardes"

    # decir el saludo
    hablar(f'{momento}, soy Honey, tu asistente personal. Por favor, ¿dime en que te puedo ayudar?')


# funcion central del asistente
def pedir_cosas():
    # activar saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    # loop central
    while comenzar:

        # activar el microfono y guardar el periddo en un string
        pedido = transformar_audio_en_Texto().lower()

        if 'abrir youtube' in pedido:
            hablar('con gusto, esta iniciando youtube')
            webbrowser.open('https://www.youtube.com')
            continue

        elif 'abrir navegador' in pedido:
            hablar('claro estoy en eso')
            webbrowser.open('https://www.google.com')
            continue

        elif 'que dia es hoy' in pedido:
            pedir_dia()
            continue

        elif 'qué hora es' in pedido:
            pedir_hora()
            continue

        elif 'gracias' in pedido:
            hablar('no hay problema')

        elif 'buscar en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('wikipedia dice lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar("estoy en ello")
            pedido = pedido.replace("busca en internet", '')
            pywhatkit.search(pedido)
            hablar("esto es lo que he encontrado:")
            continue
        elif 'reproducir' in pedido:
            hablar("buena idea, ya comienzo a reproducirlo")
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar("no la ha encontrado")
                continue

        elif 'adiós' in pedido:
            hablar('Esta bien, hasta luego.')
            break


pedir_cosas()