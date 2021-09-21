import cliente as c
import servidor as s
import os
import socket
import sys
import mapa as mp

class Servidor_TCP:

    def __init__(self, porta):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER, 'frotaC.txt')
        # Significa que é possível receber conexões fora da rede local
        self.host = ''
        self.port = porta
        self.mapa = mp.Mapa(10, 10)
        self.arq = my_file
    
    def verificar_status(self, j1, j2):
        return j1.verificar_status() and j2.verificar_status()

    def jogar(self):
        
        print("Tabuleiro Cliente")
        j1 = c.Cliente_Jogador(self.mapa)
        j1.inicializar_cliente(self.arq)
        if j1.valido == False:
            print("Tabuleiro não válido")
            return "quit"
        j2 = s.Servidor_Jogador(self.mapa)
        j2.inicializar_servidor()
        print("Tabuleiros Criados")
        reply = "Tabuleiros Criados"
        self.conn.sendall(bytes(reply.encode()))
        while self.verificar_status(j1, j2):
            
            data = self.conn.recv(1024)
            msgR = str(data.decode())
            if not msgR:
                print('QUIT')
                return "quit"
            x =  ord(msgR[0].upper()) - 65
            y = int(msgR[1])
            #print("cliente")
            resp = j1.atacar(x, y, j2)
            if resp:
                print("Cliente acertou um navio!!")
                msgF = "A"
            else:
                print("Cliente tiro no mar!!")
                msgF = "E"
            
            mortos = j1.verificar_mortos(j2)
            if mortos != "":
                print("Navios afundados C: ", mortos)
            
                #print("Cliente venceu!!")
            
                #j2.print_mapa(j1.lista_de_ataques)
                #print("servidor")
            ataque = j2.turno_serv(j1, j2)
            mortos2 = j2.verificar_mortos(j1)
            if mortos2 != "":
                print("Navios afundados S: ", mortos2)
            if not j1.verificar_status():
                return msgF + ataque + "Servidor venceu!!"
                #print("Servidor venceu!!")
            elif not j2.verificar_status():
                return msgF + ataque + "Cliente venceu!!"
            reply = msgF + ataque + mortos
            self.conn.sendall(bytes(reply.encode()))
    
    def iniciaConexao(self):
        # Cria um socket TCP/IP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #garante que o socket será destruído (pode ser reusado) após uma interrupção da execução 
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # associa o socket a porta
        self.s.bind((self.host, self.port))

        print('Server %s on port %s' % (socket.gethostname(), self.port))
        self.s.listen(1)

        while True:
            # Espera por novas conexões
            print('waiting for a connection')
            # Aceita conexões
            self.conn, self.address = self.s.accept()

            try:
                print('Connected to' , socket.gethostname() , 'on port', self.port)
                while True:
                    data = self.conn.recv(1024)
                    if str(data.decode()).upper() == 'S':
                        resultado = self.jogar()
                        if resultado != "quit":
                            self.conn.sendall(bytes(resultado.encode()))
                    print('Fim do jogo')	
                    break
                    #conn.sendall(bytes(reply.encode()))
                        
                
            finally:
                # Clean up the connection
                self.conn.close()

        return        

if __name__ == "__main__":
    porta = 1234  #int(sys.argv[1])
    b = Servidor_TCP(porta)
    b.iniciaConexao()
        
        
