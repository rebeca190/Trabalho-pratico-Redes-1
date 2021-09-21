import navio as nv

class Cliente_Jogador:
    def __init__(self, mapa):
        self.lista_de_ataques = []
        self.mapa = mapa
        self.lista_de_navios = []
        self.valido = True
        self.pos = ["n1", "n2", "n3", "n4"]
        

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
    
    def getMortos(self):
        lista_m = []
        for navio in self.lista_de_navios:
            if not navio.vivo:
                lista_m = lista_m + navio.lista_posicoes
        return lista_m 

    def inicializar_cliente(self, nomeArq):
        f = open(nomeArq, 'r')
        self.pos[0] = f.readline()
        self.pos[1]= f.readline()
        self.pos[2] = f.readline()
        self.pos[3] = f.readline()
        f.close()
        count = 5
        for i in range(4):
            texto = self.pos[i].split()
            coords = texto[0]
            orient = texto[1]
            if len(coords) != 2:
                self.valido = False
                return self.valido
            if coords[0].isnumeric():
                cordIX  = ord(coords[1].upper()) - 65
                cordIY =  int(coords[0])
                
            else:
                cordIX  =  ord(coords[0].upper()) - 65
                cordIY =  int(coords[1])
                
            if self.criar_navio(cordIX, cordIY, orient, count):
                print("Navio ", i+1, " criado")
                count = count - 1
            else:
                self.valido = False
                print("Falha ao cria navio numero" , i+1 )
       
        return 

    '''
    def atacarNovo(self, coordX, coordY):
        for coord1,coord2 in self.lista_de_ataques:
            if coordX == coord1 and coordY == coord2:
                return False
        return  True

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
        print("Mapa Cliente")
        for i in range(self.mapa.eixoX+1):
            for j in range(self.mapa.eixoY+1):      
                print( matriz[i][j], "|", end = "")   
            
            print(" ")
    
    def turno_cliente(self, j1, j2):
        
        x = "123"
        continuar = True
        while continuar:
            x = input("Vertical(letra):")
            if x.isalpha() and len(x) == 1 and (ord(x.upper()) >= 65 and ord(x.upper()) <= 74):
                continuar = False
            elif x.upper() == 'P':
                j1.print_mapa(j2.lista_de_ataques)
                j2.print_mapa(j1.lista_de_ataques)
        x =  ord(x.upper()) - 65

        continuar = True
        y = "lixo"
        while continuar:
            y = input("Horizontal(número):")
            if y.isnumeric() and len(y) == 1:
                continuar = False
        y = int(y)
        
        resp = j1.atacar(x, y, j2)
        if resp:
            print("Cliente acertou um navio!!")
        else:
            print("Cliente tiro no mar!!")
        return'''