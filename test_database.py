#!/usr/bin/env python3
"""测试PostgreSQL数据库连接和基本操作"""

import asyncio
import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import test_db_connection, init_database
from backend.db_service import ConversationService, MessageService, KnowledgeService

async def test_database_operations():
    """测试数据库基本操作"""
    print("🧪 测试PostgreSQL数据库操作...")

    # 测试连接
    if not await test_db_connection():
        print("❌ 数据库连接失败，请检查PostgreSQL是否运行")
        return

    try:
        # 初始化数据库
        await init_database()

        # 测试创建对话
        print("\n📝 测试创建对话...")
        from backend.database import get_async_db

        async for db in get_async_db():
            # 创建测试对话
            conversation = await ConversationService.create_conversation(
                db,
                title="测试对话 - 数据库集成"
            )
            print(f"✅ 创建对话成功: {conversation.id} - {conversation.title}")

            # 创建用户消息
            user_message = await MessageService.create_message(
                db,
                conversation_id=conversation.id,
                role="user",
                content="什么是Python？请简单介绍一下。"
            )
            print(f"✅ 创建用户消息成功: {user_message.id}")

            # 创建助手消息
            assistant_message = await MessageService.create_message(
                db,
                conversation_id=conversation.id,
                role="assistant",
                content="Python是一种高级编程语言...",
                stage1_responses=[
                    {"model": "openai/gpt-4", "response": "Python是Guido van Rossum创建的编程语言"},
                    {"model": "anthropic/claude-3", "response": "Python是一种解释型、高级编程语言"}
                ],
                stage2_rankings=[
                    {"model": "openai/gpt-4", "ranking": "1. Response A\\n2. Response B"}
                ],
                stage3_response={
                    "model": "gemini/gemini-pro",
                    "response": "综合来看，Python是一种简洁而强大的编程语言"
                }
            )
            print(f"✅ 创建助手消息成功: {assistant_message.id}")

            # 创建知识库条目
            knowledge_entry = await KnowledgeService.create_knowledge_entry(
                db,
                title="Python编程语言介绍",
                content="Python是一种简洁的高级编程语言，由Guido van Rossum于1991年首次发布。它具有清晰的语法和丰富的标准库，广泛应用于Web开发、数据科学、人工智能等领域。",
                conversation_id=conversation.id,
                message_id=assistant_message.id,
                tags=["Python", "编程语言", "入门教程"]
            )
            print(f"✅ 创建知识库条目成功: {knowledge_entry.id}")

            # 测试查询
            print("\n🔍 测试查询操作...")
            conversations = await ConversationService.list_conversations(db)
            print(f"✅ 查询到 {len(conversations)} 个对话")

            knowledge_entries = await KnowledgeService.list_knowledge_entries(db)
            print(f"✅ 查询到 {len(knowledge_entries)} 个知识库条目")

            # 测试搜索
            search_results = await KnowledgeService.search_knowledge_entries(db, "Python")
            print(f"✅ 搜索'Python'找到 {len(search_results)} 个结果")

            print("\n🎉 数据库操作测试全部通过！")
            break

    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_database_operations())