import requests

class TokenRequester:
    def __init__(self, url, cliente):
        self.url = url
        self.cliente = cliente

    def obtener_token(self, usuario, contrasena):
        # Datos de la solicitud
        datos = {
            "userName": usuario,
            "userPassword": contrasena
        }

        # Encabezados de la solicitud
        encabezados = {
            "Cliente": self.cliente
        }

        try:
            # Realizar la solicitud POST para obtener el token
            respuesta = requests.post(self.url, json=datos, headers=encabezados)

            # Verificar el código de estado de la respuesta
            if respuesta.status_code == 200:
                # La solicitud fue exitosa
                respuesta_json = respuesta.json()
                if respuesta_json.get("ok"):
                    token = respuesta_json.get("data")
                    return token
                else:
                    print("Error en la respuesta: ", respuesta_json.get("message"))
                    return None
            else:
                # La solicitud no fue exitosa
                print(f"Error al obtener el token. Código de estado: {respuesta.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            # Ocurrió un error durante la solicitud
            print(f"Error al obtener el token: {str(e)}")
            return None