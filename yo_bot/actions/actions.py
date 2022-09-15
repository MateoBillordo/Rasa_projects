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

        if str(elemento) == "materias":
            message += "X cantidad"
        elif str(elemento) == "finales":
            message += "X cantidad"
        elif str(elemento) == "optativas":
            message += "X cantidad"
        else:
            message += "X cantidad"
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
                    prolog_thread.query_async("findall(X,cursada_aprobada(X),CursadasAprob)", find_all=False)
                    #message += "Lista de "+str(elemento)
                elif str(elemento) == "finales":
                    prolog_thread.query_async("findall(X,final_aprobado(X),FinalesAprob)", find_all=False)
                    # message += "Lista de "+str(elemento)
                elif str(elemento) == "optativas":
                    prolog_thread.query_async("", find_all=False)
                    # message += "Lista de "+str(elemento)
                elif str(elemento) == "correlativas":
                    prolog_thread.query_async("", find_all=False)
                    # message += "Lista de "+str(elemento)
                elif str(elemento) == "carrera":
                    prolog_thread.query_async("", find_all=False)
                    # message = "Ingenieria de Sistemas"
                else:
                    prolog_thread.query_async("", find_all=False)
                    # message = "Perdon, no te entendi"
                
                result = prolog_thread.query_async_result()
                for valor in result.values():
                    message += str(valor) + " "

        dispatcher.utter_message(text=str(message))

        return []