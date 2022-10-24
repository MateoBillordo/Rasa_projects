# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from random import randint
from textblob import TextBlob
from googletrans import Translator
from swiplserver import PrologMQI
import os.path
import json

class ActionSetRolTiempo(Action):

    def name(self) -> Text:
        return "action_set_rol_tiempo"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:

        ultimoMensaje = tracker.latest_message['entities']

        if len(ultimoMensaje) > 0:
            entidad = next((x for x in ultimoMensaje if x['entity'] == "tiempo"),None)
            if entidad != None:
                for key in entidad:
                    if str(key) == "role":
                        return[SlotSet("rol_tiempo",entidad[key])]

                return[SlotSet("rol_tiempo",None)]

        return []

class OperarArchivo():

    @staticmethod
    def guardarArchivo(AGuardar,ruta):
        with open(ruta,"w") as archivo_descarga:
            json.dump(AGuardar, archivo_descarga, indent=4)
        archivo_descarga.close()

    @staticmethod
    def cargarArchivo(ruta): 
        if os.path.isfile(ruta):
            with open(ruta,"r") as archivo_carga:
                retorno=json.load(archivo_carga)
                archivo_carga.close()
        else:
            retorno={}
        return retorno

class ConsultarAProlog():

    @staticmethod
    def consulta(motivo):
        with PrologMQI() as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query_async(r"consult('C:\\Rasa_projects\\Rasa_projects\\yo_bot\\data\\datos_propios.pl')", find_all=False)
                retorno = prolog_thread.query(motivo)
                return retorno

    @staticmethod
    def consultaPredefinida(motivo,tiempo,rol_tiempo) -> List[Text]:
        result = []
        with PrologMQI() as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query_async(r"consult('C:\\Rasa_projects\\Rasa_projects\\yo_bot\\data\\datos_propios.pl')", find_all=False)
                
                if str(motivo) == "cursadas":
                    if str(tiempo) == "pasado":
                        prolog_thread.query_async("materiasCursadas(X)", find_all=False)
                    elif str(tiempo) == "presente":
                        prolog_thread.query_async("cursandoMaterias(X)", find_all=False)

                elif str(motivo) == "finales":

                    if str(tiempo) == "pasado":
                        prolog_thread.query_async("materiasAprobadas(X)",find_all=False)
                    elif str(tiempo) == "presente":
                            prolog_thread.query_async("finalesAdeudados(X)",find_all=False)
                
                elif str(motivo) == "software":
                    if str(rol_tiempo) == "positivo":
                        prolog_thread.query_async("areasDeInteres(X)",find_all=False)
                    else:
                        prolog_thread.query_async("areasDeNoInteres(X)",find_all=False)

                retorno = prolog_thread.query_async_result()
                if (type(retorno) != bool): #si es bool ninguna de las consultas anteriores se ejecuto
                    result = retorno[0]['X'] #obtengo la lista de prolog

        return result

class ActionResponderCuantos(Action):

    def name(self) -> Text:
        return "action_responder_cuantos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = "Perdon, no te entendi (cuantos)"
        result = []
        motivo = tracker.get_slot("pregunta")
        tiempo = tracker.get_slot("tiempo")
        rol_tiempo = tracker.get_slot("rol_tiempo")

        if str(motivo) == "optativas":
            if str(tiempo) == "pasado":
                message = "Todavia no hice ninguna optativa"
            else:
                message = "Todavia no investigue sobre las optativas disponibles"
        elif motivo != None:
            result = ConsultarAProlog.consultaPredefinida(motivo,tiempo,rol_tiempo)
        tamanio = len(result)
        
        if tamanio > 0:
            message = str(tamanio)

        dispatcher.utter_message(text=str(message))

        return []

