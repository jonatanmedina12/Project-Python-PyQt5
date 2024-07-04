from SqlLiteData.sqlLogic import sqlConfiguration
from LogicConnectFuntions.bidireccional import BidireccionalConnect

class MainConnect:
    def __init__(self, data):
        self.data = data
        self.connect = sqlConfiguration("desarrollo4", "Colcan2024*")
        self.conectado = False

    def connect_to_analyzer(self):
        try:
            conn = self.connect.create_connection()
            params = self.connect.load_parametrization(conn)
            if params:
                tipo_conexion = params[3]
                if tipo_conexion == "socket":
                    # Conectar mediante socket
                    ip = params[5]
                    socket1 = params[6]
                    funcion_socket1 = params[7]
                    tipo_socket1 = params[8]
                    socket2 = params[10]
                    funcion_socket2 = params[11]
                    tipo_socket2 = params[12]
                    modo_socket = params[13]

                    if modo_socket == "Bidireccional":
                        connect_bidireccional = BidireccionalConnect(ip, socket1, socket2)
                        connect_bidireccional.create_bidirectional_connection()
                        connect_bidireccional.create_bidirectional_connection2()
                        self.conectado = True
                        print("Conexión bidireccional establecida")
                    elif modo_socket == "Unidireccional":
                        connect_unidireccional = BidireccionalConnect(ip, socket1, "")
                        connect_unidireccional.create_bidirectional_connection()
                        self.conectado = True
                        print("Conexión unidireccional establecida")
                else:
                    print("Tipo de conexión no válido.")
            else:
                print("No se encontró la parametrización.")
        except Exception as e:
            print(f"Error al conectar al analizador: {e}")

    def is_connected(self):
        return self.conectado