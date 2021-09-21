import random
import navio as nv
import numpy as np

class Servidor_Jogador:
    def __init__(self, mapa):
        self.lista_de_ataques = []
        self.mapa = mapa
        self.lista_de_navios = []
        self.valido = True
        self.lista_acertos = []
        self.orientacao = 0
        self.qntH = 0
        self.qntV = 0
        self.origA = 0

    def criar_navio(self, coordIX, coordIY, orient, tam):
        if int(orient) == 1:
            coordFX = coordIX 
            coordFY = coordIY + tam - 1
        else:
            coordFX = coordIX + tam - 1
            coordFY = coordIY
            
        if self.mapa.validar_coordenadas(coordIX, coordIY, coordFX, coordFY):
            auxX = coordIX
            auxY = coordIY
            for i in range(tam):
                if self.verificar_posicao(auxX, auxY):
                    return False
                if int(orient) == 1:
                    auxY = auxY+ 1
                else: 
                    auxX = auxX + 1
                    
            navio = nv.Navio(coordIX, coordIY, coordFX, coordFY)
            self.lista_de_navios.append(navio)
            return True
        else:
            return False
    
    def atacar(self, coordX, coordY, jogador):
        self.lista_de_ataques.append((coordX, coordY))
        for navio in jogador.lista_de_navios:
            if navio.verificar_dano(coordX, coordY):
                return True
        return False
    
    def verificar_posicao(self, coordX, coordY):
        if len(self.lista_de_navios) > 0:
            for navio in self.lista_de_navios:
                if navio.verificar_existencia(coordX, coordY):
                    return True
        return False

    def verificar_status(self):
        for navio in self.lista_de_navios:
            if navio.vivo:
                return True
        return False

    def verificar_vivos(self):
        qntVivo = 0
        for navio in self.lista_de_navios:
            if navio.vivo:
                qntVivo += 1
        return qntVivo    

    def verificar_mortos(self, jogador):
        aux = 1
        afundados = ""
        for navio in jogador.lista_de_navios:
            if not navio.vivo:
                afundados += str(aux) + " "
            aux = aux + 1
        return afundados

    def atacarNovo(self, coordX, coordY):
        for coord1,coord2 in self.lista_de_ataques:
            if coordX == coord1 and coordY == coord2:
                return False
        return  True
    
    def inicializar_servidor(self):
        count = 5
        while count > 1:
            cordIX  = random.randint(0, 9)
            cordIY = random.randint(0, 9)
            orient = random.randint(1, 2)
            if self.criar_navio(cordIX, cordIY, orient, count):
                count = count - 1
           
        self.print_mapa2()
        return 
    
    def turno_serv(self, j1, j2):
        x = None
        if self.origA != 0:
            self.orientacao = self.origA 
        
        if len(self.lista_acertos) == 0:
            novo = False
            while not novo: 
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                novo = j2.atacarNovo(x,y)
        else:
            tam = len(self.lista_acertos)
            cont = 0 
            while cont < tam:
                c1 = self.lista_acertos[cont][0]
                c2 = self.lista_acertos[cont][1]
                if c1 - 1 < 0 and self.qntH == 2 and self.origA == 0:
                    self.orientacao = 2
                    self.qntH = 0

                if self.orientacao == 0 or self.orientacao == 1:
                    self.orientacao = 1
                
                    if not any(((c1 + 1),c2) == (co1, co2) for co1,co2 in self.lista_de_ataques) and c1 + 1 < self.mapa.eixoX:
                        x = c1 + 1
                        y = c2
                        cont = tam
                        self.qntH = 1
                    elif not any(((c1 - 1),c2) == (co1, co2) for co1,co2 in self.lista_de_ataques) and c1 - 1 >= 0:
                        x = c1 - 1
                        y = c2
                        cont = tam
                    if x == None and self.origA == 0:
                        self.orientacao = 2
                if self.orientacao == 2:
                    self.orientacao = 2
                    if not any((c1, ( c2+  1)) == (co1, co2) for co1,co2 in self.lista_de_ataques) and c2 + 1 < self.mapa.eixoY:
                        x = c1 
                        y = c2 + 1
                        cont = tam
                        self.qntV = 1
                    elif not any((c1, ( c2-  1)) == (co1, co2) for co1,co2 in self.lista_de_ataques) and c2 - 1 >=0:
                        x = c1
                        y = c2 - 1
                        cont = tam


                cont = cont + 1
            #olhar vizinho
        print("Servidor atacou posição: ", chr(x+65), y)
        qntVivos = j1.verificar_vivos()    
        resp = j2.atacar(x, y, j1)
        qntVivos2 = j1.verificar_vivos()  
        if resp:
            print("Servidor acertou um navio!!")
            self.lista_acertos.append((x, y))
            self.origA = self.orientacao
        else:
            print("Servidor tiro no mar!!") 
            if self.orientacao == 1 and self.qntH == 2:
                self.orientacao = 2
                self.qntH = 0
            elif self.orientacao == 1 and self.qntH == 1:
                self.qntH = 2

        if qntVivos != qntVivos2:
            lista_m = j1.getMortos()
            for c1,c2 in lista_m:
                self.lista_acertos = list(filter(((c1,c2)).__ne__,self.lista_acertos))
            #self.lista_acertos.clear()
            self.orientacao = 0
            self.qntH = 0
            self.qntV = 0 
            self.origA = 0
        
        return chr(x+65) + str(y)
        
    def print_mapa(self, ataques):
        matriz = []

        for _ in range(self.mapa.eixoX+1):
            matriz.append( [" "] * (self.mapa.eixoY+1) )
            
        for i in range(self.mapa.eixoX):
            matriz[i+1][0] = chr(i+65)
        
        for j in range(self.mapa.eixoY):
            matriz[0][j+1] = str(j) 
            
                    

        matriz[0][0] = " "    
        for co1,co2 in ataques:    
            matriz[co1+1][co2+1] = "X" 
        
        for navio in self.lista_de_navios:
            for co1,co2 in navio.lista_posicoes:
                if matriz[co1+1][co2+1] == "X":
                    if navio.vivo:
                        matriz[co1+1][co2+1] = "a"
                    else:
                        matriz[co1+1][co2+1] = "@"
                else:
                    matriz[co1+1][co2+1] = "o"
        print("Mapa Servidor")
        for i in range(self.mapa.eixoX+1):
            for j in range(self.mapa.eixoY+1):      
                print( matriz[i][j], "|", end = "")   
            
            print(" ")
        '''
        for i in self.mapa.eixoX:
            for j in self.mapa.eixoY:
                if i == 0:
                    printM += chr(j+65) + "|"
                if 
                    printM +=
            printM += "\n"
        '''
    
    def print_mapa2(self):
        matriz = []

        for _ in range(self.mapa.eixoX+1):
            matriz.append( [" "] * (self.mapa.eixoY+1) )
            
        for i in range(self.mapa.eixoX):
            matriz[i+1][0] = chr(i+65)
        
        for j in range(self.mapa.eixoY):
            matriz[0][j+1] = str(j) 
            
         
        for navio in self.lista_de_navios:
            for co1,co2 in navio.lista_posicoes:
                if matriz[co1+1][co2+1] == "X":
                    if navio.vivo:
                        matriz[co1+1][co2+1] = "a"
                    else:
                        matriz[co1+1][co2+1] = "@"
                else:
                    matriz[co1+1][co2+1] = "o"
        print("Tabuleiro Servidor")
        for i in range(self.mapa.eixoX+1):
            for j in range(self.mapa.eixoY+1):      
                print( matriz[i][j], "|", end = "")   
            
            print(" ")