class ActionResponderQueOCuales(Action):

    def name(self) -> Text:
        return "action_responder_que_o_cuales"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = "Perdon, no te entendi (que o cuales)"
        result = []
        motivo = tracker.get_slot("pregunta")
        tiempo = tracker.get_slot("tiempo")
        rol_tiempo = tracker.get_slot("rol_tiempo")

        if str(motivo) == "carrera":
            message = "Ingenieria de Sistemas"
        elif str(motivo) == "optativas":
            if str(tiempo) == "pasado":
                message = "Todavia no hice ninguna optativa"
            else:
                message = "Todavia no investigue sobre las optativas disponibles"
        elif motivo != None:
            result = ConsultarAProlog.consultaPredefinida(motivo,tiempo,rol_tiempo)
        
            tamanio = len(result)

            if tamanio == 1:
                message = result[0]
            elif tamanio > 1:
                message = ""
                for i in range(0,tamanio-1):
                    message += result[i] + ', '
                message = message.rstrip(', ')
                if (result[tamanio-1][0].lower == "i" or result[tamanio-1][0] == "I"):
                    message += ' e ' + result[tamanio-1]
                else:
                    message += ' y ' + result[tamanio-1]

        dispatcher.utter_message(text=str(message))

        return []

class ActionPorque(Action):

    def name(self) -> Text:
        return "action_responder_porque"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = "Perdon, no te entendi"
        rol_tiempo = tracker.get_slot("rol_tiempo")
        interes = tracker.get_slot("pregunta")

        if (interes != None):
            razones = OperarArchivo.cargarArchivo(".\\data\\porque.json")
            if interes == "software":
                if (str(rol_tiempo) == "positivo"):
                    message = ""
                    for key in razones["temas"]:
                        if razones["temas"][key]["interesa"] == "si":
                            message += "Me interesa " + str(key) + " porque " + razones["temas"][key]["porque"] + ". "
                
                elif (str(rol_tiempo) == "negativo"):
                    message = ""
                    for key in razones["temas"]:
                        if razones["temas"][key]["interesa"] == "no":
                            message += "No me interesa " + str(key) + " porque " + razones["temas"][key]["porque"] + ". "
            elif interes == "carrera":
                message = "Elegi esta carrera porque " + razones["carrera"]
            else:
                if (str(rol_tiempo) == "positivo"):
                    if razones["temas"][interes]["interesa"] == "si":
                        message = "Me interesa porque " + razones["temas"][interes]["porque"]
                    else:
                        message = "No me interesa ese tema porque " + razones["temas"][interes]["porque"]
                elif (str(rol_tiempo) == "negativo"):
                    if razones["temas"][interes]["interesa"] == "no":
                        message = "No me interesa porque porque " + razones["temas"][interes]["porque"]
                    else:
                        message = "Si me interesa ese tema porque " + razones["temas"][interes]["porque"]

        dispatcher.utter_message(text=str(message))

        return []

class ActionChequeaFecha(Action):
    
    def name(self) -> Text:
        return "action_chequea_fecha"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dia = tracker.get_slot("dia")
        hora = tracker.get_slot("hora")
    
        consulta = ConsultarAProlog.consulta(f'horario_valido({dia},"{hora}").')

        if consulta:
            dispatcher.utter_message(response="utter_horario_disponible")
                
        else:
            consulta2 = ConsultarAProlog.consulta(f'dia_y_hora_random(X,Y).')
            ran = randint(0,3)
            if ran == 0:
                dispatcher.utter_message(f"No, en ese horario no estoy disponible")
                dispatcher.utter_message(f"que tal el {consulta2[0]['X']} a las {consulta2[0]['Y']}")
            elif ran == 1:
                dispatcher.utter_message(f"No, no tengo ese horario disponible")
                dispatcher.utter_message(f"Les parece el {consulta2[0]['X']} a las {consulta2[0]['Y']}?")
            elif ran == 2:
                dispatcher.utter_message(f"No, en ese horario no puedo")
                dispatcher.utter_message(f"Que les parece el {consulta2[0]['X']} a las {consulta2[0]['Y']}?")
            else:
                dispatcher.utter_message(f"No, ese horario no lo tengo disponible")
                dispatcher.utter_message(f"Y el {consulta2[0]['X']} a las {consulta2[0]['Y']}?")
        
        return []

