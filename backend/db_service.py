"""数据库服务层，处理所有数据库操作"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete, func
from .database import (
    Conversation, Message, KnowledgeEntry, User,
    get_async_db
)

class ConversationService:
    """对话服务"""

    @staticmethod
    async def create_conversation(db: AsyncSession, title: str = None) -> Conversation:
        """创建新对话"""
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            id=conversation_id,
            title=title or "新对话",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        return conversation

    @staticmethod
    async def get_conversation(db: AsyncSession, conversation_id: str) -> Optional[Conversation]:
        """获取对话详情"""
        result = await db.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.id == conversation_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_conversations(db: AsyncSession) -> List[Conversation]:
        """获取对话列表"""
        result = await db.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .order_by(Conversation.updated_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def update_conversation_title(
        db: AsyncSession,
        conversation_id: str,
        title: str
    ) -> Optional[Conversation]:
        """更新对话标题"""
        result = await db.execute(
            update(Conversation)
            .where(Conversation.id == conversation_id)
            .values(title=title, updated_at=datetime.utcnow())
            .returning(Conversation)
        )
        await db.commit()
        return result.scalar_one_or_none()

    @staticmethod
    async def increment_message_count(db: AsyncSession, conversation_id: str):
        """增加对话消息计数"""
        await db.execute(
            update(Conversation)
            .where(Conversation.id == conversation_id)
            .values(
                message_count=Conversation.message_count + 1,
                updated_at=datetime.utcnow()
            )
        )
        await db.commit()

class MessageService:
    """消息服务"""

    @staticmethod
    async def create_message(
        db: AsyncSession,
        conversation_id: str,
        role: str,
        content: str,
        stage1_responses: List[Dict] = None,
        stage2_rankings: List[Dict] = None,
        stage2_metadata: Dict = None,
        stage3_response: Dict = None
    ) -> Message:
        """创建新消息"""
        message_id = str(uuid.uuid4())
        message = Message(
            id=message_id,
            conversation_id=conversation_id,
            role=role,
            content=content,
            stage1_responses=stage1_responses,
            stage2_rankings=stage2_rankings,
            stage2_metadata=stage2_metadata,
            stage3_response=stage3_response,
            created_at=datetime.utcnow()
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)

        # 更新对话消息计数
        await ConversationService.increment_message_count(db, conversation_id)

        return message

    @staticmethod
    async def update_message_stage(
        db: AsyncSession,
        message_id: str,
        stage: str,
        data: Dict
    ):
        """更新消息的阶段数据"""
        update_data = {
            f"stage{stage}_data": data,
            f"loading_stage{stage}": "completed"
        }

        if stage == 3:
            update_data["updated_at"] = datetime.utcnow()

        await db.execute(
            update(Message)
            .where(Message.id == message_id)
            .values(**update_data)
        )
        await db.commit()

    @staticmethod
    async def update_message_loading_state(
        db: AsyncSession,
        message_id: str,
        stage: str,
        state: str
    ):
        """更新消息加载状态"""
        await db.execute(
            update(Message)
            .where(Message.id == message_id)
            .values({f"loading_stage{stage}": state})
        )
        await db.commit()

class KnowledgeService:
    """知识库服务"""

    @staticmethod
    async def create_knowledge_entry(
        db: AsyncSession,
        title: str,
        content: str,
        conversation_id: str = None,
        message_id: str = None,
        tags: List[str] = None
    ) -> KnowledgeEntry:
        """创建知识库条目"""
        entry_id = str(uuid.uuid4())
        entry = KnowledgeEntry(
            id=entry_id,
            title=title,
            content=content,
            conversation_id=conversation_id,
            message_id=message_id,
            tags=tags or [],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(entry)
        await db.commit()
        await db.refresh(entry)
        return entry

    @staticmethod
    async def list_knowledge_entries(
        db: AsyncSession,
        limit: int = 50,
        offset: int = 0
    ) -> List[KnowledgeEntry]:
        """获取知识库条目列表"""
        result = await db.execute(
            select(KnowledgeEntry)
            .order_by(KnowledgeEntry.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    @staticmethod
    async def search_knowledge_entries(
        db: AsyncSession,
        query: str,
        limit: int = 20
    ) -> List[KnowledgeEntry]:
        """搜索知识库条目"""
        # 简单的文本搜索，实际项目中可能需要使用全文搜索
        result = await db.execute(
            select(KnowledgeEntry)
            .where(
                func.lower(KnowledgeEntry.title).contains(func.lower(query)) |
                func.lower(KnowledgeEntry.content).contains(func.lower(query))
            )
            .order_by(KnowledgeEntry.updated_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def increment_view_count(db: AsyncSession, entry_id: str):
        """增加查看次数"""
        await db.execute(
            update(KnowledgeEntry)
            .where(KnowledgeEntry.id == entry_id)
            .values(
                view_count=KnowledgeEntry.view_count + 1,
                updated_at=datetime.utcnow()
            )
        )
        await db.commit()

class UserService:
    """用户服务"""

    @staticmethod
    async def create_user(
        db: AsyncSession,
        username: str,
        email: str,
        password_hash: str,
        full_name: str = None,
        role: str = "user"
    ) -> User:
        """创建用户"""
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            role=role,
            is_active="true",
            created_at=datetime.utcnow()
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        result = await db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_last_login(db: AsyncSession, user_id: str):
        """更新最后登录时间"""
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(last_login=datetime.utcnow())
        )
        await db.commit()