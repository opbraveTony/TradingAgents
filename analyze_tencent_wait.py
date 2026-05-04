#!/usr/bin/env python3
"""
腾讯股票分析 - 使用更早的日期避免 API 速率限制
"""
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv
import sys
import time

load_dotenv()

print("🚀 腾讯控股深度分析")
print("=" * 80)

# 配置
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "anthropic"
config["deep_think_llm"] = "claude-sonnet-4-6"
config["quick_think_llm"] = "claude-haiku-4-5"
config["max_debate_rounds"] = 3
config["max_risk_discuss_rounds"] = 2
config["output_language"] = "Chinese"

print("📋 分析配置:")
print(f"  • 股票代码: 0700.HK (腾讯控股)")
print(f"  • 辩论轮数: 3 轮（深度分析）")
print(f"  • 输出语言: 中文")
print("=" * 80)

# 初始化
print("\n🔧 初始化 TradingAgents...")
ta = TradingAgentsGraph(debug=True, config=config)
print("✅ 初始化成功！")

# 使用更早的日期避免速率限制
ticker = "0700.HK"
analysis_date = "2024-01-15"  # 使用 2024 年初的数据

print(f"\n📈 分析目标: {ticker}")
print(f"📅 分析日期: {analysis_date}")
print("\n⏳ 开始分析（预计 10-15 分钟）...")
print("=" * 80)

# 等待一段时间让 API 限制重置
print("\n⏰ 等待 API 速率限制重置（30 秒）...")
for i in range(30, 0, -5):
    print(f"   剩余 {i} 秒...", end='\r')
    time.sleep(5)
print("\n✅ 开始分析！\n")

try:
    state, decision = ta.propagate(ticker, analysis_date)

    print("\n" + "=" * 80)
    print("✅ 分析完成！")
    print("=" * 80)

    # 生成详细的 Markdown 报告
    report = f"""# 腾讯控股 (0700.HK) 深度分析报告

## 📊 基本信息

| 项目 | 内容 |
|------|------|
| **股票代码** | {ticker} |
| **分析日期** | {analysis_date} |
| **报告生成** | {time.strftime('%Y-%m-%d %H:%M:%S')} |
| **分析深度** | 3 轮辩论 + 2 轮风险讨论 |
| **AI 模型** | Anthropic Claude Sonnet 4.6 |

---

## 🎯 最终投资决策

### 决策结果

```
{decision}
```

---

## 📝 详细分析内容

{decision}

---

## 🔍 分析方法

本报告由 TradingAgents 多智能体系统生成，包含：

1. **基础分析** - 财务健康、盈利能力、成长性
2. **技术分析** - 价格趋势、技术指标、支撑阻力
3. **情绪分析** - 市场情绪、社交媒体、投资者信心
4. **新闻分析** - 重大事件、行业动态、监管政策
5. **风险评估** - 市场风险、流动性风险、特定风险

---

## ⚠️ 免责声明

本报告仅供研究和教育目的，不构成投资建议。
投资有风险，决策需谨慎。

---

*报告生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}*
*Powered by TradingAgents + Anthropic Claude*
"""

    # 保存 Markdown 报告
    with open("tencent_0700HK_detailed_report.md", "w", encoding="utf-8") as f:
        f.write(report)

    print("\n📝 交易决策:")
    print(decision)
    print("\n" + "=" * 80)
    print("💾 详细报告已保存: tencent_0700HK_detailed_report.md")
    print("🎉 分析完成！")
    print("=" * 80)

except KeyboardInterrupt:
    print("\n\n⚠️  分析被用户中断")
    sys.exit(0)

except Exception as e:
    print(f"\n❌ 错误: {e}")

    import traceback
    print("\n详细错误:")
    print(traceback.format_exc())

    print("\n💡 建议:")
    print("  • 如果是速率限制，请等待 10-15 分钟后重试")
    print("  • 或者使用更早的日期（如 2023-12-01）")
    print("  • 检查网络连接")
    sys.exit(1)
