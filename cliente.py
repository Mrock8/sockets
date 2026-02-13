import socket

# Cambia '127.0.0.1' por la IP de la máquina servidor si usas pfSense
HOST = '192.168.31.24' 
PORT = 5000



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        mensaje = input("Escribe tu mensaje (o 'salir'): ")
        if mensaje.lower() == 'salir':
            break
        s.sendall(mensaje.encode('utf-8'))
        respuesta = s.recv(1024)
        print(f"Respuesta del servidor: {respuesta.decode('utf-8')}")
        print(f"_________________________________")
        