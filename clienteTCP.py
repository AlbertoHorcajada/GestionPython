'''
@Author Alberto Horcajada Perez
@Version 1.0 23/02/2022
'''

from socket import socket, AF_INET, SOCK_STREAM


def escribir_al_servidor_TCP(inst, mensaje:str=""):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('localhost', 64325))
    

    meses = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]
    if mensaje in meses:
        inst.mes = mensaje
        mensaje = "mes enviado"
    try:
        int(mensaje)
        inst.dias=mensaje
        mensaje = "dia enviado"
    except:
        pass

    sock.send(bytes(mensaje.encode()))

    bloque=sock.recv(8192).decode()
    inst.listaChat.put(bloque)
    '''
    inst.listaChat.put(bloque)
    inst.hiloMostrarMensaje()'''