#!/usr/bin/env python3
"""
腾讯股票详细分析 - 包含完整的分析流程和结果展示
"""
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv
import sys
import json
from datetime import datetime

# 加载环境变量
load_dotenv()

print("🚀 TradingAgents - 腾讯股票深度分析")
print("=" * 80)

# 配置 TradingAgents
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "anthropic"
config["deep_think_llm"] = "claude-sonnet-4-6"
config["quick_think_llm"] = "claude-haiku-4-5"
config["max_debate_rounds"] = 2                      # 2 轮辩论
config["max_risk_discuss_rounds"] = 2                # 2 轮风险讨论
config["output_language"] = "Chinese"
config["checkpoint_enabled"] = True                  # 启用检查点

print("📋 分析配置:")
print(f"  • 公司: 腾讯控股 (Tencent Holdings)")
print(f"  • LLM 提供商: Anthropic Claude")
print(f"  • 深度思考模型: {config['deep_think_llm']}")
print(f"  • 快速思考模型: {config['quick_think_llm']}")
print(f"  • 辩论轮数: {config['max_debate_rounds']}")
print(f"  • 风险讨论轮数: {config['max_risk_discuss_rounds']}")
print(f"  • 输出语言: {config['output_language']}")
print(f"  • 检查点恢复: {'启用' if config['checkpoint_enabled'] else '禁用'}")
print("=" * 80)

# 初始化
print("\n🔧 初始化 TradingAgents...")
try:
    ta = TradingAgentsGraph(debug=True, config=config)
    print("✅ 初始化成功！")
except Exception as e:
    print(f"❌ 初始化失败: {e}")
    sys.exit(1)

# 腾讯股票信息
print("\n" + "=" * 80)
print("📊 腾讯控股 (Tencent Holdings Limited)")
print("=" * 80)
print("  • 公司简介: 中国领先的互联网增值服务提供商")
print("  • 主营业务: 社交网络、游戏、金融科技、云服务、广告")
print("  • 核心产品: 微信/WeChat、QQ、王者荣耀、和平精英")
print("  • 上市地点: 香港交易所 (0700.HK)")
print("  • 美国 ADR: TCEHY (OTC)")
print("=" * 80)

# 选择股票代码和日期
ticker = "TCEHY"  # 使用美国 ADR
analysis_date = "2024-03-20"  # 使用较早的日期

print(f"\n📈 分析目标:")
print(f"  • 股票代码: {ticker}")
print(f"  • 分析日期: {analysis_date}")
print("=" * 80)

print("\n⏳ 开始深度分析...")
print("\n分析流程:")
print("  1️⃣  数据收集 - 获取股价、财务、新闻、技术指标")
print("  2️⃣  基础分析 - 评估公司财务健康状况")
print("  3️⃣  情绪分析 - 分析市场情绪和社交媒体")
print("  4️⃣  新闻分析 - 解读新闻事件影响")
print("  5️⃣  技术分析 - 识别技术形态和趋势")
print("  6️⃣  研究员辩论 - 多空双方深度讨论")
print("  7️⃣  交易决策 - 综合所有信息做出决策")
print("  8️⃣  风险评估 - 评估市场风险和流动性")
print("  9️⃣  最终决策 - 投资组合经理批准/拒绝")
print("\n" + "=" * 80)
print("⏱️  预计耗时: 5-10 分钟")
print("=" * 80)

try:
    # 运行分析
    state, decision = ta.propagate(ticker, analysis_date)

    print("\n" + "=" * 80)
    print("✅ 分析完成！")
    print("=" * 80)

    # 显示详细结果
    print("\n" + "=" * 80)
    print("📝 腾讯股票交易决策报告")
    print("=" * 80)
    print(f"\n股票代码: {ticker}")
    print(f"分析日期: {analysis_date}")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "-" * 80)
    print("最终决策:")
    print("-" * 80)
    print(decision)
    print("=" * 80)

    # 尝试提取更多信息
    if state:
        print("\n" + "=" * 80)
        print("📊 分析过程详情")
        print("=" * 80)

        # 显示可用的状态信息
        if hasattr(state, 'keys'):
            available_keys = [k for k in state.keys() if not k.startswith('_')]
            print(f"\n可用信息: {', '.join(available_keys)}")

            # 尝试显示一些关键信息
            if 'messages' in state:
                print(f"\n消息数量: {len(state['messages'])}")

            if 'analyst_reports' in state:
                print("\n分析师报告已生成")

            if 'research_reports' in state:
                print("研究员报告已生成")

    # 保存详细结果
    report = f"""
{'=' * 80}
腾讯股票深度分析报告
{'=' * 80}

公司信息:
  • 公司名称: 腾讯控股有限公司 (Tencent Holdings Limited)
  • 股票代码: {ticker}
  • 分析日期: {analysis_date}
  • 报告生成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

分析配置:
  • LLM 提供商: Anthropic Claude
  • 深度思考模型: {config['deep_think_llm']}
  • 快速思考模型: {config['quick_think_llm']}
  • 辩论轮数: {config['max_debate_rounds']}
  • 风险讨论轮数: {config['max_risk_discuss_rounds']}

{'=' * 80}
最终交易决策
{'=' * 80}

{decision}

{'=' * 80}
分析说明
{'=' * 80}

本报告由 TradingAgents 多智能体系统生成，综合了以下分析维度：

1. 基础面分析 - 公司财务健康状况、盈利能力、成长性
2. 技术面分析 - 价格趋势、技术指标、支撑阻力位
3. 情绪分析 - 市场情绪、社交媒体讨论、投资者信心
4. 新闻分析 - 重大新闻事件、行业动态、监管政策
5. 风险评估 - 市场风险、流动性风险、特定风险

多空双方研究员进行了 {config['max_debate_rounds']} 轮深度辩论，
风险管理团队进行了 {config['max_risk_discuss_rounds']} 轮风险讨论。

{'=' * 80}
免责声明
{'=' * 80}

本报告仅供研究和教育目的，不构成投资建议。
投资有风险，决策需谨慎。请在充分了解风险的前提下做出投资决策。

{'=' * 80}
"""

    with open("tencent_detailed_analysis.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print("\n💾 详细分析报告已保存到: tencent_detailed_analysis.txt")

    print("\n" + "=" * 80)
    print("🎉 腾讯股票深度分析完成！")
    print("=" * 80)
    print("\n📁 生成的文件:")
    print("  • tencent_detailed_analysis.txt - 完整分析报告")
    print("\n💡 建议:")
    print("  • 查看完整报告了解详细分析过程")
    print("  • 结合其他信息源进行综合判断")
    print("  • 定期更新分析以跟踪最新情况")
    print("=" * 80)

except KeyboardInterrupt:
    print("\n\n⚠️  分析被用户中断")
    print("💡 提示: 由于启用了检查点，下次运行将从中断处继续")
    sys.exit(0)

except Exception as e:
    print("\n" + "=" * 80)
    print(f"❌ 分析失败: {e}")
    print("=" * 80)

    import traceback
    print("\n详细错误信息:")
    print(traceback.format_exc())

    print("\n可能的原因:")
    print("  1. Yahoo Finance 速率限制（等待 5-10 分钟后重试）")
    print("  2. 股票代码不正确或数据不可用")
    print("  3. 网络连接问题")
    print("  4. API 配额不足")
    print("\n💡 解决建议:")
    print("  • 等待几分钟后重新运行")
    print("  • 尝试使用香港代码: 0700.HK")
    print("  • 检查网络连接和 API 配置")
    print("  • 查看上面的详细错误信息")
    sys.exit(1)
