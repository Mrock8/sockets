import socket

class Nodo:
    name = ""
    def __init__(self,port, name=None):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('1.1.1.1', 80))
            host = s.getsockname()[0]
        
        self.name = name
        self.host = host