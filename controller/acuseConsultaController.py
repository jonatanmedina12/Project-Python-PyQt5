import requests


class acuseRequester:
    def __init__(self, url, cliente):
        self.url = url
        self.cliente = cliente

    def AcuseRequest(self, token, id):
        # Encabezados de la solicitud
        encabezados = {
            "Authorization": f"Bearer {token}",
            "Cliente": self.cliente
        }

        try:

            url = f'{self.url}/{id}'
            response = requests.get(url, headers=encabezados)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                raise Exception(f'Request failed with status code {response.status_code}')

        except requests.exceptions.RequestException as e:
            # Ocurrió un error durante la solicitud
            print(f"Error al consultar los datos: {str(e)}")
            return None