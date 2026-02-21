
import socket
import threading
import time
import json

class Nodo:
    def __init__(self, port, peers_hosts=None):
        # Obtener IP local
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('1.1.1.1', 80))
            ip_local = s.getsockname()[0]
        
        self.host = ip_local
        self.port = port
        self.peers_hosts = set(peers_hosts or [])  # Conjunto de hosts de peers conocidos
        self.connections = {}  # Diccionario de conexiones activas: { (host, port): socket }
        self.server_socket = None
        self.running = True
        
    
    def handle_listen(self):
        thread = threading.Thread(target=self.start_listen)
        thread.start()
    
    def start_listen(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # Escuchar hasta 5 conexiones pendientes
            
        print(f'Escuchando en {self.host}:{self.port}')
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f'Conexión recibida de {addr}')
                # Manejar la conexión en un hilo separado
                thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                thread.start()
            except OSError:
                break  # Socket cerrado
    
    def handle_client(self, client_socket, addr):
        # Intercambiar lista de peers al inicio
        self.exchange_peers(client_socket)
        
        # Aquí puedes manejar la recepción de datos
        # Por simplicidad, solo mantener la conexión abierta
        self.connections[addr] = client_socket
        try:
            while self.running:
                # Esperar datos o algo; por ahora, solo mantener
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f'Datos recibidos de {addr}: {data.decode()}')
                # Puedes procesar o reenviar
        except:
            pass
        finally:
            client_socket.close()
            if addr in self.connections:
                del self.connections[addr]
    
    def exchange_peers(self, sock):
        try:
            # Enviar mi lista de peers
            peers_list = list(self.peers_hosts)
            sock.sendall(json.dumps(peers_list).encode())
            
            # Recibir lista del otro nodo
            data = sock.recv(1024)
            if data:
                other_peers = json.loads(data.decode())
                for host in other_peers:
                    if host not in self.peers_hosts and host != self.host:
                        self.peers_hosts.add(host)
                        print(f'Nuevo peer descubierto: {host}')
                        # Intentar conectar al nuevo peer
                        thread = threading.Thread(target=self.connect_to_peer, args=(host,))
                        thread.start()
        except Exception as e:
            print(f'Error en intercambio de peers: {e}')
    
    def connect_to_peer(self, peer_host):
        if (peer_host, self.port) in self.connections:
            return  # Ya conectado
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer_host, self.port))
            self.connections[(peer_host, self.port)] = s
            print(f'Conectado a {peer_host}:{self.port}')
            # Manejar la conexión saliente en un hilo
            thread = threading.Thread(target=self.handle_client, args=(s, (peer_host, self.port)))
            thread.start()
        except Exception as e:
            print(f'Error conectando a {peer_host}: {e}')
    
    def start_mesh(self):
        for peer_host in self.peers_hosts:
            if peer_host != self.host:  # No conectar a sí mismo
                thread = threading.Thread(target=self.connect_to_peer, args=(peer_host,))
                thread.start()
    
    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        for conn in self.connections.values():
            conn.close()
        self.connections.clear()
    
    
def main():
    # Ejemplo: Crear un nodo con lista de peers conocidos (puedes cambiar por IPs reales)
    peers_known = set()  # Conjunto de hosts de otros nodos, e.g., {'192.168.1.100', '192.168.1.101'}
    nodo1 = Nodo(5000, peers_known)
    nodo1.handle_listen()
    nodo1.start_mesh()
    
    # Mantener el programa corriendo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        nodo1.stop()
        print("Nodo detenido")

if __name__ == '__main__':
    main()