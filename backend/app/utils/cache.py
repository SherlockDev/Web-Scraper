from datetime import datetime, timedelta
from typing import Any


class TTLCache:
    def __init__(self, ttl_seconds: int):
        self.ttl_seconds = ttl_seconds
        self._store: dict[str, tuple[datetime, Any]] = {}

    def get(self, key: str) -> Any | None:
        value = self._store.get(key)
        if value is None:
            return None

        expires_at, payload = value
        if datetime.utcnow() > expires_at:
            self._store.pop(key, None)
            return None

        return payload

    def set(self, key: str, payload: Any) -> None:
        self._store[key] = (datetime.utcnow() + timedelta(seconds=self.ttl_seconds), payload)