class ActionListo(Action):
    
    def name (self) -> Text:
        return "action_listos"

    def run( self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(response="utter_estoy_listo")
        
        return []

class ActionSaludar(Action):

    def name(self):
        return "action_saludar"

    def run(self, dispatcher, tracker, domain):
        # forma de la metadata: {"metadata": {"update_id": 438632107, "message": {"message_id": 107, "from": {"id": 884975258, "is_bot": False, "first_name": "Mateo", "last_name": "Billordo", "username": "Matthew2002", "language_code": "es"}, "chat": {"id": 884975258, "first_name": "Mateo", "last_name": "Billordo", "username": "Matthew2002", "type": "private"}, "date": 1666190279, "text": "hola"}}}
        mensaje = tracker.latest_message
        # tiene la forma: {'id': 884975258, 'is_bot': False, 'first_name': 'NOMBRE', 'last_name': 'APELLIDO', 'username': 'USERNAME', 'language_code': 'es'}
        id_usuario = mensaje["metadata"]["message"]["from"]["id"]

        agenda = OperarArchivo.cargarArchivo(".\\data\\agenda.json")

        if str(id_usuario) in agenda: # si el usuario ya esta en la agenda
            nombre = agenda[str(id_usuario)]["nombre"]

            ran = randint(0,3)
            if ran == 0:
                dispatcher.utter_message(f"Hola {nombre}, que gusto volver a hablar con vos!")
            elif ran == 1:
                dispatcher.utter_message(f"Hola {nombre}, tanto tiempo!")
            else:
                dispatcher.utter_message(f"Hola {nombre}!")

            dispatcher.utter_message(response="utter_preguntar_estado_de_animo")
            
            return [SlotSet("nombre",str(nombre))]
            
        else: # si el usuario no esta en la agenda
            dispatcher.utter_message(response="utter_no_agendado")
        
        return [SlotSet("nombre",None)]

class ActionAgendarContacto(Action):

    def name(self):
        return "action_agendar_contacto"
    
    def run(self, dispatcher, tracker, domain):
        nombre = tracker.get_slot("nombre")
        mensaje = tracker.latest_message
        id_usuario = mensaje["metadata"]["message"]["from"]["id"]
        apellido_usuario = mensaje["metadata"]["message"]["from"]["last_name"]
        username = mensaje["metadata"]["message"]["from"]["username"]

        agenda = OperarArchivo.cargarArchivo(".\\data\\agenda.json")
        
        if str(id_usuario) in agenda: # si el usuario ya esta en la agenda
            nombre_actual = agenda[str(id_usuario)]["nombre"]
            if str(nombre).lower() != str(nombre_actual).lower(): # si el nombre que ingreso el usuario es distinto al que ya tenia
                dispatcher.utter_message(f"Ya te tenia agendado como {nombre_actual}, pero te voy a cambiar el nombre por {nombre}")
            else:
                dispatcher.utter_message("Lo se, es un lindo nombre :)")
        
        else: # si el usuario no esta en la agenda
            dispatcher.utter_message(response="utter_gusto_en_conocerte")
            dispatcher.utter_message(response="utter_preguntar_estado_de_animo")
            
        agenda[str(id_usuario)] = {"nombre": nombre, "apellido": apellido_usuario, "username": username}
        OperarArchivo.guardarArchivo(agenda,".\\data\\agenda.json")

        return []

class ActionResponderMalHumor(Action):

    def name(self):
        return "action_responder_mal_humor"

    def run(self, dispatcher, tracker, domain):
        
        mensaje = tracker.latest_message["text"]

        traductor = Translator()
        mensaje_traducido = traductor.translate(mensaje, dest="en").text
        objetividad = TextBlob(mensaje_traducido).sentiment.subjectivity

        if objetividad > 0.3:
            dispatcher.utter_message(response="utter_animar")
        else:
            dispatcher.utter_message(response="utter_entiendo_hecho_negativo")
        
        return []

class NoContesta(Action):
    def name(self) -> Text:
        return "no_contesta"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return[]

class ActionConfirma(Action):  
    def name (self) -> Text:
        return "action_confirmacion_reu"

    def run( self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(f"Genial, me parece perfecto")
        return []