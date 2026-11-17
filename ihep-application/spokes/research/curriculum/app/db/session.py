"""
Database engine and declarative base

``app.main`` uses ``engine`` (async) and ``Base`` to create tables when
ENVIRONMENT == "test". asyncpg is the async PostgreSQL driver pinned in
requirements.txt, so a plain ``postgresql://`` URL is mapped to it.
The engine connects lazily; nothing connects at import time.
"""

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


def _async_url(url: str) -> str:
    for prefix in ("postgresql://", "postgres://"):
        if url.startswith(prefix):
            return "postgresql+asyncpg://" + url[len(prefix):]
    return url


class Base(DeclarativeBase):
    """Declarative base for ORM models."""


engine = create_async_engine(
    _async_url(settings.DATABASE_URL),
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
)
