"""PostgreSQL database configuration and models."""

import os
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, Column, String, DateTime, Text, JSON, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import psycopg2

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:3f342bb206@localhost/llm_council"
)

# Async database URL for SQLAlchemy async
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create base model class
Base = declarative_base()

class Conversation(Base):
    """对话模型"""
    __tablename__ = "conversations"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    message_count = Column(Integer, default=0)

class Message(Base):
    """消息模型"""
    __tablename__ = "messages"

    id = Column(String, primary_key=True)
    conversation_id = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Assistant message specific fields
    stage1_responses = Column(JSON, nullable=True)
    stage2_rankings = Column(JSON, nullable=True)
    stage2_metadata = Column(JSON, nullable=True)
    stage3_response = Column(JSON, nullable=True)

    # Processing state
    loading_stage1 = Column(String, default='pending')
    loading_stage2 = Column(String, default='pending')
    loading_stage3 = Column(String, default='pending')

class KnowledgeEntry(Base):
    """知识库条目模型"""
    __tablename__ = "knowledge_entries"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    conversation_id = Column(String, nullable=True)  # 来源对话ID
    message_id = Column(String, nullable=True)  # 来源消息ID
    tags = Column(JSON, nullable=True)  # 标签列表
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    view_count = Column(Integer, default=0)

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default='user')  # 'admin', 'user'
    is_active = Column(String, default='true')
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

# Database engines
engine = create_engine(DATABASE_URL, echo=False)
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

def create_tables():
    """创建数据库表"""
    Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    """获取同步数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db() -> AsyncSession:
    """获取异步数据库会话"""
    async with AsyncSessionLocal() as session:
        yield session

async def init_database():
    """初始化数据库"""
    try:
        # 测试数据库连接
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            await session.commit()

        # 创建表
        create_tables()
        print("✅ PostgreSQL数据库初始化成功")

    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        raise

# 测试数据库连接
async def test_db_connection():
    """测试数据库连接"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute("SELECT version()")
            version = result.scalar()
            print(f"✅ 数据库连接成功: {version}")
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False