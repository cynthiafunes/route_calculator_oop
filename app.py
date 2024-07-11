import heapq

BLANCO, ROJO, VERDE, AZUL, AMARILLO = "\033[47m  \033[m", "\033[41m  \033[m", "\033[42m  \033[m", "\033[44m  \033[m", "\033[43m  \033[m"
DIRECCIONES = [(0, 1), (0, -1), (1, 0), (-1, 0)]

class Nodo:
    def __init__(self, posicion, g=0, h=0, padre=None):
        self.posicion = posicion
        self.g = g
        self.h = h
        self.f = g + h
        self.padre = padre

    def __lt__(self, other):
        return self.f < other.f

class Mapa:
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.tablero = [[BLANCO for _ in range(tamaño)] for _ in range(tamaño)]
        self.inicio = None
        self.fin = None

    def agregar_obstaculo(self, x, y):
        if self.es_valido(x, y) and self.tablero[x][y] == BLANCO and (x, y) not in [self.inicio, self.fin]:
            self.tablero[x][y] = ROJO
        else:
            print("No se puede agregar un obstáculo en esa posición.")

    def quitar_obstaculo(self, x, y):
        if self.es_valido(x, y) and self.tablero[x][y] == ROJO:
            self.tablero[x][y] = BLANCO
        else:
            print("No se puede quitar un obstáculo de esa posición.")

    def es_accesible(self, x, y):
        return self.es_valido(x, y) and self.tablero[x][y] != ROJO

    def es_valido(self, x, y):
        return 0 <= x < self.tamaño and 0 <= y < self.tamaño

    def establecer_punto(self, tipo, mensaje):
        while True:
            try:
                x = int(input(f"Introduce la coordenada X, {mensaje}"))
                y = int(input(f"Introduce la coordenada Y, {mensaje}"))
                if self.es_valido(x, y):
                    if tipo == 'inicio':
                        self.inicio = (x, y)
                    elif tipo == 'fin':
                        self.fin = (x, y)
                    break
                else:
                    print("Coordenadas no válidas. Intenta de nuevo.")
            except ValueError:
                print("Entrada inválida. Introduce números enteros.")

    def imprimir(self, camino=None):
        for fila in range(self.tamaño):
            for columna in range(self.tamaño):
                if (fila, columna) == self.inicio:
                    print(VERDE, end='')
                elif (fila, columna) == self.fin:
                    print(AZUL, end='')
                elif camino and (fila, columna) in camino:
                    print(AMARILLO, end='')
                else:
                    print(self.tablero[fila][columna], end='')
            print()

    def gestionar_obstaculos(self):
        while True:
            accion = input("Escribe 'listo' para terminar, 'a' para añadir un obstáculo, o 'q' para quitar un obstáculo: ")
            if accion == 'listo':
                break
            try:
                x = int(input("Introduce la coordenada X del obstáculo: "))
                y = int(input("Introduce la coordenada Y del obstáculo: "))
                if accion == 'a':
                    self.agregar_obstaculo(x, y)
                elif accion == 'q':
                    self.quitar_obstaculo(x, y)
                self.imprimir()
            except ValueError:
                print("Entrada inválida. Introduce números enteros.")

class CalculadoraRutas:
    def __init__(self, mapa):
        self.mapa = mapa

    def distancia_manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def encontrar_ruta(self):
        inicio = self.mapa.inicio
        fin = self.mapa.fin
        if not inicio or not fin:
            return None

        lista_abierta = []
        heapq.heappush(lista_abierta, Nodo(inicio, 0, self.distancia_manhattan(inicio, fin)))
        lista_cerrada = set()
        nodos_abiertos = {inicio: 0}

        while lista_abierta:
            nodo_actual = heapq.heappop(lista_abierta)
            lista_cerrada.add(nodo_actual.posicion)

            if nodo_actual.posicion == fin:
                camino = []
                while nodo_actual:
                    camino.append(nodo_actual.posicion)
                    nodo_actual = nodo_actual.padre
                return camino[::-1]

            for direccion in DIRECCIONES:
                posicion_vecina = (nodo_actual.posicion[0] + direccion[0], nodo_actual.posicion[1] + direccion[1])

                if self.mapa.es_accesible(posicion_vecina[0], posicion_vecina[1]) and posicion_vecina not in lista_cerrada:
                    g_nuevo = nodo_actual.g + 1
                    if posicion_vecina not in nodos_abiertos or g_nuevo < nodos_abiertos[posicion_vecina]:
                        nodo_vecino = Nodo(posicion_vecina, g_nuevo, self.distancia_manhattan(posicion_vecina, fin), nodo_actual)
                        heapq.heappush(lista_abierta, nodo_vecino)
                        nodos_abiertos[posicion_vecina] = g_nuevo
        return None

def main():
    tamaño_tablero = 5
    mapa = Mapa(tamaño_tablero)

    mapa.establecer_punto('inicio', "para el punto de inicio: ")
    mapa.imprimir()

    mapa.establecer_punto('fin', "para el punto final: ")
    mapa.imprimir()

    mapa.gestionar_obstaculos()

    calculadora = CalculadoraRutas(mapa)
    camino = calculadora.encontrar_ruta()

    if camino:
        print("Camino encontrado:")
        mapa.imprimir(camino)
    else:
        print("No se encontró un camino.")

main()
