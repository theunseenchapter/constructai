from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from ..models import User
from ..schemas import UserCreate, UserUpdate
from ..core.security import get_password_hash

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """Get user by ID"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """Get user by username"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Get user by email"""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(user_data.password)
    
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate) -> Optional[User]:
    """Update user"""
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalars().first()
    
    if not db_user:
        return None
    
    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """Delete user"""
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalars().first()
    
    if not db_user:
        return False
    
    await db.delete(db_user)
    await db.commit()
    return True
