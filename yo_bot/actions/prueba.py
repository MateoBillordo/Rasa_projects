# from dataclasses import replace
# from unittest import result
# from swiplserver import PrologMQI, PrologThread

# elemento = "materias"
# message = ""

# # formatearRespuesta(input):


# with PrologMQI() as mqi:
#     with mqi.create_thread() as prolog_thread:
#         #la unica forma que se me ocurre de diferenciar las entidades es por su valor. Implica una cadena muy grande de if-else
#         prolog_thread.query_async(r"consult('C:\\Rasa_projects\\Rasa_projects\\yo_bot\\data\\datos_propios.pl')", find_all=False)
            
#         prolog_thread.query_async("materiasCursadas(X)", find_all=False)
#         result = prolog_thread.query_async_result()[0]['X'] #obtengo la lista de prolog
        
#         tamanio = len(result)
#         message = ""

#         for i in range(0,tamanio-1):
#             message += result[i] + ', '
#         message = message.rstrip(', ')
#         if (result[tamanio-1][0] == "i" or result[tamanio-1][0] == "I"):
#             message += ' e ' + result[tamanio-1]
#         else:
#             message += ' y ' + result[tamanio-1]

#         print(message)