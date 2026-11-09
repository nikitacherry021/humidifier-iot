"""Абстрактные интерфейсы аппаратных компонентов.

Реальные реализации — в hardware/raspberry.py (появится позже),
для разработки без железа — hardware/mock.py.
"""
from abc import ABC, abstractmethod


class HumiditySensor(ABC):
    @abstractmethod
    def read(self) -> float:
        """Вернуть влажность в процентах (0..100).

        При ошибке чтения — выбросить исключение.
        """


class Relay(ABC):
    @abstractmethod
    def set(self, on: bool) -> None:
        """Включить (True) или выключить (False) реле."""

    @abstractmethod
    def get(self) -> bool:
        """Вернуть текущее состояние реле."""
