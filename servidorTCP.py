'''
@Author Alberto Horcajada Perez
@Version 1.0 23/02/2022
'''

from socketserver import BaseRequestHandler, TCPServer
from socket import socket, AF_INET, SOCK_STREAM

class RequestHandler(BaseRequestHandler):
    def handle(self):
        while True:
            bloque = self.request.recv(512)
            if not bloque: break
            if(bloque==bytes("Hola".encode())):
                bloque = bytes("botVacacional: Muy buenas usuario\n ¿Que desea usted hacer?".encode())
            elif(bloque == bytes("mes enviado".encode())):
                bloque = bytes("botVacacional: Mes recibido, cuantos dias quieres reservar de ese mes?".encode())
            elif(bloque == bytes("dia enviado".encode())):
                bloque = bytes("botVacacional: Dias recibidos, espera un momento mientras se realiza la operacion".encode())
            elif(bloque == bytes("Adios".encode())):
                bloque = bytes("botVacacional: Hasta la proxima, pase buen dia y disfrute las vacaciones".encode())
            elif(bloque == bytes("Quiero reservar unas vacaciones".encode())):
                bloque = bytes("botVacacional: Por supuesto, ¿que mes quieres reservar?\nRecuerda ingresar solo las tres primeras letras del mes".encode())
            else:
                bloque = bytes("botVacacional: Lo siento no te he entendido, ¿puedes repetirlo?".encode())
            
            self.request.send(bloque)
            
            
def start_server():
    server = TCPServer(('localhost', 64325), RequestHandler)
    server.serve_forever()