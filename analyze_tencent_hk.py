#!/usr/bin/env python3
"""
腾讯股票完整分析 - 使用香港股票代码获取更完整的数据
"""
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv
import sys

load_dotenv()

print("🚀 腾讯控股 (0700.HK) 完整分析")
print("=" * 80)

# 配置
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "anthropic"
config["deep_think_llm"] = "claude-sonnet-4-6"
config["quick_think_llm"] = "claude-haiku-4-5"
config["max_debate_rounds"] = 3                      # 3 轮深度辩论
config["max_risk_discuss_rounds"] = 2
config["output_language"] = "Chinese"
config["checkpoint_enabled"] = True

print("📋 分析配置:")
print(f"  • 股票代码: 0700.HK (腾讯控股 - 香港交易所)")
print(f"  • 辩论轮数: {config['max_debate_rounds']} 轮（深度分析）")
print(f"  • 风险讨论: {config['max_risk_discuss_rounds']} 轮")
print(f"  • 输出语言: 中文")
print("=" * 80)

# 初始化
print("\n🔧 初始化 TradingAgents...")
ta = TradingAgentsGraph(debug=True, config=config)
print("✅ 初始化成功！")

# 分析参数
ticker = "0700.HK"  # 香港交易所代码
analysis_date = "2024-03-15"  # 使用较早的日期

print(f"\n📈 分析目标: {ticker}")
print(f"📅 分析日期: {analysis_date}")
print("\n⏳ 开始深度分析（预计 10-15 分钟）...")
print("=" * 80)

try:
    state, decision = ta.propagate(ticker, analysis_date)

    print("\n" + "=" * 80)
    print("✅ 分析完成！")
    print("=" * 80)
    print("\n📝 交易决策:")
    print(decision)
    print("=" * 80)

    # 保存结果
    with open("tencent_0700HK_analysis.txt", "w", encoding="utf-8") as f:
        f.write(f"腾讯控股 (0700.HK) 分析报告\n")
        f.write(f"分析日期: {analysis_date}\n")
        f.write("=" * 80 + "\n\n")
        f.write(str(decision))

    print("\n💾 报告已保存: tencent_0700HK_analysis.txt")
    print("🎉 分析完成！")

except Exception as e:
    print(f"\n❌ 错误: {e}")
    print("\n💡 建议: 等待几分钟后重试，或使用 TCEHY 代码")
    sys.exit(1)
