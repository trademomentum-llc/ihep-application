"""
Application exceptions

Base exception for the IHEP Curriculum API. ``app.main`` registers a handler
that renders it as ``{"error": error_code, "message": message, "detail": detail}``
with ``status_code`` as the HTTP status.
"""

from typing import Any, Optional


class IHEPException(Exception):
    """Base class for errors the API returns to clients in a structured form."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 400,
        error_code: str = "IHEP_ERROR",
        detail: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.detail = detail
