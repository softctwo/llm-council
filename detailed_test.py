#!/usr/bin/env python3
"""详细测试LLM Council系统 - 显示详细错误信息"""

import asyncio
import httpx
import json
import traceback

async def detailed_test():
    """详细测试系统功能"""
    print("🔍 详细测试LLM Council系统...")

    async with httpx.AsyncClient(timeout=300.0) as client:
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
                print(f"✅ 对话创建成功: {conversation_id}")
            else:
                print(f"❌ 创建对话失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                return
        except Exception as e:
            print(f"❌ 创建对话异常: {e}")
            traceback.print_exc()
            return

        # 3. 发送测试消息（非流式）
        print("3. 发送测试消息...")
        try:
            message_data = {"content": "请用一句话解释什么是Python"}
            print(f"   发送消息: {message_data['content']}")

            response = await client.post(
                f"http://localhost:8001/api/conversations/{conversation_id}/message",
                json=message_data
            )

            print(f"   响应状态码: {response.status_code}")
            print(f"   响应头: {dict(response.headers)}")

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
                try:
                    error_json = response.json()
                    print(f"   详细错误: {json.dumps(error_json, indent=2)}")
                except:
                    pass

        except httpx.TimeoutException:
            print("❌ 请求超时 - 这可能是模型处理时间过长")
        except Exception as e:
            print(f"❌ 消息处理异常: {e}")
            traceback.print_exc()

        print("\n🎉 测试完成！")

if __name__ == "__main__":
    asyncio.run(detailed_test())