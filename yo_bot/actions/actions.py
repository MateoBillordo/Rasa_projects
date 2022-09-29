# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from swiplserver import PrologMQI
import os.path
import json

class ActionSetTiempoPositivo(Action):

    def name(self) -> Text:
        return "action_set_tiempo_positivo"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:

        ultimoMensaje = tracker.latest_message['entities']

        if len(ultimoMensaje) > 0:
            entidad = next((x for x in ultimoMensaje if x['entity'] == "tiempo"),None)
            if entidad != None:
                for key in entidad:
                    if str(key) == "role" and str(entidad[key]) == "positivo":
                        return [SlotSet("tiempo_positivo",str(entidad['value']))]
            
            return [SlotSet("tiempo_positivo",None)]
        
        return []

class ActionSetTiempoNegativo(Action):

    def name(self) -> Text:
        return "action_set_tiempo_negativo"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:

        ultimoMensaje = tracker.latest_message['entities']
        
        if len(ultimoMensaje) > 0:
            entidad = next((x for x in ultimoMensaje if x['entity'] == "tiempo"),None)
            if entidad != None:
                for key in entidad:
                    if str(key) == "role" and str(entidad[key]) == "negativo":
                        return [SlotSet("tiempo_negativo",str(entidad['value']))]

            return [SlotSet("tiempo_negativo",None)]
        
        return []

class OperarArchivo():

    @staticmethod
    def guardar(AGuardar,ruta):
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
    def consulta(motivos) -> List[Text]:
        result = []
        with PrologMQI() as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query_async(r"consult('C:\\Rasa_projects\\Rasa_projects\\yo_bot\\data\\datos_propios.pl')", find_all=False)
                
                if str(motivos[0]['value']) == "cursadas":
                    if str(motivos[1]['value']) == "pasado":
                        prolog_thread.query_async("materiasCursadas(X)", find_all=False)
                    elif str(motivos[1]['value']) == "presente":
                        prolog_thread.query_async("cursandoMaterias(X)", find_all=False)

                elif str(motivos[0]['value']) == "finales":

                    if str(motivos[1]['value']) == "pasado":
                        prolog_thread.query_async("materiasAprobadas(X)",find_all=False)
                    elif str(motivos[1]['value']) == "presente":
                        prolog_thread.query_async("finalesFaltantes(X)",find_all=False)
                
                elif str(motivos[0]['value']) == "software":
                    if str(motivos[1]['role']) == "positivo":
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

        message = ""
        result = []
        motivosConsulta = tracker.latest_message['entities']
        if str(motivosConsulta[0]['value']) == "optativas":
            if str(motivosConsulta[1]['value']) == "pasado":
                message = "Todavia no hice ninguna optativa"
            else:
                message = "Todavia no investigue sobre las optativas disponibles"
        else:
            result = ConsultarAProlog.consulta(motivosConsulta)
        tamanio = len(result)

        if tamanio > 0:
            message += str(tamanio)
        else:
            message = "Perdon, no te entendi"

        dispatcher.utter_message(text=str(message))

        return []

class ActionResponderQueOCuales(Action):

    def name(self) -> Text:
        return "action_responder_que_o_cuales"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = ""
        result = []
        motivosConsulta = tracker.latest_message['entities']
        if str(motivosConsulta[0]['value']) == "carrera":
            message = "Ingenieria de Sistemas"
        elif str(motivosConsulta[0]['value']) == "optativas":
            if str(motivosConsulta[1]['value']) == "pasado":
                message = "Todavia no hice ninguna optativa"
            else:
                message = "Todavia no investigue sobre las optativas disponibles"
        else:
            result = ConsultarAProlog.consulta(motivosConsulta)
        
            tamanio = len(result)

            if tamanio == 1:
                message = result[0]
            elif tamanio > 1:
                for i in range(0,tamanio-1):
                    message += result[i] + ', '
                message = message.rstrip(', ')
                if (result[tamanio-1][0].lower == "i" or result[tamanio-1][0] == "I"):
                    message += ' e ' + result[tamanio-1]
                else:
                    message += ' y ' + result[tamanio-1]
            else:
                message = "Perdon, no te entendi"

        dispatcher.utter_message(text=str(message))

        return []

class ActionPorque(Action):

    def name(self) -> Text:
        return "action_responder_porque"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = "Perdon, no te entendi"
        positivo = next(tracker.get_latest_entity_values("tiempo","positivo"),None)
        negativo = next(tracker.get_latest_entity_values("tiempo","negativo"),None)
        interes = next(tracker.get_latest_entity_values("area_de_interes"),None)        

        if (interes != None):
            razones = OperarArchivo.cargarArchivo(".\\data\\porque.json")
            if (positivo != None):
                if razones["temas"][interes]["interesa"] == "si":
                    message = "Me interesa porque " + razones["temas"][interes]["porque"]
                else:
                    message = "No me interesa ese tema porque " + razones["temas"][interes]["porque"]
            elif (negativo != None):
                if razones["temas"][interes]["interesa"] == "no":
                    message = "No me interesa porque porque " + razones["temas"][interes]["porque"]
                else:
                    message = "Si me interesa ese tema porque " + razones["temas"][interes]["porque"]
        else:
            pregunta_anterior = tracker.get_slot("pregunta_anterior")
            if (pregunta_anterior != None):

                positivo = tracker.get_slot("tiempo_positivo")
                negativo = tracker.get_slot("tiempo_negativo")
                razones = OperarArchivo.cargarArchivo(".\\data\\porque.json")
                
                if (pregunta_anterior == "software"):
                    
                    if (positivo != None):
                        message = ""
                        for key in razones["temas"]:
                            if razones["temas"][key]["interesa"] == "si":
                                message += "Me interesa " + str(key) + " porque " + razones["temas"][key]["porque"] + ". "
                    
                    elif (negativo != None):
                        message = ""
                        for key in razones["temas"]:
                            if razones["temas"][key]["interesa"] == "no":
                                message += "No me interesa " + str(key) + " porque " + razones["temas"][key]["porque"] + ". "
                
                elif (pregunta_anterior == "carrera"):
                    message = "Elegi esta carrera porque " + razones["carrera"]

        dispatcher.utter_message(text=str(message))

        return []
