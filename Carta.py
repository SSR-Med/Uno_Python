class Carta:
    def __init__(self, color, tipo):
        # Tipo: 1 a 9 es número normal,
        # 10: Bloqueo
        # 11: Reverse
        # 12: Dos cartas más

        # Colores:
        # Los colores son: amarillo, azul, rojo y verde
        self.color = color
        self.tipo = tipo

    def imprimirTipo(self):
        if self.tipo < 10:
            return str(self.tipo)
        elif self.tipo == 10:
            return "Bloqueo"
        elif self.tipo == 11:
            return "Reversa"
        else:
            return "+2"

    def imprimirTodo(self):
        return "Color: " + self.color + " Tipo: "+self.imprimirTipo()
