class Mapa:
    def __init__(self, eixoX, eixoY):
        self.eixoX = eixoX
        self.eixoY = eixoY

    def validar_coordenada(self, coordX, coordY):
        if coordX >= 0 and coordX < self.eixoX and coordY >= 0 and \
                coordY < self.eixoY:
            return True
        else:
            return False

    def validar_coordenadas(self, coordIX, coordIY,  coordFX, coordFY):
        if self.validar_coordenada(coordIX, coordIY) and \
                self.validar_coordenada(coordFX, coordFY):
            return True
        else:
            return False
