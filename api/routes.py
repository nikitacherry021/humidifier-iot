"""HTTP API для управления контроллером увлажнителя."""
from flask import Blueprint, jsonify, request

from core.controller import Controller


def create_blueprint(controller: Controller) -> Blueprint:
    bp = Blueprint("api", __name__, url_prefix="/api")

    @bp.get("/status")
    def status():
        return jsonify(controller.status())

    @bp.get("/humidity")
    def humidity():
        s = controller.status()
        return jsonify({"humidity": s["humidity"], "error": s["error"]})

    @bp.post("/mode")
    def set_mode():
        data = request.get_json(silent=True) or {}
        try:
            controller.set_mode(data.get("mode"))
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify(controller.status())

    @bp.post("/thresholds")
    def set_thresholds():
        data = request.get_json(silent=True) or {}
        try:
            controller.set_thresholds(
                float(data.get("on_below")),
                float(data.get("off_above")),
            )
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify(controller.status())

    return bp
