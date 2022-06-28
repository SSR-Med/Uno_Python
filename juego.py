import random
import os
import time
def clear(): return os.system("cls")


# Creación de la baraja: Se escoge una lista como estructura de datos para
# alojar las cartas, puesto que el juego tiene cartas repetidas que no se
# identifican en un set(). Cada carta lleva un identificador según su color:
# Az para azul, Ro para rojo, Ve para verde y Am para amarillo. Además, los
# números 10, 11, 12 hacen referencia a las cartas especiales reversa, bloqueo y +2
# correspondientemente.
cartas = ['01Am', '01Az', '01Ro', '01Ve', '02Am', '02Az', '02Ro', '02Ve', '03Am', '03Az', '03Ro',
          '03Ve', '04Am', '04Az', '04Ro', '04Ve', '05Am', '05Az', '05Ro', '05Ve', '06Am', '06Az',
          '06Ro', '06Ve', '07Am', '07Az', '07Ro', '07Ve', '08Am', '08Az', '08Ro', '08Ve', '09Am', '09Az',
          '09Ro', '09Ve', '10Am', '10Az', '10Ro', '10Ve', '11Am', '11Az', '11Ro', '11Ve', '12Am',
          '12Az', '12Ro', '12Ve', '01Am', '01Az', '01Ro', '01Ve', '02Am', '02Az', '02Ro', '02Ve', '03Am',
          '03Az', '03Ro', '03Ve', '04Am', '04Az', '04Ro', '04Ve', '05Am', '05Az', '05Ro', '05Ve', '06Am',
          '06Az', '06Ro', '06Ve', '07Am', '07Az', '07Ro', '07Ve', '08Am', '08Az', '08Ro', '08Ve', '09Am',
          '09Az', '09Ro', '09Ve', '10Am', '10Az', '10Ro', '10Ve', '11Am', '11Az', '11Ro', '11Ve', '12Am', '12Az', '12Ro', '12Ve']
# Se revuelve la baraja antes de repartirla
random.shuffle(cartas)

# Creacion de los jugadores: Se escoge ingresar las cartas de cada jugador en
# diccionarios porque es necesario hacer varias operaciones de búsqueda y estas
# son mas eficientes en un diccionario que en una lista. El problema de las
# cartas repetidas se solucionó usando dos claves para cada color.
humano = {'Amarillo1': set(), 'Azul1': set(), 'Rojo1': set(), 'Verde1': set(),
          'Amarillo2': set(), 'Azul2': set(), 'Rojo2': set(), 'Verde2': set()}
maquina1 = {'Amarillo1': set(), 'Azul1': set(), 'Rojo1': set(), 'Verde1': set(),
            'Amarillo2': set(), 'Azul2': set(), 'Rojo2': set(), 'Verde2': set()}
maquina2 = {'Amarillo1': set(), 'Azul1': set(), 'Rojo1': set(), 'Verde1': set(),
            'Amarillo2': set(), 'Azul2': set(), 'Rojo2': set(), 'Verde2': set()}
maquina3 = {'Amarillo1': set(), 'Azul1': set(), 'Rojo1': set(), 'Verde1': set(),
            'Amarillo2': set(), 'Azul2': set(), 'Rojo2': set(), 'Verde2': set()}

# El primer jugador se escoge al azar y se comienza a jugar en sentido horario
turno = random.randint(0, 3)
orientacion = 1
sumaGolosa = 2

# Se crea lista jugadores para poder manipular los diccionarios de arriba con
# mayor facilidad
jugadores = [humano, maquina1, maquina2, maquina3]

# cartaEspecial es para revisar si el efecto de la carta especial que está en la mesa todavia perdura
cartaEspecial = False


# La funcion agregarCarta identifica si al momento de repartir el jugador
# ya posee esa carta y la agrega a la segunda clave del mismo color


