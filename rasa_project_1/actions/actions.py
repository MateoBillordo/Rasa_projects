# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from email import message
from multiprocessing.sharedctypes import Value
import re
from tkinter.messagebox import NO
from turtle import st
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormValidationAction

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

class ActionListarTarjetasDisponibles(Action):
    
    def name(self) -> Text:
         return "action_listar_tarjetas_disponibles"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            message = "Las tarjetas disponibles son: Visa Classic, Gold y Platinum, y Mastercard Standar, Gold y Platinum"
            dispatcher.utter_message(text=str(message))
            return []

class ActionCrearCuenta(Action):

    def name(self) -> Text:
         return "action_crear_cuenta"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            tipo_cuenta = tracker.latest_message['entities'][0]['value']
            message = "Felicitaciones! Has creado una " + str(tipo_cuenta)
            dispatcher.utter_message(text=str(message))
            return [SlotSet("tipo_cuenta",str(tipo_cuenta))]

class ActionCaracteristicasTarjetas(Action):

    def name(self) -> Text:
         return "action_responder_caracteristicas_tarjetas"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            tipo_tarjeta = tracker.latest_message['entities'][0]['value']
            message = "La tarjeta " + str(tipo_tarjeta)
            if str(tipo_tarjeta) == "visa classic":
                message += " ofrece desembolso de efectivo de emergencia, servicio de reemplazo de tarjetas y proteccion de precios"
            elif str(tipo_tarjeta) == "visa gold":
                message += " ofrece desembolso de efectivo de emergencia, servicio de reemplazo de tarjetas, proteccion de precios, garantia extendida y proteccion de compra"
            elif str(tipo_tarjeta) == "mastercard standar":
                message += " ofrece proteccion de compras"
            elif str(tipo_tarjeta) == "mastercard gold":
                message += " ofrece proteccion de compras, garantia extendida, proteccion de precios, asistencia medica en viajes y telemedicina"
            else:
                message += " no se encuentra dentro de nuestras opciones"
            dispatcher.utter_message(text=str(message))
            return []

class ValidateTarjetaCreditoForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_tarjeta_credito_form"
    
    @staticmethod
    def tarjeta_credito_db() -> List[Text]:
        return [
            "visa classic",
            "visa gold",
            "mastercard standar",
            "mastercard gold"
        ]
    
    @staticmethod
    def tipo_cuenta_db() -> List[Text]:
        return [
            "cuenta universal gratuita",
            "caja de ahorro",
            "cuenta corriente",
            "cuenta sueldo"
        ]

    def validar_tipo_cuenta(self, value: Text, dispatcher: "CollectingDispatcher", tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if value.lower() in self.tipo_cuenta_db():
            return [SlotSet("tipo_cuenta",value.lower())]
        elif str(value.lower()) == "no tengo cuenta":
            dispatcher.utter_message(text="Debes tener una cuenta para solicitar una tarjeta")
        else:
            dispatcher.utter_message(response="utter_tipo_cuenta_invalido")
        return [SlotSet("tipo_cuenta",None)]

    def validar_tarjeta_credito(self, value: Text, dispatcher: "CollectingDispatcher", tracker: Tracker,
        domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:

        if value.lower() in self.tarjeta_credito_db():
            return [SlotSet("tipo_tarjeta_credito",value.lower())]
        else:
            dispatcher.utter_message(response="utter_tipo_tarjeta_no_valido")
            return [SlotSet("tipo_tarjeta_credito",None)]