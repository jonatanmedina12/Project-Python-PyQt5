import socket
import time


class SocketConnect:
    def __init__(self, ip_analizador, port):
        self.ip_analizador = ip_analizador
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_function_socket(self, max_attempts=10, retry_interval=1):
        try:
            attempts = 0
            while attempts < max_attempts:
                try:
                    self.sock.connect((self.ip_analizador, self.port))
                    print("Conexión exitosa al analizador.")
                    return self.sock
                except ConnectionRefusedError as e:
                    attempts += 1
                    print(f"Intento de conexión {attempts} fallido. Reintentando en {retry_interval} segundo(s)...")
                    time.sleep(retry_interval)

            print(f"No se pudo establecer conexión con el analizador después de {max_attempts} intentos.")
            return None
        except Exception as e:
            print(e)
