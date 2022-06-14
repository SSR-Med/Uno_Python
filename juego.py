from Carta import Carta
import random
import time
import os

# Tipo: 1 a 9 es número normal,
# 10: Bloqueo
# 11: Reverse
# 12: Dos cartas más

# Colores:
# Los colores son: amarillo, azul, rojo y verde

# Inicialización del juego. Se crean todas las cartas de la baraja
# Para limpiar la pantalla


def clear(): return os.system('cls')


# Lista de todas las cartas del juego
listaCartas = []
# Las cartas que van sobrando
cartasSobrantes = list()
# Los números
for i in range(1, 13):
    # Los colores
    for elemento in ["Amarillo", "Azul", "Rojo", "Verde"]:
        listaCartas.append(Carta(elemento, i))
        listaCartas.append(Carta(elemento, i))
# Shuffle las cartas
random.shuffle(listaCartas)
# Jugadores
jugadores = {'jugador': list(), 'robot1': list(),
             'robot2': list(), 'robot3': list()}
# Darle cartas a los jugadores
for i in range(8):
    jugadores['jugador'].append(listaCartas.pop())
    jugadores['robot1'].append(listaCartas.pop())
    jugadores['robot2'].append(listaCartas.pop())
    jugadores['robot3'].append(listaCartas.pop())
# Luego de eso se pone una carta de listaCartas en cartasSobrantes, dado que esa será la mesa de juego
cartasSobrantes.append(listaCartas.pop())
# Lista jugadores
listaJugadores = ['jugador', 'robot1', 'robot2', 'robot3']
# Se randomiza la lista, para saber quien es el primero
random.shuffle(listaJugadores)
# Posición será la variable cambiante, encargada de darle el turno a cada persona
posicion = 0
# El sumador puede ser 1 o -1, dependiendo si lo invirtieron o no
sumador = 1
# cantidadCartasComer: la cantidad de cartas a comer
cantidadCartasComer = 0
cartaActual = cartasSobrantes[-1]
'''
Funciones maquina y jugador
'''
# Primera función: Agregar una carta


def agregarCarta(lista):
    if len(listaCartas) == 0:
        listaCartas = cartasSobrantes[:-1]
        random.shuffle(listaCartas)
        cartasSobrantes = cartasSobrantes[-1]
    lista.append(listaCartas.pop())


# Segunda función: Verificar si siquiera puede jugar ese turno. Este es si no tiene una carta para jugar


def checkCartaTurnoRobot(color, tipo, jugadorFuncion):
    global cantidadCartasComer
    if tipo < 10:  # Es un caso diferente tener un número normal a una carta especial
        for elemento in jugadorFuncion:
            if elemento.color == color or elemento.tipo == tipo:
                return elemento  # Si encuentra la carta entonces retorna el elemento
        # Si no encuentra la carta entonces tiene que comer una carta
        agregarCarta(jugadorFuncion)
        if jugadorFuncion[-1].color == color or elemento.tipo == tipo:
            return elemento
    else:
        if tipo == 10:  # En caso de que sea un bloqueo
            for elemento in jugadorFuncion:
                if elemento.tipo == tipo:
                    return elemento
            print("El turno de",
                  listaJugadores[posicion], "ha sido bloqueado")
        elif tipo == 11:  # n caso de que sea un reverse
            for elemento in jugadorFuncion:
                if elemento.color == color or elemento.tipo == tipo:
                    # Si encuentra la carta entonces el sumador no va hacia su ruta natural, sino su contrario
                    sumador = sumador * -1
                    return elemento
            agregarCarta(jugadorFuncion)
            if jugadorFuncion[-1].color == color or elemento.tipo == tipo:
                return elemento
        else:  # En caso de que sea de sumar +2
            for elemento in jugadorFuncion:
                if elemento.tipo == tipo:
                    cantidadCartasComer += 2
                    return elemento
            for i in range(cantidadCartasComer):
                agregarCarta(jugadorFuncion)
            cantidadCartasComer = 0
    return None


'''
Funciones jugador

'''
# Primera función: Saber si el jugador tiene la carta


def checkCartaTurno(color, tipo, jugadorFuncion):
    global cantidadCartasComer
    if tipo < 10:  # Es un caso diferente tener un número normal a una carta especial
        for elemento in jugadorFuncion:
            if elemento.color == color or elemento.tipo == tipo:
                return True  # Si encuentra la carta entonces retorna el elemento
        # Si no encuentra la carta entonces tiene que comer una carta
        agregarCarta(jugadorFuncion)
        if jugadorFuncion[-1].color == color or elemento.tipo == tipo:
            return True
        print("Te has comida una carta, luego la verás en tu baraja")
    else:
        if tipo == 10:  # En caso de que sea un bloqueo
            for elemento in jugadorFuncion:
                if elemento.tipo == tipo:
                    return True
            print("Tu turno ha sido bloqueado")
        elif tipo == 11:  # n caso de que sea un reverse
            for elemento in jugadorFuncion:
                if elemento.color == color or elemento.tipo == tipo:
                    # Si encuentra la carta entonces el sumador no va hacia su ruta natural, sino su contrario
                    sumador = sumador * -1
                    return True
            agregarCarta(jugadorFuncion)
            print("Te has comida una carta, luego la verás en tu baraja")
            if jugadorFuncion[-1].color == color or elemento.tipo == tipo:
                return True
        else:  # En caso de que sea de sumar +2
            for elemento in jugadorFuncion:
                if elemento.tipo == tipo:
                    cantidadCartasComer += 2
                    return True
            for i in range(cantidadCartasComer):
                agregarCarta(jugadorFuncion)
            print("No quiero traer malas noticias, pero te has comido",
                  cantidadCartasComer, "cartas.")
            cantidadCartasComer = 0
    return False


