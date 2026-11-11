"""Точка входа. Запускает Flask и фоновый контроллер.

Переменная окружения HARDWARE задаёт слой железа:
  - mock (по умолчанию) — без реального железа, для разработки
  - rpi — реализация для Raspberry Pi (появится позже)
"""
import os

from flask import Flask, jsonify

from api.routes import create_blueprint
from core.controller import Controller
from hardware.mock import MockHumiditySensor, MockRelay


def build_controller() -> Controller:
    hardware = os.environ.get("HARDWARE", "mock")
    if hardware == "mock":
        sensor = MockHumiditySensor()
        relay = MockRelay()
    else:
        raise RuntimeError(f"HARDWARE={hardware} not implemented yet")
    return Controller(sensor, relay)


def create_app() -> Flask:
    app = Flask(__name__)

    controller = build_controller()
    controller.start()
    app.register_blueprint(create_blueprint(controller))

    @app.get("/")
    def index():
        return jsonify({
            "name": "humidifier-iot",
            "version": "0.1.0",
            "hardware": os.environ.get("HARDWARE", "mock"),
            "api_root": "/api/status",
        })

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
