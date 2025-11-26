#!/usr/bin/env python3
"""测试各个API服务的连接性"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.openrouter import query_model

async def test_all_models():
    """测试所有配置的模型"""

    # 测试消息
    test_messages = [
        {"role": "user", "content": "请用一句话回答：1+1等于多少？"}
    ]

    # 测试模型列表
    test_models = [
        "openrouter:x-ai/grok-4.1-fast:free",
        "deepseek:deepseek-chat",
        "moonshot:moonshot-v1-8k",
        "zhipu:glm-4.6"
    ]

    print("🧪 开始测试各个API服务...\n")

    for model in test_models:
        print(f"📡 测试模型: {model}")
        try:
            response = await query_model(model, test_messages, timeout=30.0)
            if response and response.get('content'):
                content = response['content'][:100] + "..." if len(response['content']) > 100 else response['content']
                print(f"✅ 成功: {content}")
            else:
                print(f"❌ 失败: 无响应内容")
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_all_models())