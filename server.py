'''
import socket
import threading

host = '127.0.0.1' # localhost (direccion del propio equiepo)
port =  65123 #puerto mayores a 1023 estan liberados (puerto de escucha)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((host, port))
    server.listen()
    print("El seridor esta escuchando")
    conn, addr = server.accept()
    print (f"Conetado a: {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            mensaje = data.decode()
            print(f"mensaje del usuario: {mensaje}")
            conn.sendall(data)
    finally:
        conn.close()
finally:
    server.close()
'''



import socket
import threading

host = '127.0.0.1'
port = 55123

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clientes = []
apodos = []

def broadcast(mensaje):
    for cliente in clientes:
        try:
            cliente.send(mensaje)
        except BrokenPipeError:
            print("No se pudo enviar mensaje: cliente desconectado (pipe roto).")
        except ConnectionResetError:
            print("Cliente cerró conexión inesperadamente durante broadcast.")
        except OSError as e:
            print(f"Error general al hacer broadcast: {e}")
        

def handle(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)
            broadcast(mensaje)
        except ConnectionResetError:
            print("El cliente cerró la conexión de forma abrupta.")
        except ConnectionAbortedError:
            print("El cliente abortó la conexión.")
        except OSError as e:
            print(f"Error de socket con el cliente: {e}")
        finally:
            if cliente in clientes:
                index = clientes.index(cliente)
                cliente.close()
                apodo = apodos.pop(index)
                clientes.remove(cliente)
                broadcast(f"{apodo} dejó el chat.".encode())
            break

def recibir():
    while True:
        try:
            cliente, direccion = server.accept()
            print(f"Conectado con {direccion}")
        except OSError as e:
            print(f"Error al aceptar nueva conexión: {e}")
            break

        try:
            cliente.send("Apodo".encode())
            apodo = cliente.recv(1024).decode().strip()
            if not apodo:
                raise ValueError("Apodo vacío")
        except ConnectionResetError:
            print("Cliente cerró conexión antes de enviar apodo.")
            cliente.close()
            continue
        except ValueError:
            print("Cliente envió apodo vacío.")
            cliente.close()
            continue
        except Exception as e:
            print(f"Error al recibir apodo: {e}")
            cliente.close()
            continue

        apodos.append(apodo)
        clientes.append(cliente)
        print(f"Apodo del cliente: {apodo}")
        broadcast(f"{apodo} se unió al chat.".encode())
        cliente.send("Conectado al servidor.".encode())

        thread = threading.Thread(target=handle, args=(cliente,))
        thread.start()


print("Servidor escuchando")
recibir()

