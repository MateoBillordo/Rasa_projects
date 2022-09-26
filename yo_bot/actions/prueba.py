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
            
#         prolog_thread.query_async("materiasAprobadas(X)", find_all=False)
#         # result = prolog_thread.query_async_result()[0]['X'] #obtengo la lista de prolog
        
#         # for i in range(len(result)-1):
#         #     message += result[i] + ', '
        
#         # message = message.rstrip(', ')

#         # message += ' y ' + result[len(result)-1]

#         # print(message)

#         lista = [{'c':'v1'},{'c':'v2'}]
#         i = lista.index(next((x for x in lista if x['c'] == 'v2'),None))
#         print(i)