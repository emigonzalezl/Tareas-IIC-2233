# Tarea 1: DCCasillas 4️⃣➕5️⃣🟰9️⃣

## Consideraciones generales :octocat:

En mi tarea logre completar ambas clases y  lograr que interactuen entre ellas mediante el uso de el menu. 
En el principal archivo de mi tarea (main.py) se ejecuta la gran mayoría del juego. Este main esta compuesto por:

La función ```iniciar_juego()```, que inicializa la calse de ```DCCasillas``` y la devuelve. La instancio dentro de main al inicial el primer juego y al iniciar un juego nuevo en el menu de acciones.

La funcion ```primer_juego()```, que ejecuta la primera instancia de un juego para resolver el problema de no tener una clase definida aún. Esta función fue planteada al comenzar la tarea, antes de probar los test cases. Luego optimice cada función de clase para que no permitieran su ejecucion si no se cumplian algunos parmetros como que el usuario fuese un string vacio. Sin embargo, esta era la manera mas robusta de evitar errores en la primera instancia de juego antes de recibir ningun input del usuario.

La función ```main.py()``` utilica todas las funciones y clases definidas anteriormente para ejecutar el juego. En la primera parte se utiliza ```primer_juego()```, y dentro de ```primer_juego()``` se instancia la clase DCCasillas mediante el uso de ```iniciar_juego()```. Luego se nombra tablero y dccasillas para ser usados posteriormente, aqui tambien se designa el tablero 1 (o 0) como tablero actual. Se pasa al menu de acciones.

La siguiente parte consta de dos while, uno dentro del otro. EL while exterior es el menu de acciones y dentro de la opcion "Volver al menu de juego" se encuentra el while del menu de juego. En este se pueden ejecutar todas las acciones, mientras que en el menu de acciones la accion "resolver tablero" **no logro ser implementada.**

Idealmente, todas las funciones que no son ```main()``` estarian en ```herramientas.py```, pero esto ya no lo hice con tiempo y no quiero arriesgarme a romper el codigo (ultimo push en una hora), pero esa era mi idea inicial y formato ideal para modularizar mas mi codigo.

## tablero.py

### ✅ __init__()
El archivo inicializa los tres atributos de clase. No se añadieron atributos adicionales. Paso todos los tests publicos.

### ✅ cargar_tablero()
Carga el tablero segun el archivo de tablero correspondiente. Es una función simple que cicla por cada casilla del archivo armando el tablero y añadiendo cada dila al atributo de clase de tablero. Para esta función supongo que el archivo esta correctamente armado y sigue el formato de dado en el enunciado donde la primera linea da la cantidad de filas y columnas editables en el tablero (o el largo real del tablero por indices desde '0'). Paso todos los tests publicos.

### ✅ mostrar_tablero()
Imprime el tablero actual usando la funcion imprimir_tablero importada desde visualizador.pyc. Siempre cumple su función en el terminal pero sin los test cases publicos no estoy segura de si manejo todos los casos posibles. Asumo que el tablero que se va a entregar para mostrar usando el visualizador esta correctamente construido.

### ✅ modificar_casilla()
Para esta función no realizo muchos supuestos, ya que mi función logra controlar varias situaciones donde posiblemente los paramtero ingresados arrojarian error. Se revisa que el input, en caso de ser un int, esté dentro de el largo máximo para filas y columnas, que no sea negativo, y que la casilla a editar sea válida. En caso de qué input sea un String se revisa que te cumpla con .isdigit() y se convierte a int para pasar por el mismo control que si fuese un int. Paso todos los tests publicos.

### ✅ validar_tablero()
Valida la solución del tablero actual. Para esto se recorre cada casilla regular que contenga un numero, se realiza una suma para cada fila y columna y se ve que cumpla con la restriccion de la ultima fila/columna segun corresponda. En el caso de qué uno de estos chequeos no se ha válido, toda la función retorna False. Paso todos los tests publicos.

### ❌ resolver_tablero()
Me quede sin tiempo para resolver esta función. Es la una parte faltante en mi tarea. Se representa en el main como: "función todavia no disponible".

## dccasillas.py

### ✅ __init__()
A mi parecer esta completa. Hace todo lo necesario para la correcta ejecucion de todas sus funciones de clase. Sin embargo al no tener los test cases publicos a mano no estoy segura de lo que pedian mas alla del enunciado. Todos los atributos funcionan correctamente. dentro de self.tableros hay una lista con todas las instancias de Tablero disponibles para la configuración actual y sus respectivos tableros.

### ✅ abrir_tablero()
En esta función cambio el número de tablero actual para la instancia DCCasillas por el número de tablero especificado. Aqui realizo el supuesto de qué el parámetro recibido por la función va a ser un int (para los test cases), y en el menu me aseguro de controlar los parametros de entrada y transformarlo a int antes de ingresarlos a la función. Paso todos los tests publicos.

### ✅ guardar_estado()
Esta función guarda correctamente el estado de juego del usuario. Se revisa que el archivo config exista usando ```os.path.exists(ruta)```, pero se realiza el supuesto de que si el archivo config dado existe, los tableros asociados a este también. Se itera para cada casilla y se escribe (o reescribe si es que ya existia) el archivo usuario.txt con el formato solicitado. Paso todos los tests publicos.

