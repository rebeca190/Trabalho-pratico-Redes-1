import socket
import sys 
import time
class Cliente_UDP:
    def __init__(self, host, port):
        self.host = host
        self.porta = port
        #cria um UDP/IP socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.idmsg = 0
    
    def leitura(self):
        continuar = True
        while continuar:
            acao = input("Deseja enviar dados(D) ou pesquisar(P) ou sair(Q): ")
            if acao.upper() == 'P' or acao.upper() == 'D':
                acao = acao.upper()
                continuar = False
            elif acao.upper() == 'Q':
                return "quit"
        continuar = True
        while continuar:
            tipo = input("Escolha o tipo de combustivel (0 - diesel, 1 - álcool, 2- gasolina): ")
            if tipo == '0' or tipo == '1' or tipo == '2':
                continuar = False

        continuar = True    
        if acao == 'D':
            while continuar:
                preco = input("Digite o preço do combustivel(Tam min 4): ")
                if preco.isnumeric() and len(preco) >= 4:
                    continuar = False
        else:
            while continuar:
                raio = input("Digite o raio de pesquisa: ")
                if raio.isnumeric():
                    continuar = False

        continuar = True
        while continuar:
            coordX = input("Digite a longitude: ")
            if coordX.isnumeric():
                continuar = False
        
        continuar = True
        while continuar:
            coordY = input("Digite a latitude: ")
            if coordY.isnumeric():
                continuar = False

        if acao == 'D':
            return acao + " " + str(self.idmsg) + " " + tipo + " " + preco + " " + coordX + " " + coordY
        else:
            return acao + " " + str(self.idmsg) + " " + tipo + " " + raio + " " + coordX + " " + coordY
        
    def reenviaErro(self, msg):
        contador = 0
        print("Erro ao receber mesnagem." , end="")
        msgR = 'lixo ' + str(self.idmsg-1)
        msgR = bytes(msgR.encode())
        while int(str(msgR.decode()).split()[1]) != self.idmsg:
            contador = contador + 1
            print("Tentando reenviar mensagem... ")
            self.s.sendto(bytes(msg.encode()), (self.host, self.porta))
            try:
                msgR, adress = self.s.recvfrom(1024)
            except:
                time.sleep(5)
            if contador == 6:
                print("Time out, verifique o status do servidor")
                return "quit"
        print("Mensagem número ", str(self.idmsg), " enviada.")
        return str(msgR.decode())

    def comunicacao(self):
        #Tempo maximo de espera por uma resposta
        self.s.settimeout(30.0)
        while True:
            #incremento identificador da mensagem
            self.idmsg = self.idmsg + 1
            msg = self.leitura()
            
            if msg != 'quit':
                #Envio de mensagm em bytes para o servidor
                self.s.sendto(bytes(msg.encode()), (self.host, self.porta))
                print("Mensagem número ", str(self.idmsg), " enviada.")
                msgR =  bytes("lixo".encode())
                try:
                    msgR, adress = self.s.recvfrom(1024)
                    resp = str(msgR.decode())
                except:
                    resp = self.reenviaErro(msg)
                    if resp == 'quit':
                        break
                aux = int(resp.split()[1])
                if aux != self.idmsg:
                    resp = self.reenviaErro(msg)
                print("Servidor responde: ", resp ) 
            else:
                break 
            
            
        print('closing socket')
        self.s.close()

if __name__ == "__main__":
    host = sys.argv[1] #ip/nome
    port = int(sys.argv[2]) #porta
    cli = Cliente_UDP(host,port)
    cli.comunicacao()