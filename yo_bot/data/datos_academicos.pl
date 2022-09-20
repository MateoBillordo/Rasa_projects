%Materias de Ing de Sistemas%
%Codigo,Nombre,Curso,Cuatrimestre,Correlativas

materia(6111,'Introduccion a la Programacion I',1,1,[]).
materia(6112,'Analisis Matematico I',1,1,[]).
materia(6113,'Algebra I',1,1,[]).
materia(6114,'Quimica',1,1,[]).
materia(6121,'Ciencias de la Computacion I',1,2,[]).
materia(6122,'Introduccion a la Programacion II',1,2,[6111]).
materia(6123,'Algebra Lineal',1,2,[6113]).
materia(6124,'Fisica General',1,2,[6112]).
materia(6125,'Matematica Discreta',1,2,[6113]).
materia(6211,'Ciencias de la Computacion II',2,1,[6121,6122,6125]).
materia(6212,'Analisis y Diseño de Algoritmos I',2,1,[6121,6122,6125]).
materia(6213,'Introduccion a la Arquitectura de Sistemas',2,1,[6122]).
materia(6214,'Analisis Matematico II (Ing. de Sistemas)',2,1,[6112]).
materia(6215,'Electricidad y Magnetismo',2,1,[6124]).
materia(6221,'Analisis y Diseño de Algoritmos II',2,2,[6211,6212]).
materia(6222,'Comunicacion de Datos I',2,2,[6213]).
materia(6223,'Probabilidades y Estadistica',2,2,[6214,6123,6125]).
materia(6224,'Electronica Digital',2,2,[6215]).
materia(6311,'Programacion Orientada a Objetos',3,1,[6221]).
materia(6312,'Estructuras de Almacenamiento de Datos',3,1,[6221,6223]).
materia(6313,'Metodologias de Desarrollo de Software I',3,1,[6221]).
materia(6314,'Arquitectura de Computadoras I',3,1,[6213,6224]).
materia(6321,'Programacion Exploratoria',3,2,[6221]).
materia(6322,'Base de Datos I',3,2,[6312,6313]).
materia(6323,'Lenguajes de Programacion I',3,2,[6311]).
materia(6324,'Sistemas Operativos I',3,2,[6312,6314]).
materia(6325,'Investigacion Operativa I',3,2,[6214,6223]).
materia(6411,'Arquitectura de Computadoras y Tecnicas Digitales',4,1,[6314]).
materia(6412,'Teoria de la Informacion',4,1,[6212,6222,6223]).
materia(6413,'Comunicacion de Datos II',4,1,[6222,6324]).
materia(6414,'Introduccion al Calculo Diferencial e Integral',4,1,[6214]).
materia(6421,'Diseño de Sistemas de Software',4,2,[6311,6322,6324]).
materia(6422,'Diseño de Compiladores I',4,2,[6323]).
materia(6511,'Ingenieria de Software',5,1,[6421]).

%Cursadas aprobadas

cursada_aprobada(6114).
cursada_aprobada(6113).
cursada_aprobada(6112).
cursada_aprobada(6111).
cursada_aprobada(6124).
cursada_aprobada(6125).
cursada_aprobada(6121).
cursada_aprobada(6122).
cursada_aprobada(6123).
cursada_aprobada(6214).
cursada_aprobada(6215).
cursada_aprobada(6211).
cursada_aprobada(6213).
cursada_aprobada(6212).
cursada_aprobada(6223).
cursada_aprobada(6222).
cursada_aprobada(6224).
cursada_aprobada(6221).
cursada_aprobada(6311).
cursada_aprobada(6313).
cursada_aprobada(6312).
cursada_aprobada(6314).

%Finales aprobados

final_aprobado(6113).
final_aprobado(6111).
final_aprobado(6112).
final_aprobado(6114).
final_aprobado(6124).
final_aprobado(6125).
final_aprobado(6121).
final_aprobado(6122).
final_aprobado(6123).
final_aprobado(6211).
final_aprobado(6213).

