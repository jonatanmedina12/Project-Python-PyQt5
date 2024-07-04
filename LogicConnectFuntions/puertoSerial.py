import serial

class SerialConnection:
    def __init__(self, puerto, baudrate, bytesize, parity, stopbits):
        self.puerto = puerto
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.ser = None

    def conectar(self):
        try:
            self.ser = serial.Serial(
                port=self.puerto,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits
            )
            print(f"Conexión exitosa al puerto {self.puerto}")
        except serial.SerialException:
            print(f"Error al conectar con el puerto {self.puerto}")

    def enviar_datos(self, datos):
        if self.ser is not None:
            self.ser.write(datos.encode())
            print(f"Datos enviados: {datos}")
        else:
            print("No hay una conexión serial establecida")

    def recibir_datos(self):
        if self.ser is not None:
            if self.ser.in_waiting > 0:
                datos = self.ser.readline().decode('utf-8').rstrip()
                return datos
            else:
                return None
        else:
            print("No hay una conexión serial establecida")
            return None

    def cerrar_conexion(self):
        if self.ser is not None:
            self.ser.close()
            print("Conexión cerrada")

    def obtener_conexion(self):
        return self.ser