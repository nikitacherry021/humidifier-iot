"""Контроллер: опрашивает датчик, реализует логику режимов и гистерезис."""
import threading
import time

from core import config
from hardware.base import HumiditySensor, Relay


class Controller:
    def __init__(self, sensor: HumiditySensor, relay: Relay):
        self.sensor = sensor
        self.relay = relay
        self.mode = config.MODE
        self.on_below = config.ON_BELOW
        self.off_above = config.OFF_ABOVE
        self.last_switch = 0.0
        self.last_humidity = None
        self.last_error = None
        self._stop = threading.Event()
        self._thread = None

    # --- жизненный цикл ---

    def start(self) -> None:
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def _loop(self) -> None:
        while not self._stop.is_set():
            self._tick()
            time.sleep(config.POLL_INTERVAL)

    def _tick(self) -> None:
        # 1) чтение датчика
        try:
            self.last_humidity = self.sensor.read()
            self.last_error = None
        except Exception as exc:  # noqa: BLE001
            self.last_error = str(exc)
            self.last_humidity = None
            # безопасное состояние
            self.relay.set(False)
            return

        # 2) режимы
        if self.mode == "on":
            self.relay.set(True)
            return
        if self.mode == "off":
            self.relay.set(False)
            return

        # 3) auto с гистерезисом
        now = time.monotonic()
        if now - self.last_switch < config.MIN_SWITCH_INTERVAL:
            return
        current = self.relay.get()
        if not current and self.last_humidity < self.on_below:
            self.relay.set(True)
            self.last_switch = now
        elif current and self.last_humidity > self.off_above:
            self.relay.set(False)
            self.last_switch = now

    # --- управление из API ---

    def set_mode(self, mode: str) -> None:
        if mode not in ("auto", "on", "off"):
            raise ValueError("mode must be one of: auto, on, off")
        self.mode = mode

    def set_thresholds(self, on_below: float, off_above: float) -> None:
        if not (0 <= on_below < off_above <= 100):
            raise ValueError("require 0 <= on_below < off_above <= 100")
        self.on_below = float(on_below)
        self.off_above = float(off_above)

    def status(self) -> dict:
        return {
            "humidity": self.last_humidity,
            "mode": self.mode,
            "relay": self.relay.get(),
            "on_below": self.on_below,
            "off_above": self.off_above,
            "error": self.last_error,
        }