def agregarCarta(jugador, carta):
    colorCarta = carta[-2:]
    if colorCarta == 'Am':
        if carta not in jugador['Amarillo1']:
            jugador['Amarillo1'].add(carta)
        else:
            jugador['Amarillo2'].add(carta)
    elif colorCarta == 'Az':
        if carta not in jugador['Azul1']:
            jugador['Azul1'].add(carta)
        else:
            jugador['Azul2'].add(carta)
    elif colorCarta == 'Ro':
        if carta not in jugador['Rojo1']:
            jugador['Rojo1'].add(carta)
        else:
            jugador['Rojo2'].add(carta)
    else:
        if carta not in jugador['Verde1']:
            jugador['Verde1'].add(carta)
        else:
            jugador['Verde2'].add(carta)


# Asignación inicial de cartas
for i in range(8):
    for jugador in jugadores:
        carta = cartas.pop()
        agregarCarta(jugador, carta)

# Las cartas restantes se convierten en la pila de arrastre. Además se crea la
# pila de descarte, donde van las cartas jugadas
descarte = [cartas.pop()]


# La función tieneCartas identifica si un jugador tiene cartas para jugar o si
# ya ganó
def tieneCartas(jugador):
    for conjunto in jugador:
        if len(jugador[conjunto]) != 0:
            return True
    return False

# En caso de que la pila de arrastre quede vacía, se reordena la pila de descarte
# y esta se usa como nueva pila de arrastre, para lo anterior se usa la funcion
# reiniciarCartas


def reiniciarCartas():
    global descarte
    cartas = descarte.copy()
    random.shuffle(cartas)
    descarte = [cartas.pop()]

# La funcion revisarBaraja revisa que haya la cantidad suficiente de cartas para
# arrastrar en la lista cartas, de lo contrario reinicia la baraja con la pila de
# descarte


def revisarBaraja(numCartas):
    if len(cartas) >= numCartas:
        return True
    return reiniciarCartas()

# La funcion verificarNumero identifica si la maquina que tiene turno posee un numero igual
# al de la pila de descarte


def verificarNumero(jugador):
    numero = descarte[-1][:2]
    if str(numero)+"Az" in jugador["Azul1"]:
        jugador['Azul1'].remove(str(numero)+"Az")
        return str(numero)+"Az"
    if str(numero)+"Az" in jugador['Azul2']:
        jugador['Azul2'].remove(str(numero)+"Az")
        return str(numero)+"Az"
    # Verde:
    if str(numero)+"Ve" in jugador['Verde1']:
        jugador['Verde1'].remove(str(numero)+"Ve")
        return str(numero)+"Ve"
    if str(numero)+"Ve" in jugador['Verde2']:
        jugador['Verde2'].remove(str(numero)+"Ve")
        return str(numero)+"Ve"
    # Amarillo
    if str(numero)+"Am" in jugador['Amarillo1']:
        jugador['Amarillo1'].remove(str(numero)+"Am")
        return str(numero)+"Am"
    if str(numero)+"Am" in jugador['Amarillo2']:
        jugador['Amarillo2'].remove(str(numero)+"Am")
        return str(numero)+"Am"
    # Rojo
    if str(numero)+"Ro" in jugador['Rojo1']:
        jugador['Rojo1'].remove(str(numero)+"Ro")
        return str(numero)+"Ro"
    if str(numero)+"Ro" in jugador['Rojo2']:
        jugador['Rojo2'].remove(str(numero)+"Ro")
        return str(numero)+"Ro"
    return False

# La funcion verificarBot identifica si la maquina que tiene turno posee al menos
# una carta que pueda lanzar a la pila de descarte y la elimina en caso de ser verdad


def verificarBot(jugador):
    jugada = verificarNumero(jugador)
    if jugada == False:
        color = descarte[-1][-2:]
        # verifica si hay una carta del mismo color y la elimina si la encuentra
        if color == "Am":
            if len(jugador['Amarillo1']) != 0:
                return jugador['Amarillo1'].pop()
            elif len(jugador['Amarillo2']) != 0:
                return jugador['Amarillo2'].pop()
        elif color == "Az":
            if len(jugador['Azul1']) != 0:
                return jugador['Azul1'].pop()
            elif len(jugador['Azul2']) != 0:
                return jugador['Azul2'].pop()
        elif color == "Ve":
            if len(jugador['Verde1']) != 0:
                return jugador['Verde1'].pop()
            elif len(jugador['Verde2']) != 0:
                return jugador['Verde2'].pop()
        elif color == "Ro":
            if len(jugador['Rojo1']) != 0:
                return jugador['Rojo1'].pop()
            elif len(jugador['Rojo2']) != 0:
                return jugador['Rojo2'].pop()
    return jugada

