import requests


def obter_clima():

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=-28.9369"
        "&longitude=-51.5495"
        "&current=temperature_2m,weather_code"
    )

    resposta = requests.get(url, timeout=5)

    dados = resposta.json()

    return {
        "temperatura": round(
            dados["current"]["temperature_2m"]
        ),
        "weather_code": dados["current"]["weather_code"]
    }