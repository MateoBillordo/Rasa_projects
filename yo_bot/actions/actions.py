# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from email import message
from typing import Any, Text, Dict, List
from unittest import result

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from swiplserver import PrologMQI, PrologThread


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ConsultarAProlog():

    def consulta(motivo) -> List[Text]:
        result = []
        with PrologMQI() as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query_async(r"consult('C:\\Rasa_projects\\Rasa_projects\\yo_bot\\data\\datos_propios.pl')", find_all=False)
                
                if str(motivo['value']) == "cursadas":
                    
                    if str(motivo['role']) == "aprobado":
                        prolog_thread.query_async("materiasCursadas(X)", find_all=False)
                    elif str(motivo['role']) == "cursando":
                        prolog_thread.query_async("cursandoMaterias(X)", find_all=False)
                    else:
                        prolog_thread.query_async("cursadasFaltantes(X)",find_all=False)

                elif str(motivo['value']) == "finales":

                    if str(motivo['role']) == "aprobado":
                        prolog_thread.query_async("materiasAprobadas(X)",find_all=False)
                    elif str(motivo['role']) == "adeudado":
                        prolog_thread.query_async("finalesFaltantesHastaAhora(X)",find_all=False)
                    else:
                        prolog_thread.query_async("finalesFaltantes(X)",find_all=False)

                result = prolog_thread.query_async_result()[0]['X'] #obtengo la lista de prolog

        return result

class ActionResponderCuantos(Action):

    def name(self) -> Text:
        return "action_responder_cuantos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = ""
        motivoConsulta = tracker.latest_message['entities'][0]
        result = ConsultarAProlog.consulta(motivoConsulta)
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
        motivoConsulta = tracker.latest_message['entities'][0]
        if str(motivoConsulta['value']) == "carrera":
            message = "Ingenieria de Sistemas"
        else:
            result = ConsultarAProlog.consulta(motivoConsulta)
        
            tamanio = len(result)

            if tamanio == 1:
                message = result[0]
            elif tamanio > 1:
                for i in range(0,tamanio-1):
                    message += result[i] + ', '
                message = message.rstrip(', ')
                message += ' y ' + result[tamanio-1]
            else:
                message = "Perdon, no te entendi"

        dispatcher.utter_message(text=str(message))

        return []