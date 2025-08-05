'''
import socket

host = '127.0.0.1' #ip del servidor
port = 65123 #puerto de envio

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((host, port))
    print (f"conectado al servidor {host}:{port}")
    while True:
        mensaje = input("Ingrese le mensaje: ")
        # se manda el mensaje codificado en bytes
        cliente.sendall(mensaje.encode())

        data = cliente.recv(1024)
        respuesta = data.decode()
        print("recibido del servidor: ", respuesta)
        print(" ")
        decision = input("Desea manda otro mensaje ? si o no: ").lower()
        if decision != "si":
            break

finally:
    cliente.close()
'''



import socket
import threading

apodo = input("Elige un apodo: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    cliente.connect(('127.0.0.1',55123))
except ConnectionRefusedError:
    print("no se pudo conectar, el servidor esta escuchando?")

def recibir():
    while True:
        try:
            mensaje = cliente.recv(1024).decode()
            if mensaje == 'Apodo':
                cliente.send(apodo.encode())
            else:
                print(mensaje)
        except ConnectionAbortedError:
            print("La conexión fue abortada localmente.")
            cliente.close()
            break
        except ConnectionResetError:
            print("El servidor cerró la conexión inesperadamente.")
            cliente.close()
            break
        except OSError as e:
            print(f"Error de socket al recibir: {e}")
            cliente.close()
            break

def write():
    while True:
        try:
            mensaje = input()
            if mensaje.lower() == "/salir":
                cliente.send(f"{apodo} ha salido del chat.".encode())
                cliente.close()
                break
            cliente.send(f"{apodo}: {mensaje}".encode())
        except BrokenPipeError:
            print("El servidor cerró la conexión de forma inesperada (pipe roto).")
            break
        except ConnectionResetError:
            print("La conexión fue restablecida por el servidor.")
            break
        except OSError as e:
            print(f"Error general de socket: {e}")
            break


recive_thread = threading.Thread(target=recibir)
recive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()




