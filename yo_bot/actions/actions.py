# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from email import message
from typing import Any, Text, Dict, List

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

class ActionResponderCuantos(Action):

    def name(self) -> Text:
        return "action_responder_cuantos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        elemento = tracker.latest_message['entities'][0]['value']
        message = ""

        with PrologMQI() as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query_async("consult('plan_de_estudios.pl')", find_all=False)
                if str(elemento) == "materias":
                    prolog_thread.query_async("materiasCursadas(X)", find_all=False)
                    result = prolog_thread.query_async_result()
                    message = str(len(result))

                elif str(elemento) == "finales":
                    prolog_thread.query_async("materiasAprobadas(X)", find_all=False)
                    result = prolog_thread.query_async_result()
                    message = str(len(result))

                elif str(elemento) == "optativas":
                    message += "Cant de "+str(elemento)

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

        elemento = tracker.latest_message['entities'][0]['value']

        message = ""
        with PrologMQI() as mqi:
            with mqi.create_thread() as prolog_thread:
                #la unica forma que se me ocurre de diferenciar las entidades es por su valor. Implica una cadena muy grande de if-else
                prolog_thread.query_async("consult('plan_de_estudios.pl')", find_all=False)
                if str(elemento) == "materias":
                    #message += "Lista de "+str(elemento)
                    prolog_thread.query_async("materiasCursadas(X)", find_all=False)
                    result = prolog_thread.query_async_result()
                    for valor in result.values():
                        message += str(valor) + " "

                elif str(elemento) == "finales":
                    # message += "Lista de "+str(elemento)
                    prolog_thread.query_async("materiasAprobadas(X)", find_all=False)
                    result = prolog_thread.query_async_result()
                    for valor in result.values():
                        message += str(valor) + " "

                elif str(elemento) == "optativas":
                    #prolog_thread.query_async("", find_all=False)
                    message += "Lista de "+str(elemento)

                elif str(elemento) == "carrera":
                    message = "Ingenieria de Sistemas"

                else:
                    message = "Perdon, no te entendi"

        dispatcher.utter_message(text=str(message))

        return []