# Humidifier IoT

Программный IoT-контроллер увлажнителя воздуха с REST API.

## Идея

Устройство измеряет влажность воздуха и автоматически включает/выключает
увлажнитель через реле. Управление и мониторинг — через HTTP API, что позволяет
подключить Android-приложение или любой другой клиент.

## Целевая платформа

- **Hardware**: Raspberry Pi + датчик влажности (SHT31 / BME280 / DHT22) + реле/MOSFET.
- **OS**: Raspberry Pi OS (или другая Unix-like система).
- **Разработка и проверка**: любая Unix-like система (например, Alt Linux) в режиме
  имитации железа (mock mode). Реальный датчик и реле не требуются.

## Архитектура

sensor -> Controller -> relay
              |
              v
         REST API (Flask)
              |
              v
       Android / curl / Postman

- `hardware/` — интерфейсы `HumiditySensor` и `Relay` и их реализации
  (`mock.py` для разработки, `raspberry.py` — для будущего железа).
- `core/` — логика: конфиг, контроллер с гистерезисом, режимы.
- `api/` — HTTP эндпоинты.
- `storage/` — настройки и история (появится позже).

## Режимы работы

- `auto` — включение при влажности ниже `on_below`, выключение выше `off_above`.
- `on` — увлажнитель включён постоянно.
- `off` — увлажнитель выключен.

## Запланированное API

- `GET  /api/status` — текущая влажность, режим, состояние реле, пороги.
- `GET  /api/humidity` — только влажность.
- `POST /api/mode` — переключение режима (`auto` / `on` / `off`).
- `POST /api/thresholds` — установка порогов.

## План развития

1. Базовый API + mock режим.
2. Сохранение настроек в `storage/settings.json`.
3. Логирование влажности в CSV, эндпоинт `/api/history`.
4. Тесты для логики гистерезиса.
5. Реализация `hardware/raspberry.py` (для будущего запуска на Pi).
6. Android-приложение (следующий семестр).

## Как запустить (mock mode)

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python app.py

В другом терминале:

    curl http://localhost:5000/api/status
    curl -X POST http://localhost:5000/api/mode \
      -H "Content-Type: application/json" -d '{"mode": "auto"}'
    curl -X POST http://localhost:5000/api/thresholds \
      -H "Content-Type: application/json" -d '{"on_below": 45, "off_above": 55}'
