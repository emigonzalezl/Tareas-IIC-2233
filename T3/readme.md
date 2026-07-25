# Tarea 3: Departamento de las Colecciones del Cosmos 🌌

Logre implementar todo a excepcion del mapa. Para la parte del filtrado en ventana principal el sistema de filtrado es bastante restrictivo y considera que la entidad a filtrar fue escrita primero y las propiedades despues, siguiendo el ejemplo dado en la ventana. 
### Cosas implementadas y no implementadas :white_check_mark: :x:

1. ✅ Carga de datos : Item hecho completo. Tests publicos pasados 100%
2. ✅ Consultas simples : Item hecho completo. Tests publicos pasados 100%
3. ✅ Consultas complejas : Item hecho completo. Tests publicos pasados 100%
4. Interfaz gráfica e Interacción: Se implementa la ventana de entrada, ventana, principal y ventana mapa. Se implementa un sistema de filtrado. No se implementa el mapa.

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```, que contiene todas las clases de ventana y su ejecución. Se creo consultas_2.py para modularizar las consultas complejas y se importaron las funciones a consultas.py para que funcionaran los tests.


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Asumo que para ejecutar consulta, la ruta dada es a una carpeta que contiene la entidad a filtrar, el sistema de filtrado que hice revisa en base a eso y no a archivos individuales. Osea que se peude elegir entre las carpetas
Para la consulta tambien asumo que no se pedira filtrar mas de un elemento a la vez. En mi codigo si se repiten los filtros, es decir si para astronautas filtra primero para los que tienen rango 2 y despues rango 1, no habran coincidencias y por ende no mostrara ninguno. Se asume que el input esta bien escrito, es decir separado por comas y sin espacios




## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. QMessageBox.warning()
--> https://stackoverflow.com/questions/11204733/qmessagebox-warning-yellow-exclamation-mark-icon
2. deleteLater()
--> https://www.geeksforgeeks.org/python/deletelater-method-in-pyqt5/
