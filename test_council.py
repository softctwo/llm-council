#!/usr/bin/env python3
"""测试LLM Council完整工作流程"""

import asyncio
import sys
import os
import httpx
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.council import stage1_collect_responses, stage2_collect_rankings, stage3_synthesize_final

async def test_council_workflow():
    """测试完整的LLM Council工作流程"""

    print("🏛️  开始测试LLM Council完整工作流程...\n")

    # 测试用户问题
    user_question = "请解释什么是人工智能，并举例说明其应用场景。"
    print(f"❓ 用户问题: {user_question}\n")

    try:
        # Stage 1: 收集各模型的初始回答
        print("🔄 Stage 1: 收集各模型的初始回答...")
        stage1_results = await stage1_collect_responses(user_question)

        print(f"✅ 收集到 {len(stage1_results)} 个有效回答:")
        for result in stage1_results:
            content = result['response'][:100] + "..." if len(result['response']) > 100 else result['response']
            print(f"   📝 {result['model']}: {content}")
        print()

        # Stage 2: 匿名评审阶段
        print("🔄 Stage 2: 匿名评审阶段...")
        rankings, label_to_model = await stage2_collect_rankings(user_question, stage1_results)

        print(f"✅ 收集到 {len(rankings)} 个评审:")
        for i, ranking in enumerate(rankings):
            if ranking:
                print(f"   🎯 评审者 {i+1}: {ranking.get('parsed_ranking', [])}")
        print()

        print(f"📋 标签映射: {label_to_model}\n")

        # Stage 3: 最终综合
        print("🔄 Stage 3: 主席综合最终回答...")
        final_response = await stage3_synthesize_final(user_question, stage1_results, rankings)

        if final_response:
            print("✅ 最终综合回答:")
            print(f"   🎖️  {final_response['response'][:200]}...")
        else:
            print("❌ 最终综合失败")

    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

async def test_api_endpoint():
    """测试API端点"""
    print("\n🌐 测试API端点...")

    try:
        async with httpx.AsyncClient() as client:
            # 创建新对话
            create_response = await client.post("http://localhost:8001/api/conversations", json={})
            if create_response.status_code == 200:
                conversation_id = create_response.json()["id"]
                print(f"✅ 创建对话成功: {conversation_id}")

                # 发送消息
                message_data = {"content": "什么是机器学习？"}
                msg_response = await client.post(
                    f"http://localhost:8001/api/conversations/{conversation_id}/message",
                    json=message_data
                )

                try:
                    if msg_response.status_code == 200:
                        result = msg_response.json()
                        print("✅ API端点测试成功")
                        print(f"   📊 Stage 1: {len(result['stage1'])} 个响应")
                        print(f"   🎯 Stage 2: {len(result['stage2'])} 个评审")
                        print(f"   🎖️  Stage 3: {'有' if result['stage3'] else '无'} 综合回答")
                        if result.get('metadata'):
                            print(f"   📋 元数据: {list(result['metadata'].keys())}")
                    else:
                        print(f"❌ 消息发送失败: {msg_response.status_code}")
                        print(f"   错误信息: {msg_response.text}")
                except Exception as msg_error:
                    print(f"❌ 处理消息响应时出错: {str(msg_error)}")
            else:
                print(f"❌ 创建对话失败: {create_response.status_code}")
                print(f"   错误信息: {create_response.text}")

    except Exception as e:
        print(f"❌ API测试失败: {str(e)}")

if __name__ == "__main__":
    async def main():
        await test_council_workflow()
        await test_api_endpoint()

    asyncio.run(main())