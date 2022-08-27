# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from email import message
from turtle import st
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_precios"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            costo_producto = tracker.latest_message['entities'][0]['value']
            message = "El costo del producto es de "
            if str(costo_producto) == "tarjeta de credito":
                message += "$500 por mes"
            elif str(costo_producto) == "caja de ahorro":
                message += "$0"
            elif str(costo_producto) == "cuenta corriente":
                message += "$1200 por mes"
            elif str(costo_producto) == "caja fuerte":
                message += "$6500 cada tres meses"
            else:
                message = "El producto indicado no se encuentra disponible"
            dispatcher.utter_message(text=str(message))
            return []
