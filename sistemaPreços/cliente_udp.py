import socket
import sys

#endereço para o qual os dados vão ser enviados
host = 'localhost'

#número da porta que o servidor que vai receber os dados está escutando
port = 1234

#cria um UDP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print ('Para sair use CTRL+X e pressione enter\n')
msg = 'ok'
while msg != '\x18':
	#envia os dados
	msg = input("Digite msg: ")
	s.sendto(bytes(msg.encode()), (host, port))
	
	msg, adress = s.recvfrom(1024)
	print("R:", str(msg.decode())  ) 
	
print('closing socket')
s.close()