# La funcion verificarHumano rectifica que la carta seleccionada
# por el jugador si pueda ser lanzada a la pila de descarte y de ser cierto la elimina


def verificarHumano(carta):
    numero = descarte[-1][:2]
    color = descarte[-1][-2:]
    if carta[:2] == numero or carta[-2:] == color:
        for conjunto in humano:
            if carta in humano[conjunto]:
                humano[conjunto].remove(carta)
                return carta
    return False
# En caso de que sea un +2


def verificarHumanoEspecial(carta):
    if carta[:2] == '12':
        for conjunto in humano:
            if carta in humano[conjunto]:
                humano[conjunto].remove(carta)
                return carta
    return False

# La funcion siguiente sirve para identificar dependiendo de la carta
# que aparezca en la pila de descarte, de quien es el próximo turno (retorna un indice)


def siguiente(indJugadorAnterior):
    global cartaEspecial
    global orientacion
    # si la ultima carta es un 11, esto corresponde a la carta de reversa
    # entonces la orientacion en la que se esta jugando cambia
    if int(descarte[-1][:2]) == 11 and cartaEspecial == True:
        orientacion = orientacion * -1
        cartaEspecial = False
        return (indJugadorAnterior + orientacion) % len(jugadores)
    # si la ultima carta es un 11, esto corresponde a la carta de bloqueo
    # entonces el siguiente indice no puede jugar
    if int(descarte[-1][:2]) == 10 and cartaEspecial == True:
        cartaEspecial = False
        return (indJugadorAnterior + 2)*orientacion % len(jugadores)
    else:
        # si la ultima carta de la pila de descarte tiene numero hasta el 9
        # el turno no se ve afectado
        return (indJugadorAnterior + orientacion) % len(jugadores)

# La funcion jugarBot busca de quien es el turno y llama las funciones
# segun corresponda


def jugarBot(jugador):
    global sumaGolosa
    global cartaEspecial
    # si la carta en descarte es menor a diez, se juega normal
    if int(descarte[-1][:2]) <= 11 or cartaEspecial == False:
        # verifica si la maquina tiene una carta que le sirva
        jugada = verificarBot(jugador)
        # si la jugada no arroja un False quiere decir que encontro una carta
        # esta carta se agrega a la pila de descarte
        if jugada != False:
            if 13 > int(jugada[:2]) > 9:
                cartaEspecial = True
            descarte.append(jugada)
            return jugada
        # si la jugada no encuentra una carta, se arrastra una carta de la baraja
        else:
            revisarBaraja(1)
            carta = cartas.pop()
            agregarCarta(jugador, carta)
            # luego se revisa nuevamente si la carta puede agregarse a la pila de descarte
            jugada = verificarBot(jugador)
            if jugada != False:
                descarte.append(jugada)
                return jugada
    # si la carta en descarte es un 12 (es decir un +2) el bot solo puede lanzar si tiene otro +2
    # de lo contrario debe arrastrar lo que se encuentre en la variable sumaGolosa
    if int(descarte[-1][:2]) == 12 and cartaEspecial == True:
        jugada = verificarNumero(jugador)
        if jugada != False:
            descarte.append(jugada)
            sumaGolosa = sumaGolosa + 2
            return jugada
        else:
            # Revisa si la cantidad a arrastrar es suficiente para la lista de cartas
            revisarBaraja(sumaGolosa)
            cartaEspecial = False
            print(
                "Al pobre le ha tocado comer +{suma} cartas".format(suma=sumaGolosa))
            for i in range(sumaGolosa):
                carta = cartas.pop()
                agregarCarta(jugador, carta)
            sumaGolosa = 2
    return False
# Función para mostrar la baraja


def imprimirBaraja():
    barajaHumano = ""
    for conjunto in humano:
        for e in humano[conjunto]:
            barajaHumano = barajaHumano + " " + e
    print("Tus cartas actualmente son: ", barajaHumano, sep="\n")


