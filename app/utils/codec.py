import ast
import json
from typing import Any


def format_number(number: int) -> str:
    if number >= 1000:
        return f"{number:,}".replace(",", ".")
    return str(number)


def _encode_bytes(obj: Any) -> Any:
    match obj:
        case dict():
            return {k: _encode_bytes(v) for k, v in obj.items()}
        case list():
            return [_encode_bytes(v) for v in obj]
        case bytes():
            return repr(obj)
        case _:
            return obj


def _decode_bytes(obj: Any) -> Any:
    match obj:
        case dict():
            return {k: _decode_bytes(v) for k, v in obj.items()}
        case list():
            return [_decode_bytes(v) for v in obj]
        case str() if len(obj) >= 3 and obj[0] == "b" and obj[1] in ("'", '"'):
            try:
                result = ast.literal_eval(obj)
                return result if isinstance(result, bytes) else obj
            except Exception:
                return obj
        case _:
            return obj


def serialize_json(data: dict[str, Any] | None) -> str | None:
    if not data:
        return None
    return json.dumps(_encode_bytes(data), ensure_ascii=False)


def deserialize_json(data_str: str | None) -> dict[str, Any]:
    if not data_str:
        return {}
    return _decode_bytes(json.loads(data_str))  # type: ignore[no-any-return]
