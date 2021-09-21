import mapa as mp
import navio as nv
import socket
import sys
import os

class Cliente_TCP:
    def __init__(self, mapa):
        self.lista_de_ataques = []
        self.mapa = mapa
        self.lista_de_navios = []
        self.valido = True
        self.pos = ["n1", "n2", "n3", "n4"]
        self.lista_ataque_recebido = []
        self.lista_acertos = []
        self.mortosAtual = ''


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
        
    def verificar_posicao(self, coordX, coordY):
        if len(self.lista_de_navios) > 0:
            for navio in self.lista_de_navios:
                if navio.verificar_existencia(coordX, coordY):
                    return True
        return False

    def inicializar_cliente(self):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        nomeArq = os.path.join(THIS_FOLDER, 'frotaC.txt')
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
    
    def atacado(self, coordX, coordY):
        self.lista_ataque_recebido.append((coordX, coordY))
        for navio in self.lista_de_navios:
            if navio.verificar_dano(coordX, coordY):
                return True
        return False

    def print_mapaCliente(self):
        matriz = []

        for _ in range(self.mapa.eixoX+1):
            matriz.append( [" "] * (self.mapa.eixoY+1) )
            
        for i in range(self.mapa.eixoX):
            matriz[i+1][0] = chr(i+65)
        
        for j in range(self.mapa.eixoY):
            matriz[0][j+1] = str(j) 
        
        matriz[0][0] = " "    
        for co1,co2 in self.lista_ataque_recebido:    
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
    
    def print_mapaServidor(self):
        matriz = []

        for _ in range(self.mapa.eixoX+1):
            matriz.append( [" "] * (self.mapa.eixoY+1) )
            
        for i in range(self.mapa.eixoX):
            matriz[i+1][0] = chr(i+65)
        
        for j in range(self.mapa.eixoY):
            matriz[0][j+1] = str(j) 
         
        matriz[0][0] = " "    
        for co1,co2 in self.lista_de_ataques:    
            matriz[co1+1][co2+1] = "X" 
        
        for co1,co2 in self.lista_acertos:
             matriz[co1+1][co2+1] = "O"
         
        print("Mapa Servidor")
        for i in range(self.mapa.eixoX+1):
            for j in range(self.mapa.eixoY+1):      
                print( matriz[i][j], "|", end = "")   
            
            print(" ")

        print ("Navios inimigos já afundados: ", end="")
        print(self.mortosAtual)


    def turno_cliente(self):
        
        x = "123"
        continuar = True
        while continuar:
            x = input("Vertical(letra):")
            if x.isalpha() and len(x) == 1 and (ord(x.upper()) >= 65 and ord(x.upper()) <= 74):
                continuar = False
            elif x.upper() == 'P':
                self.print_mapaCliente()
                self.print_mapaServidor()
            elif x.upper() == 'Q':
                return "quit"
        #x =  ord(x.upper()) - 65

        continuar = True
        y = "lixo"
        while continuar:
            y = input("Horizontal(número):")
            if y.isnumeric() and len(y) == 1:
                continuar = False
        #y = int(y)
        self.lista_de_ataques.append(( ord(x.upper()) - 65,int(y)))
        return x.upper() + y
        '''
        resp = j1.atacar(x, y, j2)
        if resp:
            print("Cliente acertou um navio!!")
        else:
            print("Cliente tiro no mar!!")
        return'''
    def jogar(self, msg):
        s.sendall(bytes(msg.encode()))
        dataR = s.recv(1024)
        print ("Servidor responde:" , str(dataR.decode()))
        self.print_mapaCliente()
        while msg != "\x18":			
            
            msg = j1.turno_cliente() #input('Digite uma mensagem:\n')
            if msg == "quit":
                print("Jogo terminado pelo cliente")
                break
            s.sendall(bytes(msg.encode()))
            
            dataR = s.recv(1024)
            respS = str(dataR.decode())
            if respS[0] == 'A':
                self.lista_acertos.append((ord(msg[0])-65, int(msg[1])))
                print ("Servidor responde: Acertou um navio. Ataque:" , respS[1], respS[2])
            else:
                print ("Servidor responde: Tiro no mar. Ataque:" , respS[1], respS[2])
            self.atacado(ord(respS[1])-65, int(respS[2]))
            #self.lista_ataque_recebido.append(( ))
            if respS[3:] == "Cliente venceu!!" or respS[3:] == "Servidor venceu!!":
                self.mortosAtual = '1 2 3 4'
                print('------------Fim de jogo-----------')
                print(respS[3:])
                self.print_mapaCliente()
                self.print_mapaServidor()
                break
            mortosNovo = respS[3:len(respS)]
            if len(self.mortosAtual) != len(mortosNovo):
                self.mortosAtual = mortosNovo
                print ("Navios inimigos já afundados: ", end="")
                print(self.mortosAtual)
            
        print('closing connection bye...')
        s.close()  
        return   
if __name__ == "__main__":
    #for arg in sys.argv[1:]:
        #print (arg)
    
    #print(sys.argv[1])
    #print(sys.argv[2])
    host = sys.argv[1] #ip/nome
    port = int(sys.argv[2]) #porta

    # Cria um socket TCP/IP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    #Os dados são enviados com a função sendall() e, recebidos com a função recv().
    j1 = Cliente_TCP(mp.Mapa(10,10)) 
    j1.inicializar_cliente()
    if j1.valido:   
        msg = input('Digite S para começar a batalha naval\n')
        if msg.upper() == 'S':
            j1.jogar(msg)
        else:
            msg = "quit"
            s.sendall(bytes(msg.encode()))
            print('Jogo não iniciado...')
            s.close() 