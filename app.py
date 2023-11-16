import json

from flask import Flask, Response

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

app = Flask(__name__)


@app.route("/weather-forecast", methods=["POST"])
def create_weather_forecast():
    try:
        weather_forecast_adapter = get_weather_forecast_adapter()
        open_weather_service = get_open_weather_service()
        interactor = CreateWeatherForecastInteractor(
            weather_forecast_adapter=weather_forecast_adapter,
            open_weather_service=open_weather_service,
        )

        response = interactor.run()

        return response
    except Exception as e:
        error_message = f"{e.__class__.__name__}({e})"
        return Response(
            status=400,
            response=json.dumps({"message": error_message}),
        )


@app.route("/weather-forecast/<string:entity_id>")
def detail_weather_forecast(entity_id):
    try:
        weather_forecast_adapter = get_weather_forecast_adapter()
        interactor = DetailWeatherForecastInteractor(
            weather_forecast_adapter=weather_forecast_adapter,
            entity_id=entity_id,
        )

        response = interactor.run()

        return response
    except Exception as e:
        error_message = f"{e.__class__.__name__}({e})"
        return Response(
            status=400,
            response=json.dumps({"message": error_message}),
        )


@app.route("/weather-forecast/<string:entity_id>", methods=["DELETE"])
def delete_weather_forecast(entity_id):
    try:
        weather_forecast_adapter = get_weather_forecast_adapter()
        interactor = DeleteWeatherForecastInteractor(
            weather_forecast_adapter=weather_forecast_adapter,
            entity_id=entity_id,
        )

        interactor.run()

        return Response(status=204)
    except Exception as e:
        error_message = f"{e.__class__.__name__}({e})"
        return Response(
            status=400,
            response=json.dumps({"message": error_message}),
            content_type="application/json",
        )


@app.route("/weather-forecast")
def list_weather_forecast():
    try:
        weather_forecast_adapter = get_weather_forecast_adapter()
        interactor = ListWeatherForecastInteractor(
            weather_forecast_adapter=weather_forecast_adapter,
        )

        response = interactor.run()

        return response
    except Exception as e:
        error_message = f"{e.__class__.__name__}({e})"
        return Response(
            status=400,
            response=json.dumps({"message": error_message}),
            content_type="application/json",
        )
