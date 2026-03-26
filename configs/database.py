from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from configs import settings


DATABASE_URL = settings.APP_DB_CONNECTION_STRING or "sqlite:///./app.db"


def _build_engine():
    engine_kwargs = {
        "future": True,
        "pool_pre_ping": True,
    }

    if DATABASE_URL.startswith("sqlite"):
        # SQLite needs this flag when used from FastAPI request handlers.
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    else:
        # QueuePool is enabled by default for non-SQLite databases; these
        # settings make the pool behavior explicit for production workloads.
        engine_kwargs["pool_size"] = 5
        engine_kwargs["max_overflow"] = 10
        engine_kwargs["pool_recycle"] = 1800

    return create_engine(DATABASE_URL, **engine_kwargs)


engine = _build_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a SQLAlchemy session per request and
    guarantees the session is closed afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBSession = Annotated[Session, Depends(get_db)]