# Lista para imprimir facilmente de quién es el turno
stringTurno = ['Humano', 'Maquina1', 'Maquina2', 'Maquina3']

# Lo que se ejecuta hasta que haya un ganador
verdadJuego = True
while verdadJuego == True:
    jugador = jugadores[turno]
    print("El turno actual es de %s" % stringTurno[turno])
    print("La carta actual en la mesa es: %s" % descarte[-1])
    # Si el turno es de las maquinas
    if turno != 0:
        # Para ver si el bot agregó una carta
        verdadBot = jugarBot(jugador)
        if verdadBot != False:
            print("La carta introducida por {jugador} es: {carta}".format(
                jugador=stringTurno[turno], carta=verdadBot))
        else:
            print("El jugador {jugador} no introdujo carta alguna".format(
                jugador=stringTurno[turno]))
        if tieneCartas(jugador):
            turno = siguiente(turno)
            continue
        else:
            print("El ganador es %s" % stringTurno[turno])
            verdadJuego = False
            continue
    # Si el turno es del humano
    else:
        imprimirBaraja()
        verdadHumano = True
        # El contadorArrastre es para que el jugador no pueda arrastrar más de una vez
        contadorArrastre = 0
        while verdadHumano == True:
            if int(descarte[-1][:2]) != 12 or cartaEspecial == False:
                if contadorArrastre == 0:
                    print("¿Deseas lanzar una carta (L) o arrastrar (A)?")
                else:
                    imprimirBaraja()
                    print("¿Deseas lanzar una carta (L) o pasar turno (T)?")
                decision = input()
                if decision == "L":
                    print(
                        "¿Qué carta quieres lanzar? (las cartas 10, 11, 12 hacen referencia a bloqueo, reversa y +2, respectivamente)")
                    carta = input()
                    jugada = verificarHumano(carta)
                    if jugada == False:
                        print(
                            "Hay un error de sintaxis o aun no puedes poner esa carta")
                        continue
                    else:
                        descarte.append(jugada)
                        if int(jugada[:2]) == 11 or int(jugada[:2]) == 10:
                            cartaEspecial = True
                        if int(jugada[:2]) == 12:
                            cartaEspecial = True
                        if tieneCartas(jugador):
                            turno = siguiente(turno)
                            verdadHumano = False
                            continue
                        else:
                            verdadHumano = False
                            verdadJuego = False
                            continue
                elif decision == "A" and contadorArrastre == 0:
                    contadorArrastre += 1
                    cartaArrastrar = cartas.pop()
                    revisarBaraja(1)
                    agregarCarta(jugador, cartaArrastrar)
                    # En caso de que sea arrastre
                    pass
                elif decision == "T" and contadorArrastre == 1:
                    turno = siguiente(turno)
                    verdadHumano = False
                else:
                    print("Error de sintaxis, por favor elija una opción posible")
                    continue
            elif int(descarte[-1][:2]) == 12 and cartaEspecial == True:
                print("Hay un +2. ¿Quieres aceptar el +2 (A) o poner un +2 (L)?")
                decision = input()
                if decision == "A":
                    print("Debes arrastrar %d cartas" % sumaGolosa)
                    revisarBaraja(sumaGolosa)
                    for i in range(sumaGolosa):
                        carta = cartas.pop()
                        agregarCarta(jugador, carta)
                    sumaGolosa = 2
                    cartaEspecial = False
                elif decision == "L":
                    print(
                        "¿Qué carta quieres lanzar? (las cartas 10, 11, 12 hacen referencia a bloqueo, reversa y +2, respectivamente)")
                    carta = input()
                    jugada = verificarHumanoEspecial(carta)
                    if jugada == False:
                        print(
                            "Hay un error de sintaxis o aun no puedes poner esa carta")
                        continue
                    else:
                        cartaEspecial = True
                        descarte.append(jugada)
                        sumaGolosa = sumaGolosa + 2

                turno = siguiente(turno)
                verdadHumano = False
        if tieneCartas(jugador) == False:
            print("Eres el ganador")
            verdadJuego = False
        time.sleep(6)
        clear()
