import socket
import tkinter as tk
import threading
import ctypes

# Cambia '127.0.0.1' por la IP de la máquina servidor si usas pfSense
HOST = '192.168.31.24' 
PORT = 5000

bloqueo = None

def crear_pantalla_bloqueo():
    global bloqueo
    bloqueo = tk.Tk()
    bloqueo.attributes('-fullscreen', True)  # Pantalla completa
    bloqueo.attributes('-topmost', True)    # Siempre al frente
    bloqueo.configure(bg='black')           # Fondo negro
    
    label = tk.Label(bloqueo, text="ACCESO RESTRINGIDO", fg="white", bg="black", font=("Arial", 30))
    label.pack(expand=True)
    
    # Bloquea intentos de cerrar con Alt+F4
    bloqueo.protocol("WM_DELETE_WINDOW", lambda: None)
    bloqueo.mainloop()

def logoff():
    ctypes.windll.user32.ExitWindowsEx(0, 0)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        
        respuesta = s.recv(1024)
        
        op = int(respuesta.decode('utf-8'))
        
        
        match op:
            case 1:
                logoff()
            case 2:
                threading.Thread(target=crear_pantalla_bloqueo).start()
            case 3:
                if bloqueo:
                    bloqueo.quit() # Cierra la ventana y devuelve el control
            case _:
                print('Opcion no definida')
                break
        
        
        


        