cursada_no_aprobada(X):-materia(X,_,_,_,_),not(cursada_aprobada(X)).

final_no_aprobado(X):-materia(X,_,_,_,_),not(final_aprobado(X)).

cursada_aprobada_final_no_aprobado(X):-cursada_aprobada(X),final_no_aprobado(X).

sin_correlativas(X):-materia(X,_,_,_,Y),length(Y,0).

al_menos_una_correlativa(X):-materia(X,_,_,_,Y),length(Y,L),L>0.

una_correlativa(X):-materia(X,_,_,_,Y),length(Y,1).

%Consultas que devuelven listas
materiasCursadas(Lista):-findall(Nom,(materia(Cod,Nom,_,_,_),cursada_aprobada(Cod)),Lista).

materiasAprobadas(Lista):-findall(Nom,(materia(Cod,Nom,_,_,_),final_aprobado(Cod)),Lista).

cursadasFaltantes(Lista):-findall(Nom,(materia(Cod,Nom,_,_,_),cursada_no_aprobada(Cod)),Lista).

finalesFaltantes(Lista):-findall(Nom,(materia(Cod,Nom,_,_,_),final_no_aprobado(Cod)),Lista).

finalesFaltantesHastaAhora(Lista):-findall(Nom,(materia(Cod,Nom,_,_,_),cursada_aprobada_final_no_aprobado(Cod)),Lista).

%IMPRESION POR PANTALLA

%Imprime el primer elemento de la lista de correlatividades
primero_lista([Cabeza|_]):-
    materia(Cabeza,Nom,_,_,_),
    write(Nom).

%Imprime el resto de la lista de correlatividades
imprimir_lista([]).
imprimir_lista([Cabeza|Cola]):-
    materia(Cabeza,N,_,_,_),
    length(Cola,L),
    (L>0,write(', ');L=0,write(' y ')),
    write(N),
    imprimir_lista(Cola).

%Imprime las materias con solo una correlativa
materias_con_una_correlativa:-
    una_correlativa(X),materia(X,Nom,_,_,Y),
    write('Para hacer '),write(Nom),write(' solo necesitas '),primero_lista(Y),
    nl,fail;nl.

%Imprime las materias de un curso dado
materias_de(A):-write('Materias del curso: '),writeln(A),
    materia(_,X,A,_,_),write('*'),writeln(X),
    fail;nl.

%Imprime el plan de estudios completo
plan_is:-writeln('Plan de Ingenieria de Sistemas'),
    materia(Cod,Nom,Cur,Cua,Correlativas),
    write(' Curso: '),write(Cur),
    write(' Cua: '),write(Cua),
    write(' Nom:'),write(Nom),
    (
        (sin_correlativas(Cod),write(' Sin correlativas'));
        (al_menos_una_correlativa(Cod),write(' Correlativas: '),
        Correlativas=[_|X],primero_lista(Correlativas),imprimir_lista(X))
                   ),
    nl,nl,false;nl.

%Imprime todas las materias cursadas
materias_cursadas:-cursada_aprobada(X),materia(X,Nom,_,_,_),writeln(-Nom),fail;nl.

%Imprime todas las materias aprobadas
materias_aprobadas:-final_aprobado(X),materia(X,Nom,_,_,_),writeln(-Nom),fail;nl.

%Imprime los finales adeudados de las materias cursadas
finales_faltantes_hasta_ahora:-materia(X,Nom,_,_,_),final_no_aprobado(X),cursada_aprobada(X),writeln(-Nom),fail;nl.

%Imprime las cursadas adeudadas
cursadas_faltantes:-materia(X,Nom,_,_,_),cursada_no_aprobada(X),writeln(-Nom),fail;nl.

%Imprime los finales adeudados
finales_faltantes:-materia(X,Nom,_,_,_),final_no_aprobado(X),writeln(-Nom),fail;nl.