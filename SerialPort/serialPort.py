import serial


class serialPort:
    def __init__(self, puerto, baudrate, timeout):
        self.puerto = puerto
        self.baudrate = baudrate
        self.timeout = timeout

    @staticmethod
    def checksum_to_hex(checksum):
        return f"{checksum:02X}"

    def connect_to_serial(self):
        try:
            # Abrir la conexión serial
            ser = serial.Serial(self.puerto, self.baudrate, timeout=self.timeout)
            print("Conexión establecida con el analizador en el puerto", self.puerto)

            # Enviar mensaje de establecimiento de conexión (ENQ)
            mensaje_enq = b'\x05'
            ser.write(mensaje_enq)
            print("Mensaje ENQ enviado")

            # Esperar la respuesta de establecimiento de conexión (ACK)
            mensaje_ack = ser.read(1)
            if mensaje_ack == b'\x06':
                print("Mensaje ACK recibido")
            else:
                print("Error al recibir el mensaje ACK")
                raise serial.SerialException("Error de conexión")

            # Construir la trama ASTM
            stx = b'\x02'  # Carácter STX (Start of Text)
            etx = b'\x03'  # Carácter ETX (End of Text)
            cr = b'\x0D'  # Carácter CR (Carriage Return)
            cl = b"0x0A"
            trama_datos = b'1H|\\^&||||||||||P|1|||||||||||||||||N||||||||||||||'
            trama_sin_checksum = stx + trama_datos + cr + etx
            print(trama_sin_checksum)
            checksum = self.calcular_checksum(trama_sin_checksum)
            print(checksum)
            checksum_hex = self.checksum_to_hex(checksum).encode()
            print(checksum_hex)
            trama_envio = stx + trama_datos  + b"\r" + etx +checksum_hex + b"\r" + b"\n"

            # Enviar la trama ASTM al analizador
            ser.write(trama_envio)
            print("Trama enviada:", trama_envio)

            # Esperar el mensaje de aceptación de trama (ACK)
            mensaje_ack = ser.read(1)
            if mensaje_ack == b'\x06':
                print("Mensaje ACK recibido")
            else:
                print("Error al recibir el mensaje ACK")
                raise serial.SerialException("Error de comunicación")

            # Leer la respuesta del analizador
            trama_respuesta = b''
            while True:
                byte = ser.read(1)
                trama_respuesta += byte
                if byte == etx:
                    break
            print("Respuesta recibida:", trama_respuesta)

            # Enviar mensaje de fin de conexión (EOT)
            mensaje_eot = b'\x04'
            ser.write(mensaje_eot)
            print("Mensaje EOT enviado")

        except serial.SerialException as e:
            print("Error en la comunicación serial:", str(e))

        finally:
            # Cerrar la conexión serial
            if 'ser' in locals() and ser.is_open:
                ser.close()
                print("Conexión cerrada con el analizador en el puerto", self.puerto)

    # Función para calcular el checksum
    @staticmethod
    def calcular_checksum( trama):
        checksum = 0
        for byte in trama:
            if byte not in [0x02, 0x03, 0x0D, 0x0A]:  # Excluir caracteres de control
                checksum += byte
        return checksum % 256


if __name__ == "__main__":
    sc = serialPort("COM2", 9600, 1)
    sc.connect_to_serial()
