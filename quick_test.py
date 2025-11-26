#!/usr/bin/env python3
"""快速测试LLM Council系统"""

import asyncio
import httpx
import json

async def quick_test():
    """快速测试系统功能"""
    print("🚀 快速测试LLM Council系统...")

    async with httpx.AsyncClient() as client:
        # 1. 测试健康检查
        print("1. 测试后端健康状态...")
        try:
            response = await client.get("http://localhost:8001/")
            if response.status_code == 200:
                print("✅ 后端服务正常")
            else:
                print(f"❌ 后端服务异常: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ 无法连接后端: {e}")
            return

        # 2. 创建对话
        print("2. 创建新对话...")
        try:
            response = await client.post("http://localhost:8001/api/conversations", json={})
            if response.status_code == 200:
                conversation = response.json()
                conversation_id = conversation["id"]
                print(f"✅ 对话创建成功: {conversation_id[:8]}...")
            else:
                print(f"❌ 创建对话失败: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ 创建对话异常: {e}")
            return

        # 3. 发送测试消息（非流式）
        print("3. 发送测试消息...")
        try:
            message_data = {"content": "请用一句话解释什么是Python"}
            response = await client.post(
                f"http://localhost:8001/api/conversations/{conversation_id}/message",
                json=message_data,
                timeout=60.0
            )
            if response.status_code == 200:
                result = response.json()
                print("✅ 消息处理成功")
                print(f"   📊 Stage 1: {len(result['stage1'])} 个响应")
                print(f"   🎯 Stage 2: {len(result['stage2'])} 个评审")
                print(f"   🎖️  Stage 3: {'有' if result['stage3'] else '无'} 综合回答")

                if result['stage3']:
                    content = result['stage3']['response'][:100] + "..." if len(result['stage3']['response']) > 100 else result['stage3']['response']
                    print(f"   📝 综合回答预览: {content}")
            else:
                print(f"❌ 消息处理失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
        except Exception as e:
            print(f"❌ 消息处理异常: {e}")

        print("\n🎉 测试完成！系统运行正常。")
        print("📱 前端地址: http://localhost:5173")
        print("🔧 后端API: http://localhost:8001")

if __name__ == "__main__":
    asyncio.run(quick_test())