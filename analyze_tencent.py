#!/usr/bin/env python3
"""
使用 TradingAgents 分析腾讯股票
"""
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv
import sys

# 加载环境变量
load_dotenv()

print("🚀 TradingAgents - 腾讯股票分析")
print("=" * 70)

# 配置 TradingAgents 使用 Anthropic Claude
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "anthropic"
config["deep_think_llm"] = "claude-sonnet-4-6"      # 复杂推理
config["quick_think_llm"] = "claude-haiku-4-5"      # 快速任务
config["max_debate_rounds"] = 2                      # 2 轮辩论（标准深度）
config["max_risk_discuss_rounds"] = 1
config["output_language"] = "Chinese"                # 中文输出

print("📋 配置信息:")
print(f"  • LLM 提供商: {config['llm_provider']}")
print(f"  • 深度思考模型: {config['deep_think_llm']}")
print(f"  • 快速思考模型: {config['quick_think_llm']}")
print(f"  • 辩论轮数: {config['max_debate_rounds']}")
print(f"  • 输出语言: {config['output_language']}")
print("=" * 70)

# 初始化 TradingAgents
print("\n🔧 初始化 TradingAgents...")
try:
    ta = TradingAgentsGraph(debug=True, config=config)
    print("✅ 初始化成功！")
except Exception as e:
    print(f"❌ 初始化失败: {e}")
    sys.exit(1)

# 腾讯股票代码选项
print("\n" + "=" * 70)
print("📊 腾讯股票代码选项:")
print("  1. 0700.HK  - 腾讯控股（香港交易所）")
print("  2. TCEHY    - 腾讯 ADR（美国 OTC）")
print("=" * 70)

# 使用美国 ADR 代码（yfinance 支持更好）
ticker = "TCEHY"
analysis_date = "2024-04-15"  # 使用较早的日期避免速率限制

print(f"\n📈 分析股票: {ticker} (腾讯控股)")
print(f"📅 分析日期: {analysis_date}")
print("=" * 70)
print("\n⏳ 正在运行分析，这可能需要 5-10 分钟...")
print("   流程: 数据收集 → 分析师报告 → 研究员辩论 → 交易决策 → 风险评估 → 最终决策")
print("\n" + "=" * 70)

try:
    # 运行分析
    _, decision = ta.propagate(ticker, analysis_date)

    print("\n" + "=" * 70)
    print("✅ 分析完成！")
    print("=" * 70)
    print("\n📝 腾讯股票交易决策:")
    print("=" * 70)
    print(decision)
    print("=" * 70)

    # 保存结果到文件
    with open("tencent_analysis.txt", "w", encoding="utf-8") as f:
        f.write(f"腾讯股票分析报告\n")
        f.write(f"股票代码: {ticker}\n")
        f.write(f"分析日期: {analysis_date}\n")
        f.write(f"=" * 70 + "\n\n")
        f.write(str(decision))

    print("\n💾 分析结果已保存到: tencent_analysis.txt")
    print("\n" + "=" * 70)
    print("🎉 腾讯股票分析完成！")
    print("=" * 70)

except Exception as e:
    print("\n" + "=" * 70)
    print(f"❌ 分析失败: {e}")
    print("=" * 70)
    print("\n可能的原因:")
    print("  1. Yahoo Finance 速率限制（等待 5-10 分钟后重试）")
    print("  2. 股票代码不正确")
    print("  3. 网络连接问题")
    print("  4. API 配额不足")
    print("\n💡 建议:")
    print("  • 等待几分钟后重新运行")
    print("  • 尝试使用香港代码: 0700.HK")
    print("  • 检查网络连接")
    sys.exit(1)
