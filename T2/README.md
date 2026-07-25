# Tarea 2: DCCartas contra la DCCatastrofe!

### Main.py
Archivo principal donde se corre la tarea. Contiene la función main que junta todas las funciones de los otros archivos e instancia las clases de jugador e IA. Tambien contiene la función pedir_nombre que pide y devuelve nombre y dificultad elegida.

### DCCartas
Contiene la clase abstracta de carta y sus clases hijas tropa y estructura. También contiene la clase de carta mixta que se construye en base a una tropa y una estructura, hereda sus atributos mediante properties y hereda sus métodos con super().

### Jugadores.py
Contiene las clases de jugador e IA, cada uno con sus atributos correspondientes y métodos de atacar, recibir daño y usar habilidad especial.

### DCCombate.py
Archivo con la función de combate(). Se encarga de hacer combatir a ls cartas. Devuelve True si el usuario derroto a una IA y False si el usuario se queda sin cartas y pierde la partida, donde se finaliza el programa

### tienda.py
Archivo que contiene la clase Tienda y funciones tienda y pool_cartas. Tienda es la clase donde se guardan las cartas de la tienda. La función ienda() ejecuta la tienda y todas sus su secciones cómo curar y revivir cartas, que luego es llamada desde main.py. La función pool_cartas elige cartas al azar para la tienda,

### herramientas.py

contiene varias utilidades como:
cargar_cartas: Lee csv de cartas y las instancia con la clase Carta
cargar_ia: Lee csv de ias y csv de multiplicadores para instanciarlas con la clase IA
Mostrar menu principal: Muestra y ejecuta el meu principal
Colección: Muestra y ejecuta la colección
Seleccion Inicial: Usa una random sample para la seleccion inicial de cartas

### paramteros.py

Archivo que contiene los parámetros editables del juego. 

### habilidades_cartas.py y habilidades_ia.py
Iban a ser implementados pero permanecen principalmente vacios. :(

### Cosas implementadas y no implementadas :white_check_mark: :x:

* :white_check_mark: Herencia y Programación Orientada a Objetos (OOP) : Implementado correctamente
* :white_check_mark: Interfaz y Juego Inicial : Implementado correctamente
* :white_check_mark: Clase Carta : Implementado correctamente
* :white_check_mark: Clase Carta Tropa : Implementado correctamente
* :white_check_mark: Clase Carta Estructura : Implementado correctamente
* :white_check_mark: Cartas Mixtas : Implementado correctamente
* :white_check_mark: Clase Jugador : Implementado correctamente
* :white_check_mark: Clase Inteligencia Artificial (IA) : Implementado correctamente
* :white_check_mark: Menús y Flujo del Juego : Implementado correctamente
* :white_check_mark: Reglas de Juego y Combate : Implementado correctamente
* :white_check_mark: Archivos y Parámetros : Implementado correctamente
* :white_check_mark: Estilo, Organización y Entrega : Implementado correctamente
* :x: HABILIDADES: Solo implementé la del montapatos, todas las otras cartas y ias no tienen habilidad
* :x: Bonus: No lo implementé.

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. No es necesario crear ni ejecutar nada más. Este codigo fue escrito en la version de python ```3.12.8``` y no se probo en versiones posteriores.

## Librerías :books:
La lista de librerías que utilicé fue la siguiente:

1. ```os```: para verificar que existieran los archivos
2. ```random```: para obtener probabilidades al azar dentro de parametros dados.


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

Se modularizaron muchos archivos pero no se creo una libreria como tal.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Asumo que solo son cambiados los parametros desde parametros.py


-------
Link usado para ver como usar enumerate:
https://www.codecademy.com/resources/docs/python/built-in-functions/enumerate
Para hacer un __str__ personalizado en la clase Jugador
