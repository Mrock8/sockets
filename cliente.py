import socket
import ctypes

# Cambia '127.0.0.1' por la IP de la máquina servidor si usas pfSense
HOST = '192.168.31.24' 
PORT = 5000

def logoff():
    ctypes.windll.user32.ExitWindowsEx(0, 0)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        
        respuesta = s.recv(1024)
        
        op = respuesta.decode('utf-8')
        
        
        match int(op):
            case 1:
                logoff()
            case _:
                print('Opcion no definida')
                break
        
        
        


        