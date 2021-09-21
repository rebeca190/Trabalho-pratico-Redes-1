import socket
import sys
import os

class Servidor_UDP:

    def __init__(self, port):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        self.my_file = os.path.join(THIS_FOLDER, 'postos.txt')
        f = open(self.my_file, 'a')
        f.close()
        
        self.host = ''
        self.porta = port
        
        #cria um UDP/IP socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #garante que o socket será destruído (pode ser reusado) após uma interrupção da execução 
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        #associa o socket à uma porta
        self.s.bind((self.host, self.porta)) 
    
    def pesquisar(self, pesq):
        #Separa as informacoes
        tipo = pesq[0]
        raio = int(pesq[1])
        coordX = int(pesq[2])
        coordY = int(pesq[3])

        #abre o arquvio e lê todas as linhas
        f = open(self.my_file, 'r')
        texto = f.readlines()
        f.close()

        #verifica linha por linha, comparando o tipo e as coordenadas para compar com o menor preco já encontrado
        menorP = '' 
        for l in texto:
            linha = l.split()
            if linha[0] == tipo:
                if abs(int(linha[2]) - coordX) <= raio and  abs(int(linha[3]) - coordY) <= raio:
                    if menorP == '':
                        menorP = int(linha[1])
                    elif int(linha[1]) < menorP:
                        menorP = int(linha[1])
        
        if  menorP == '':
            menorP = "nenhum posto encontrado"
        return "O menor preço da região é " + str(menorP)
   
    def adicionar(self, adc):
        coordX = int(adc[2])
        coordY = int(adc[3])

        #Abre o arquvio e coloco o pointer no ultimo caracter
        f = open(self.my_file, 'a')
        #seta a linha a ser escrevida
        aux = "\n" + " ".join(adc) 
        #escreve no arquivo
        f.write(aux) 
        #fecha o arquivo
        f.close()

        return "O novo posto da coordenada " + str(coordX) + ":" + str(coordY) + " foi adiconado."
    def comunicacao(self):
        
        while True:
            #Espera por novas mensagens
            print('waiting to receive message')
            #Recebe a mensagem
            data, address = self.s.recvfrom(1024)
            #Escrever na tela as informações recebidas
            print ('Msg recebida: ' + str(data.decode()) + '\nDe: ' + address[0] + '\nEscutando na porta: ' + str(address[1]))
            #Transforma os bytes para string
            msg = (str(data.decode())).split()
            #Verifica se eh pesquisar ou dados
            if msg[0] == 'P':
                resp = self.pesquisar(msg[2:])
            else:
                resp = self.adicionar(msg[2:])
            #Seta a mensagem a ser enviada
            data = "Mensagem " + msg[1]  + " recebida\n" + resp
            #Transforma a mensagem para bytes e envia para o endereço que recebeu
            self.s.sendto(bytes(data.encode()), (address[0], address[1]))
            

if __name__ == "__main__":
    port = int(sys.argv[1]) #ip/nome
    serv = Servidor_UDP(port)
    serv.comunicacao()