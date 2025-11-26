#!/usr/bin/env python3
"""测试KIMI kimi-k2-thinking模型"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def test_kimi():
    """测试KIMI模型"""
    print("🧪 测试KIMI kimi-k2-thinking-turbo模型...")

    api_key = os.getenv("MOONSHOT_API_KEY")
    if not api_key:
        print("❌ 未找到MOONSHOT_API_KEY")
        return

    url = "https://api.moonshot.cn/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "kimi-k2-thinking-turbo",
        "messages": [
            {"role": "user", "content": "请用一句话解释什么是Python"}
        ],
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            print("   发送请求...")
            response = await client.post(url, headers=headers, json=payload)

            print(f"   响应状态码: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                message = data['choices'][0]['message']
                content = message.get('content', '')
                print("✅ KIMI模型响应成功")
                print(f"   📝 回答: {content[:200]}...")
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print(f"   错误信息: {response.text}")

    except httpx.TimeoutException:
        print("❌ KIMI模型响应超时")
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    asyncio.run(test_kimi())