def buscarCarta(color, tipo, jugadorFuncion, colorMesa, tipoMesa):
    global cantidadCartasComer
    for elemento in jugadorFuncion:
        if elemento.color == color or elemento.tipo == tipo:
            if tipo < 10:  # Números normales
                if colorMesa == color or tipoMesa == tipo:
                    cartasSobrantes.append(
                        jugadorFuncion.pop(elemento))
                    return True
            else:
                if tipo == 10:  # En caso de que sea un bloqueo
                    if tipoMesa == tipo:
                        cartasSobrantes.append(
                            jugadorFuncion.pop(elemento))
                        return True
                if tipo == 11:  # En caso de que sea un reverse
                    if tipoMesa == tipo or colorMesa == color:
                        sumador = sumador * -1
                        cartasSobrantes.append(
                            jugadorFuncion.pop(elemento))
                        return True
                else:
                    if tipoMesa == tipo:
                        cantidadCartasComer += 2
                        cartasSobrantes.append(
                            jugadorFuncion.pop(elemento))
                        return True
            return False


'''
Funciones sistema
'''
# Primera función: Sumar posición:


def sumarPosicion(a):
    # Para que no se salga de la lista
    if a > 3:
        return 0
    if a < 0:
        return 3


# Diccionario palabras: Para pasar lo de tipo usuario a tipo real
#"Bloqueo", "Reversa", "+2"
diccionarioTipo = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
                   "7": 7, "8": 8, "9": 9, "Bloqueo": 10, "Reversa": 11, "+2": 12}

while jugadores['jugador'] != 0 and jugadores['robot1'] != 0 and jugadores['robot2'] != 0 and jugadores['robot3'] != 0:
    # Imprimir los jugadores con una carta (Como si fuera uno)
    print("Jugadores con una carta:")
    for elemento in listaJugadores:
        if len(jugadores[elemento]) == 1:
            print(elemento)
    # Para imprimir el turno
    posicionAnterior = posicion + (sumador*-1)
    print("El turno anterior fue de",
          listaJugadores[sumarPosicion(posicion + (sumador*-1))])
    print("El turno actual es de", listaJugadores[posicion])
    print("El turno posterior es de",
          listaJugadores[sumarPosicion(posicion + sumador)])

    # ¿Qué carta está en el tope?
    cartaActual = cartasSobrantes[-1]
    # Imprimir la carta del tope
    print("La carta actual de la mesa es:")
    print("Color:")
    print(cartaActual.color)
    print("Tipo:")
    print(cartaActual.imprimirTipo())
    # En caso de que esté jugando un robot
    if listaJugadores[posicion] != "jugador":
        cartaRobot = checkCartaTurnoRobot(cartaActual.color, cartaActual.tipo,
                                          jugadores[listaJugadores[posicion]])
        if cartaRobot != None:
            cartasSobrantes.append(
                jugadores[listaJugadores[posicion]].pop(cartaRobot))

    else:  # En caso de que esté jugando el jugador
        # Para imprimir las cartas del jugador
        print("Tus cartas actualmente son: ")
        for i in jugadores['jugador']:
            print(str(i+1)+". "+jugadores['jugador'][i].imprimirTodo())
        # Ahora el jugador va a elegir, pero antes el programa verificará si el usuario siquiera puede jugar
        if checkCartaTurno(cartaActual.color, cartaActual.tipo, jugadores['jugador']) == True:
            verdad = True
            while verdad == True:
                #  Los colores son: amarillo, azul, rojo y verde
                print(
                    "Los colores posibles para elegir son: Amarillo, Azul, Rojo y Verde")
                print("¿De qué color es la carta que vas a seleccionar?")
                colorSeleccionar = input()
                while colorSeleccionar not in ["Amarillo", "Azul", "Rojo", "Verde"]:
                    print("Color seleccionado erroneo, por favor elegir otro:")
                    colorSeleccionar = input()
                print(
                    "Los tipos de cartas disponibles son las numericas de 1 a 9 y las de tipo especial(Bloqueo, Reversa, +2)")
                tipoSeleccionar = input(
                    "¿De qué tipo es la carta que vas a seleccionar?")
                while tipoSeleccionar not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "Bloqueo", "Reversa", "+2"]:
                    print("Tipo seleccionado erroneo, por favor elegir otro:")
                    tipoSeleccionar = input()
                # Ya seleccionando vamos a revisar si esa carta está o coincide con la que requerimos
            if buscarCarta(colorSeleccionar, diccionarioTipo[tipoSeleccionar], jugadores['jugador'], cartaActual.color, cartaActual.tipo):
                print(
                    "La carta que se seleccionó va a ser empleada, seguirá el próximo turno")
                verdad = False
            else:
                print("Carta incorrecta, se repetirá el proceso de selección")

        else:
            print(
                "No podrás elegir carta esta vez, tal vez en el próximo turno serás capaz de hacerlo")

    posicion += sumador
    posicion = sumarPosicion(posicion)
    time.sleep(6)
    clear()
for elemento in listaJugadores:
    if len(jugadores[elemento]) == 0:
        print("Felicidades, el ganador es: ", elemento)
        break
