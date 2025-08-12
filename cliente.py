
import socket
import threading

HOST = '127.0.0.1'
PORT = 55123

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#intenta conectarse al servidor
try:
    cliente.connect((HOST, PORT))
except ConnectionRefusedError as e:
    print(f"No se pudo conectar al servidor: {e}")
    exit()

print("Te has conectado al servidor, ya puedes escribir")
# funcion recibir mensajes  y mostrar
def recibir():
    try:
        while True:
            mensaje = cliente.recv(1024)
            if not mensaje:
                print("Conexión cerrada por el servidor.")
                break
            print(mensaje.decode())
    except (ConnectionAbortedError, ConnectionResetError, OSError) as e:
        print(f"Error en recepción: {e}")
    finally:
        cliente.close()
# hilo para poder recibir y mandar mensajes en simultaneo o paralelo
thread = threading.Thread(target=recibir, daemon=True)
thread.start()

try:
    while True:
        mensaje = input()
        if mensaje.lower() == "/salir":
            cliente.send("Usuario ha salido del chat.".encode())
            break
        cliente.send(mensaje.encode())
except KeyboardInterrupt:
    print("\nCerrando cliente por interrupción...")
finally:
    cliente.close()