### ✅ recuperar_estado 
La función recupera correctamente el estado de juego, verificando mediante ```os.path.exists(ruta)``` que se pued recuperar un estado de juego. Revisa que la primera linea sea un número, es decir que represente la cantidad de tableros, pero se asume que el resto del tablero esta bien construido. Se verifica que el usuario no sea un string vacío para realizar esta acción, sin embargo esto es principalmente para la ejecución de los Test cases, ya que en el menú principal no se permite realizar esta acción (ni guardar_estado) sin crear un usuario y entregar una configuración primero.


## Menú: 25 pts (45,5%)
### ✅ Consola 
El usuario puede interactuar con la consola de manera libre, y sus respuestas y la validez de esta se controlan dentro del codigo correctamente, permitiendo el ingreso solo de parametros correctos. En caso de introducir un parámetro incorrecto, se avisa al usuario y se dice que intente de nuevo, entrando en un bucle hasta conseguir una respuesta válida.

### ✅ Menú de Inicio
Se trata de un bucle que itera sobre si hasta que el usuario indica que quiere salir del juego, o se elige una opción que lleve al usuario al menú de acciones. Se encuentra dentro de el bucle de menú de acciones. Todas las funciones de este menú se ejecutan correctamente, y los parámetros asociados al juego actual, como nombre de usuario, cantidad de tableros resueltos, etc, se van actualizando a mí que el usuario interactúa con el programa.

### ✅ Menú de Acciones
Un bucle que itera sobre sí, permitiendo al usuario acceder a las distintas opciones, y volver al menú de juego. Se accede a él mediante la función main, donde se ejecuta la gran mayoría del programa. 

### ✅ Modularización
EL programa esta modularizado. No se ocupan variables globales. Todos los archivos del programa interactúan entre sí correctamente. Ningún archivo excede las 400 lineas. El archivo más largo tiene una medición de alrededor de 300, debido a que tiene una gran cantidad de comentarios y espacios para facilitar la lectura. La gran mayoría del programa se ejecuta mediante funciones, y dentro de ellas se llaman a bucles y las instancias de clase necesarias. con la extension flake8 verifique que ninguna linea sobrepasa los 100 caracteres, con la mas extensa teniendo 98.

### ✅🟠 PEP8
No sabia si ponerlo en verde o amarillo. Estoy aquí completé todos los ítems de formato PEP8. Sin embargo ocupe Tab en vez de los cuatro espacios, para que el proceso de ejecución no fuera tan tedioso. Dudo de si poner este ítem en amarillo o verde ya que mi tab en VS code está configurado en cuatro espacios, y verifique manualmente que esto fuera asi a lo largo del proceso, pero no se si eso cuenta como seguir exactamente el formato dado por PEP8.


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```data``` en ```T1``` para guardar los estados de usuario


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```guardar_estado(), recuperar_estado() / módulo``` (no debe instalarse)
Uso especificado mas arriba en guardar_estado() y recuperar_estado()
2. ```visualizador```: ```imprimir_tablero()```
Modulo y función dada.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```herramientas```: Contiene a ```mostrar_menu_acciones()```, ```mostrar_menu_juego```, Hecha para imprimir los menus y manejar inputs de usuario mas facilmente. Se importan y usan en main.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Asumo que todos los archivos ```config``` y de tablero son válidos y se encuentran en la carpeta config: Se especifica en el enunciado que podíamos asumir que eran válidos.

2. Asumo que se respeta la restriccion de variable ingresable dada en el enunciado para cada función de clase en DCCasillas y Tablero. Ya que así se ven en el enunciado.

3. Asumo que quien ejecuta y revisa la tarea la esta abriendo desde T1, especificado en el enunciado, y que cuentan con una carpeta data, siendo esta la ruta para guardar los archivos de estado de usuario.

4. Asumo que quien ejecuta y revisa la tarea posee una carpeta de configuraciones, sobre las cuales cada configuración está armada correctamente y es válida, y que los tableros asociados a esta también existen y son válidos, siguiendo el formato propuesto en el enunciado, y con el cual se trabajó en la carpeta dada encontrada en syllabus.

5. Asumo que quien ejecuta y revisa la tarea, lo hace en una versión de Python 3.12.X, con X mayor a 0. Esto porque el visualizador sólo funciona en estas versiones.

6. Asumo que el tablero que se va a entregar para mostrar usando el visualizador esta correctamente construido.

PD: Siempre que corri mi archivo, tanto en la terminal de VS Code como la terminal del computador, lo hice abriendolo desde la carpeta T1, y todos los paths estan armados para que la tarea sea ejecutada desde T1, que es lo que interprete del enunciado.
La librería dada de visualizador siempre arroja el error de que no se ha podido resolver la importación. Esto no afecta en la ejecución del código, y la función imprimir tablero sigue funcionando correctamente.
EL puntaje fue calculado realizando una suma de todas las casillas regulares editables de un tablero en particular al ser resuelto por primera vez, siendo esta suma añadida al puntaje total del usuario. Este puntaje es indiferente de la cantidad de movimientos efectuados sobre el tablero.

La información sobre como usar ```os``` (use ```os.path.exists(path)```)la saque de: https://www.freecodecamp.org/news/how-to-check-if-a-file-exists-in-python/ 
