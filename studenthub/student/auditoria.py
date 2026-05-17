import json
import logging
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path


_SENSITIVE_KEYS = {"password", "token", "csrfmiddlewaretoken", "secret"}


def _build_audit_logger() -> logging.Logger:
    logger = logging.getLogger("student.audit")
    if logger.handlers:
        return logger

    base_dir = Path(__file__).resolve().parent.parent
    logs_dir = base_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(logs_dir / "auditoria.log", encoding="utf-8")
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(message)s"))

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


AUDIT_LOGGER = _build_audit_logger()


def _safe_post_data(request):
    if request.method != "POST":
        return {}

    cleaned = {}
    for key, value in request.POST.items():
        if key.lower() in _SENSITIVE_KEYS:
            cleaned[key] = "*"
        else:
            cleaned[key] = value
    return cleaned


def _client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def audit_crud(action: str, resource: str):
    """Decorator for auditing CRUD views with structured JSON logs."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            start = datetime.now(timezone.utc)
            status = "ok"
            status_code = 200
            error_message = None

            try:
                response = view_func(request, *args, **kwargs)
                status_code = getattr(response, "status_code", 200)
                if status_code >= 400:
                    status = "error"
                return response
            except Exception as exc:
                status = "error"
                status_code = 500
                error_message = str(exc)
                raise
            finally:
                end = datetime.now(timezone.utc)
                duration_ms = int((end - start).total_seconds() * 1000)

                user_repr = "anonymous"
                user = getattr(request, "user", None)
                if user and getattr(user, "is_authenticated", False):
                    user_repr = str(user)

                event = {
                    "timestamp": end.isoformat(),
                    "action": action,
                    "resource": resource,
                    "status": status,
                    "status_code": status_code,
                    "path": request.path,
                    "method": request.method,
                    "ip": _client_ip(request),
                    "user": user_repr,
                    "params": kwargs,
                    "payload": _safe_post_data(request),
                    "duration_ms": duration_ms,
                }

                if error_message:
                    event["error"] = error_message

                AUDIT_LOGGER.info(json.dumps(event, ensure_ascii=True))

        return wrapper

    return decorator