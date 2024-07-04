import requests


class ConsultaRequester:
    def __init__(self, url, cliente):
        self.url = url
        self.cliente = cliente

    def consultar_datos(self, token, code_dm):
        # Encabezados de la solicitud
        encabezados = {
            "Authorization": f"Bearer {token}",
            "Cliente": self.cliente
        }

        # Datos de la solicitud
        datos = {
            "CodeDM": code_dm
        }

        try:
            # Realizar la solicitud POST para consultar los datos
            respuesta = requests.post(self.url, json=datos, headers=encabezados)

            # Verificar el código de estado de la respuesta
            if respuesta.status_code == 200:
                # La solicitud fue exitosa
                respuesta_json = respuesta.json()
                if respuesta_json.get("ok"):
                    datos_consultados = respuesta_json.get("data")
                    if datos_consultados:
                        return datos_consultados
                    else:
                        return {"ok": True, "message": None, "data": []}
                else:
                    print("Error en la respuesta: ", respuesta_json.get("message"))
                    return None
            else:
                # La solicitud no fue exitosa
                print(f"Error al consultar los datos. Código de estado: {respuesta.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            # Ocurrió un error durante la solicitud
            print(f"Error al consultar los datos: {str(e)}")
            return None