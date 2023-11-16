from http.server import BaseHTTPRequestHandler, HTTPServer


import json
from typing import Optional

from adapters.getters import get_weather_forecast_adapter
from backend.interactors.delete_weather_forecast_interactor import (
    DeleteWeatherForecastInteractor,
)
from backend.interactors.detail_weather_forecast_interactor import (
    DetailWeatherForecastInteractor,
)
from backend.interactors.create_weather_forecast_interactor import (
    CreateWeatherForecastInteractor,
)
from backend.interactors.list_weather_forecast_interactor import (
    ListWeatherForecastInteractor,
)
from backend.services.getters import get_open_weather_service


def create_weather_forecast():
    weather_forecast_adapter = get_weather_forecast_adapter()
    open_weather_service = get_open_weather_service()
    interactor = CreateWeatherForecastInteractor(
        weather_forecast_adapter=weather_forecast_adapter,
        open_weather_service=open_weather_service,
    )

    response = interactor.run()

    return response


def detail_weather_forecast(entity_id):
    weather_forecast_adapter = get_weather_forecast_adapter()
    interactor = DetailWeatherForecastInteractor(
        weather_forecast_adapter=weather_forecast_adapter, entity_id=entity_id
    )

    response = interactor.run()

    return response


def delete_weather_forecast(entity_id):
    weather_forecast_adapter = get_weather_forecast_adapter()
    interactor = DeleteWeatherForecastInteractor(
        weather_forecast_adapter=weather_forecast_adapter, entity_id=entity_id
    )

    interactor.run()


def list_weather_forecast():
    weather_forecast_adapter = get_weather_forecast_adapter()
    interactor = ListWeatherForecastInteractor(
        weather_forecast_adapter=weather_forecast_adapter,
    )

    response = interactor.run()

    return response


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa
        if self.path.startswith("/weather-forecast/"):
            entity_id = self.path.split("/")[-1]

            if entity_id:
                response = detail_weather_forecast(entity_id)
            else:
                response = list_weather_forecast()

            self._response(response)
        else:
            self._response(status_code=404)

    def do_POST(self):  # noqa
        if self.path == "/weather-forecast":
            response = create_weather_forecast()
            self._response(response, 201)
        else:
            self._response(status_code=400)

    def do_DELETE(self):  # noqa
        if self.path.startswith("/weather-forecast/"):
            entity_id = self.path.split("/")[-1]
            delete_weather_forecast(entity_id)
            self._response(status_code=204)
        else:
            self._response(status_code=400)

    def _response(self, response: Optional = None, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        if response:
            self.wfile.write(json.dumps(response).encode())


def main():
    print("Starting server")
    server = HTTPServer(("localhost", 5000), Handler)
    print("Listening at port 5000 🚀")
    server.serve_forever()


if __name__ == "__main__":
    main()
