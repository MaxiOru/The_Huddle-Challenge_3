
import socket
import threading

host = '127.0.0.1'
port = 55123

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clientes = []
cliente_direccion = {}


def broadcast(mensaje):
    clientes_desconectados = []
    for cliente in clientes:
        try:
            cliente.send(mensaje)
        except (BrokenPipeError, ConnectionResetError, OSError) as e:
            print(f"No se pudo enviar mensaje: cliente desconectado ({e})")
            clientes_desconectados.append(cliente)
    
    # Limpiar clientes desconectados después del broadcast
    for cliente in clientes_desconectados:
        if cliente in clientes:
            clientes.remove(cliente)
            cliente_direccion.pop(cliente, None)
            cliente.close()


def handle(cliente, direccion):
    while True:
        try:
            direccion_cliente = cliente_direccion.get(cliente, direccion)
            mensaje_recibido = cliente.recv(1024)
            
            # Si el mensaje está vacío, el cliente se desconectó
            if not mensaje_recibido:
                break
                
            mensaje_enviar = f"{direccion_cliente}: {mensaje_recibido.decode()}"
            broadcast(mensaje_enviar.encode())
        except (ConnectionResetError, ConnectionAbortedError, OSError) as e:
            print(f"Cliente {direccion} desconectado o error: {e}")
            break
    
    # Limpieza al salir del loop
    if cliente in clientes:
        clientes.remove(cliente)
        direccion_cliente = cliente_direccion.pop(cliente, None)
        if direccion_cliente:
            broadcast(f"{direccion_cliente} dejó el chat.".encode())
        cliente.close()


def recibir():
    while True:
        try:
            cliente, direccion = server.accept()
            print(f"Conectado con {direccion}")
            
            cliente_direccion[cliente] = direccion
            clientes.append(cliente)

            broadcast(f"{direccion} se unió al chat.".encode())
            # cliente.send("Conectado al servidor".encode())
            
            thread = threading.Thread(target=handle, args=(cliente, direccion))
            thread.daemon = True
            thread.start()
            
        except OSError as e:
            print(f"Error al aceptar nueva conexión: {e}")
            break


print("Servidor escuchando")
recibir()

