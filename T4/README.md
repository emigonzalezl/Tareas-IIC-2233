# Tarea 4: DCCasino :school_satchel:

En mi tarea, implemente toda la parte del Networking cleinte-servidor, siguieindo los ejemplos de codigo de la experiencia 4 y 5. El cliente se va a conectar correctamente el servidor mediante sockets, las ventanas principales están correctamente implementadas con PyQt5 y señales de comunicacion entre frontend y backend. Lo principal en mi atrea es que funciona el login y la carga de dinero, y se revisa correctamente que no hayan mas usuarios con ese nombre antes de conectarse al servidor. No fue implementado ningun juego ni otros aspectos de la tarea.


## Consideraciones generales :octocat:

<SOLO hice la base nel networking de la tarea, NO esta implementado ningun juego ni interacción de clientes con ellos.>

## Cosas implementadas y no implementadas :white_check_mark: :x:

### Ventanas
* Ventana de inicio: Item hecho completo con notificacion si el nombre de usuario si ya esta en uso por un cliente conectado, y pasa a la ventana principal si esta disponible.
* Ventana principal: Item hecho con historial de actualizar dinero y no se superponen los elementos. Ninguno de los juegos se hizo por lo que los botones no hacen nada.
* Ventana de recarga: Funcional. Permite recargar dinero y permita aumentar o dimsinuirlo en unidades.

### Networking
*TCP/IP: Se raliza cliente/servidor con udo de sockets, connect, bind listen y accept. Cada servidor tiene un thread por cliente.4 bytes de largo.

## Ejecución :computer:
Para ejecutar la tarea es necesario ejeciutar el servidor con su archivo main.py, y luego ejecutar el archivo main.py en cliente.


## Librerías :books:
Lista de librerias utilizadas:

1. PyQt5
2. socket
3. json
4. threading
5. time
6. random
7. sys (solo las funciones permitidas)


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. Mi codigo esta muy fuertemente inspirado de las experiencias 4 y 5, por lo que la gran mayoria esta basado en este, lo que me sirvio para entender bien serialiación y networking y saber como estructurar la tarea y como hacer que el servidor y cliente pudiesen interactuar correctamente. Me base mucho del codigo dado en el curso pero no use codigo de fuentes externas.