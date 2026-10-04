import requests


def obter_clima():

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=-28.9369"
        "&longitude=-51.5495"
        "&current=temperature_2m,weather_code"
    )

    try:

        resposta = requests.get(
            url,
            timeout=5
        )

        # Se a API retornar 4xx ou 5xx,
        # gera uma exceção controlada
        resposta.raise_for_status()

        dados = resposta.json()

        # Verifica se a resposta realmente possui "current"
        current = dados.get("current")

        if not current:
            print(
                "Resposta inesperada da Open-Meteo:",
                dados
            )

            return {
                "temperatura": "--",
                "weather_code": None
            }

        temperatura = current.get("temperature_2m")
        weather_code = current.get("weather_code")

        return {
            "temperatura": (
                round(temperatura)
                if temperatura is not None
                else "--"
            ),
            "weather_code": weather_code
        }


    except requests.RequestException as erro:

        print(
            "Erro ao consultar Open-Meteo:",
            erro
        )

        return {
            "temperatura": "--",
            "weather_code": None
        }


    except ValueError as erro:

        print(
            "Resposta inválida da Open-Meteo:",
            erro
        )

        return {
            "temperatura": "--",
            "weather_code": None
        }