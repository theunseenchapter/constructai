# Optional database imports
try:
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
    from sqlalchemy import create_engine
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    AsyncSession = None
    create_async_engine = None
    async_sessionmaker = None
    declarative_base = None
    DeclarativeBase = None
    sessionmaker = None
    Session = None
    create_engine = None

from core.config import settings

if DATABASE_AVAILABLE:
    # Create async engine
    engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
        future=True
    )

    # Create async session factory
    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    # Create synchronous engine for pricing system
    sync_database_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    sync_engine = create_engine(sync_database_url, echo=settings.debug)
    SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
else:
    engine = None
    AsyncSessionLocal = None
    sync_engine = None
    SyncSessionLocal = None

# Base class for models
if DATABASE_AVAILABLE:
    class Base(DeclarativeBase):
        pass
else:
    Base = None

# Dependency to get database session
async def get_db():
    if not DATABASE_AVAILABLE or AsyncSessionLocal is None:
        yield None
        return
        
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

# Dependency to get synchronous database session for pricing system
def get_sync_db():
    if not DATABASE_AVAILABLE or SyncSessionLocal is None:
        return None
        
    db = SyncSessionLocal()
    try:
        return db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
