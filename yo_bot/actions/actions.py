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

    def consulta(self,motivo) -> List[Text]:
        result = []
        with PrologMQI() as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query_async(r"consult('C:\\Rasa_projects\\Rasa_projects\\yo_bot\\data\\datos_academicos.pl')", find_all=False)
                
                if str(motivo) == "cursadas":
                    prolog_thread.query_async("materiasCursadas(X)", find_all=False)
                elif str(motivo) == "finales":
                    prolog_thread.query_async("materiasAprobadas(X)",find_all=False)

                result = prolog_thread.query_async_result()[0]['X'] #obtengo la lista de prolog

        return result

class ActionResponderCuantos(Action):

    def name(self) -> Text:
        return "action_responder_cuantos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = ""
        motivoConsulta = tracker.latest_message['entities'][0]['value']
        result = ConsultarAProlog.consulta(motivoConsulta)
        tamanio = len(result)

        if tamanio > 0:
            message += tamanio
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
        motivoConsulta = tracker.latest_message['entities'][0]['value']
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