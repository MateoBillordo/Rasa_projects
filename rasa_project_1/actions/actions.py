# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from email import message
from re import A
from turtle import st
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionListarCuentas(Action):

    def name(self) -> Text:
        return "action_listar_cuentas"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            message = "Los tipos de cuentas disponibles son: Cuenta corriente, caja de ahorro, cuenta universal gratuita y cuenta sueldo. Todas poseen caracteristicas diferentes"
            dispatcher.utter_message(text=str(message))
            return []

class ActionResponderCaracteristicas(Action):
    
    def name(self) -> Text:
         return "action_responder_caracteristicas"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            tipo_cuenta = tracker.latest_message['entities'][0]['value']
            message = "La " + str(tipo_cuenta)
            if str(tipo_cuenta) == "cuenta universal gratuita":
                message += "permite abrir una cuenta bancaria a todas aquellas personas que no posean otro tipo de cuenta en el sistema financiero. Los beneficios que ofrece esta cuenta son la gratuidad en: apertura de cuenta, mantenimiento de la misma, otorgamiento de tarjeta de debito y en extracciones mediante cajero automatico (hasta 8 por mes). Para solicitarla solo es necesario el DNI"
            elif str(tipo_cuenta) == "caja de ahorro":
                message += "es una cuenta gratuita en lo que respecta a apertura, mantenimiento, provision de tarjeta de debito y utilizacion de cajeros automaticos (sin limite). Esta cuenta otorga un rendimiento mensual porcentual sobre el saldo que se encuentre en la cuenta. Adicionalmente, brinda la posibilidad de gestionar gratuitamente tu cuenta a traves de home banking. Para solicitarla solo es necesario la presentacion del DNI a fin de confirmar datos personales"
            elif str(tipo_cuenta) == "cuenta corriente":
                message += "no tiene costo de apertura pero si de mantenimineto, para conocer los montos ingresa al siguiente link www.elbanco.com/cta-cte-montos. Esta cuenta ofrece la posibilidad de operar con un monto en descubierto determinado, el mismo sera fijado al momento de creacion de la cuenta. Ademas, es posible solicitar una chequera asociada a tu cuenta, podras solicitarla una vez que tu cuenta haya sido creada"
            elif str(tipo_cuenta) == "cuenta sueldo":
                message += "es la cuenta donde te depositan el sueldo si trabajas en relación de dependencia. Deberas informarle a tu empleador una vez que hayas creado la cuenta brindandole el numero de la misma para que pueda empezar a depositar tu sueldo alli. Esta cuenta es gratuita, no tiene costo de apertura, mantenimiento ni de provision de la trajeta de debito asociada. Podras operar en cajeros automaticos sin costo alguno (ni limite en cantidad de operaciones por mes)"
            else:
                message += "no se encuentra dentro de nuestras opciones disponibles"
            dispatcher.utter_message(text=str(message))
            return []

class ActionCrearCuenta(Action):

    def name(self) -> Text:
         return "action_crear_cuenta"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            #intent = tracker.latest_message['intent'].get('name')
            tipo_cuenta = tracker.latest_message['entities'][0]['value']
            message = "Para abrir una " + str(tipo_cuenta) + " entra a este link y segui los pasos que alli se indican: www.elbanco/creacion-de-" + str(tipo_cuenta)
            #if str(intent) == "crear_cuenta":
            return [SlotSet("tipo_cuenta",str(tipo_cuenta))]
            #return []