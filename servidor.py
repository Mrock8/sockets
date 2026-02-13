import socket

# Configuración: IP local y puerto
HOST = '0.0.0.0'  # Escucha en todas las interfaces
PORT = 5000       

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor iniciado. Esperando conexión en el puerto {PORT}...")
    
    conn, addr = s.accept()
    with conn:
        print(f"Conectado con éxito desde: {addr}")
        while True:
            data = conn.recv(1024) # Recibe hasta 1024 bytes
            if not data:
                break
            print(f"Mensaje recibido: {data.decode('utf-8')}")
            conn.sendall(b"Mensaje recibido por el servidor")