import socket
import sys 
import time
import datetime

class Cliente_UDP:
    def __init__(self):
        self.host = 'localhost'
        self.porta = 1234
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.idmsg = 2
    
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
                preco = input("Digite o preço do combustivel: ")
                if preco.isnumeric() :
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
        #um inteiro identificador da mensagem
        if acao == 'D':
            return acao + " " + str(self.idmsg) + " " + tipo + " " + preco + " " + coordX + " " + coordY
        else:
            return acao + " " + str(self.idmsg) + " " + tipo + " " + raio + " " + coordX + " " + coordY
        
    def reenviaErro(self, msg):
        print("Erro ao receber mesnagem." , end="")
        msgR = 'lixo lixo ' + str(self.idmsg-1)
        msgR = bytes(msgR.encode())
        while int(str(msgR.decode()).split()[2]) != self.idmsg:
            print("Tentando reenviar mensagem... ")
            self.s.sendto(bytes(msg.encode()), (self.host, self.porta))
            try:
                msgR, adress = self.s.recvfrom(1024)
            except:
                time.sleep(5)
        print("Mensagem número ", str(self.idmsg), " enviada.")
        return str(msgR.decode())

    def comunicacao(self):
        while True:
            self.idmsg = self.idmsg + 1
            msg = self.leitura()
            target_time = datetime.datetime(2020, 10, 31, 15, 59, 10)  # 3 am on 3 July 2017
            while datetime.datetime.now() < target_time:
                time.sleep(1)
            if msg != 'quit':
                self.s.sendto(bytes(msg.encode()), (self.host, self.porta))
                print("Mensagem número ", str(self.idmsg), " enviada.")
                msgR =  bytes("lixo".encode())
                try:
                    msgR, adress = self.s.recvfrom(1024)
                    resp = str(msgR.decode())
                except:
                    resp = self.reenviaErro(msg)
                aux = int(resp.split()[2])
                if aux != self.idmsg:
                    resp = self.reenviaErro(msg)
                print("Servidor responde: ", resp ) 
            else:
                break 
            
            self.s.sendto(bytes(msg.encode()), (self.host, self.porta))
            print("Mensagem número ", str(self.idmsg), " enviada.")
            msgR =  bytes("lixo".encode())
            try:
                msgR, adress = self.s.recvfrom(1024)
                resp = str(msgR.decode())
            except:
                resp = self.reenviaErro(msg)
            aux = int(resp.split()[2])
            if aux != self.idmsg:
                resp = self.reenviaErro(msg)
            print("Servidor responde: ", resp ) 

        print('closing socket')
        self.s.close()

if __name__ == "__main__":
    cli = Cliente_UDP()
    cli.comunicacao()