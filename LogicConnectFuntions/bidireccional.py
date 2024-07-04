from Socket_connection.socket_logic import SocketConnect


class BidireccionalConnect:
    def __init__(self, ip, puerto, puerto2):
        self.ip = ip
        self.puerto = puerto
        self.puerto2 = puerto2

    def create_bidirectional_connection(self):
        try:
            # Crear conexión de socket 1
            socket1 = SocketConnect(self.ip, self.puerto)
            socket1_conn = socket1.connect_function_socket()

            if socket1_conn is not None:
                return socket1_conn
            else:
                return None

        except Exception as e:
            print(e)

    def create_bidirectional_connection2(self):
        try:

            # Crear conexión de socket 2
            socket2 = SocketConnect(self.ip, self.puerto2)
            socket2_conn = socket2.connect_function_socket()

            if socket2_conn is not None:
                return socket2_conn
            else:
                return None
        except Exception as e:
            print(e)
