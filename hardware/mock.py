"""Mock-реализации для разработки без реального железа.

MockHumiditySensor выдаёт правдоподобно меняющееся значение (random walk).
MockRelay печатает события переключения в stdout.
"""
import random

from hardware.base import HumiditySensor, Relay


class MockHumiditySensor(HumiditySensor):
    def __init__(self, initial: float = 50.0):
        self._value = initial

    def read(self) -> float:
        self._value += random.uniform(-1.5, 1.5)
        self._value = max(30.0, min(70.0, self._value))
        return round(self._value, 1)


class MockRelay(Relay):
    def __init__(self):
        self._state = False

    def set(self, on: bool) -> None:
        if on != self._state:
            self._state = on
            print(f"[MOCK RELAY] {'ON' if on else 'OFF'}")

    def get(self) -> bool:
        return self._state
