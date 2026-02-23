import socket
import threading

class Nodo:
    name = ""
    port = 5000
    peers = []
    
    
    def __init__(self,port=None, name=None):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('1.1.1.1', 80))
            host = s.getsockname()[0]
        
        #Atributos de la Clase Nodo
        self.name = name
        self.host = host
        self.port = port
        
        #El nodo escucha mensajes UDP por defecto para esperar sus nodos hermanos
        self.listen_thread = threading.Thread(target=self.listen).join().start()
        
        
    
    #=========================Metodos de la Clase Nodo=========================
    
    #=================Metodos de Descubrimiento de Nodos (UDP)=================
    
    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_UDP:
            s_UDP.bind(('', self.port))
            print("Esperando solicitudes de descubrimiento...")
            while True:
                #Posibles mejoras: agregar un sistema de autenticacion entre nodos
                data, addr = s_UDP.recvfrom(1024)
                if data == b"DISCOVERY_REQUEST":
                    print(f"Solicitud recibida de {addr}, respondiendo...")
                    s_UDP.sendto(b"NODO_ACTIVO_OK", addr)
       
    #=============================================================================
    #Se ejecuta discovery() durante la ejecucion del 
    #programa principal para hallar nuevos nodos
    def discovery(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_UDP:
            s_UDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s_UDP.settimeout(2)
            
            mensaje = b"DISCOVERY_REQUEST"
            
            try:
                print("Buscando nodos en la red...")
                s_UDP.sendto(mensaje, ('<broadcast>', self.port))
                while True:
                    data, addr = s_UDP.recvfrom(1024)
                    print(f"Nodo encontrado en la IP: {addr[0]} - Respuesta: {data.decode()}")
                    if self.host != addr:
                        self.peers.append(addr)
                        
            except s_UDP.timeout:
                print("Búsqueda finalizada.")
    
    #=================Metodos de Comunicacion entre Nodos (TCP)=================

    
    def start_server(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_TCP:
            s_TCP.bind(('0.0.0.0', self.port))
            s_TCP.listen(5)
            print('Esperando conecciones...')
            socket_cliente, addr = s_TCP.accept()
            
            while True:
                print(f'conexion acceptanda de {addr}')
                socket_cliente.send(bytes("Hola desde el servidor", "utf-8"))
                
    #=============================================================================       
    def start_client(self):
            
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_TCP:
            s_TCP.connect(( self.host))
            
            while True:
                    
                pass
        
    #=============================================================================       
    
           
    
           
            