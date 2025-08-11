import socket
import threading

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 55123))
print ("Te has conectado al servidor, ya puedes escribir")


def recibir():
    while True:
        try:
            mensaje = cliente.recv(1024)
            # Si el mensaje está vacío, el servidor cerró la conexión
            if not mensaje:
                print("El servidor cerró la conexión.")
                cliente.close()
                break
            print(mensaje.decode())
        except (ConnectionAbortedError, ConnectionResetError, OSError) as e:
            print(f"Error de conexión: {e}")
            cliente.close()
            break


def write():
    while True:
        try:
            mensaje = input()
            if mensaje.lower() == "/salir":
                cliente.send("Usuario ha salido del chat.".encode())
                cliente.close()
                break
            # No enviar mensajes vacíos
            if mensaje.strip():
                cliente.send(mensaje.encode())
        except (BrokenPipeError, ConnectionResetError, OSError) as e:
            print(f"Error al enviar mensaje: {e}")
            break


recive_thread = threading.Thread(target=recibir)
recive_thread.daemon = True
recive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.daemon = True
write_thread.start()

# Esperar a que termine el thread de escritura
write_thread.join()