
import socket
import threading

HOST = '127.0.0.1'
PORT = 55123

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Servidor escuchando en {HOST}:{PORT}")

clientes = []
#funcion para mandar mensajes a todos los cliente conectados, en la lista clientes
def broadcast(mensaje):
    for cliente in clientes[:]:
        try:
            cliente.send(mensaje)
        except (BrokenPipeError, ConnectionResetError, OSError) as e:
            print(f"No se pudo enviar mensaje: cliente desconectado ({e})")
            # remover el cliente
            if cliente in clientes:
                clientes.remove(cliente)
#funcion para tratar a los clientes, recibir sus mensajes, y de acuerdo a su contendio lo manda o no a los demas o les avisa
def handle(cliente, direccion):
    try:
        while True:
            mensaje = cliente.recv(1024)
            if not mensaje:
                # Cliente desconectado
                broadcast(f"{direccion} se desconectó.".encode())
                break
            texto = mensaje.decode()
            if texto == "Usuario ha salido del chat.":
                broadcast(f"{direccion} dejó el chat.".encode())
                break
            broadcast(f"{direccion}: {texto}".encode())
    except (ConnectionResetError, ConnectionAbortedError, OSError) as e:
        print(f"Cliente {direccion} desconectado o error: {e}")
        broadcast(f"{direccion} se desconectó.".encode())
    finally:
        if cliente in clientes:
            clientes.remove(cliente)
        cliente.close()
# funcion que permite recibir clientes y crear hilos para cada cliente
def recibir():
    try:
        while True:
            cliente, direccion = server.accept()
            print(f"Conectado con {direccion}")
            clientes.append(cliente)
            broadcast(f"{direccion} se ha conectado".encode())
            thread = threading.Thread(target=handle, args=(cliente, direccion), daemon=True)
            thread.start()
    except OSError as e:
        print(f"Servidor cerrado o error en accept: {e}")

if __name__ == "__main__":
    print("Para cerrar el servidor cierra esta ventana.")
    recibir()
