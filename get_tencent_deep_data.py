#!/usr/bin/env python3
"""
腾讯股票深度数据获取 - 使用 AkShare
包含：实时行情、财务数据、新闻资讯、技术指标等
"""
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import sys

print("🚀 腾讯控股深度数据分析")
print("=" * 80)

# 存储所有数据
all_data = {}

try:
    # 1. 实时行情
    print("\n📊 1/6 获取实时行情...")
    stock_hk_spot = ak.stock_hk_spot_em()
    tencent_spot = stock_hk_spot[stock_hk_spot['代码'] == '00700']

    if not tencent_spot.empty:
        all_data['spot'] = tencent_spot.iloc[0].to_dict()
        print(f"✅ 最新价: {all_data['spot']['最新价']} 港元 ({all_data['spot']['涨跌幅']}%)")

    # 2. 历史数据和技术指标
    print("\n📈 2/6 获取历史数据（90天）...")
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")

    stock_hk_hist = ak.stock_hk_hist(
        symbol="00700",
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust="qfq"
    )

    if not stock_hk_hist.empty:
        # 计算技术指标
        stock_hk_hist['MA5'] = stock_hk_hist['收盘'].rolling(window=5).mean()
        stock_hk_hist['MA10'] = stock_hk_hist['收盘'].rolling(window=10).mean()
        stock_hk_hist['MA20'] = stock_hk_hist['收盘'].rolling(window=20).mean()
        stock_hk_hist['MA60'] = stock_hk_hist['收盘'].rolling(window=60).mean()

        # 计算 RSI
        delta = stock_hk_hist['收盘'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        stock_hk_hist['RSI'] = 100 - (100 / (1 + rs))

        # 计算 MACD
        exp1 = stock_hk_hist['收盘'].ewm(span=12, adjust=False).mean()
        exp2 = stock_hk_hist['收盘'].ewm(span=26, adjust=False).mean()
        stock_hk_hist['MACD'] = exp1 - exp2
        stock_hk_hist['Signal'] = stock_hk_hist['MACD'].ewm(span=9, adjust=False).mean()

        all_data['history'] = stock_hk_hist
        print(f"✅ 获取 {len(stock_hk_hist)} 天历史数据")

    # 3. 财务数据
    print("\n💰 3/6 获取财务数据...")
    try:
        # 获取港股财务指标
        stock_financial = ak.stock_financial_hk_analysis_indicator_em(symbol="00700")
        if not stock_financial.empty:
            all_data['financial'] = stock_financial
            print(f"✅ 获取 {len(stock_financial)} 期财务数据")

            # 显示最新财务指标
            latest_financial = stock_financial.iloc[-1]
            print(f"   最新财报期: {latest_financial['报告期']}")
    except Exception as e:
        print(f"   ⚠️  财务数据获取失败: {e}")

    # 4. 公司基本信息
    print("\n🏢 4/6 获取公司基本信息...")
    try:
        stock_info = ak.stock_hk_main_board_spot_em()
        tencent_info = stock_info[stock_info['代码'] == '00700']
        if not tencent_info.empty:
            all_data['company_info'] = tencent_info.iloc[0].to_dict()
            print(f"✅ 公司名称: {all_data['company_info']['名称']}")
    except Exception as e:
        print(f"   ⚠️  公司信息获取失败: {e}")

    # 5. 新闻资讯
    print("\n📰 5/6 获取新闻资讯...")
    try:
        # 获取港股新闻
        news = ak.stock_news_em(symbol="00700")
        if not news.empty:
            all_data['news'] = news.head(10)  # 最新10条新闻
            print(f"✅ 获取 {len(all_data['news'])} 条最新新闻")
            print("\n   最新新闻标题:")
            for idx, row in all_data['news'].head(3).iterrows():
                print(f"   • {row['新闻标题']}")
    except Exception as e:
        print(f"   ⚠️  新闻数据获取失败: {e}")

    # 6. 资金流向
    print("\n💸 6/6 获取资金流向...")
    try:
        money_flow = ak.stock_individual_fund_flow_rank(symbol="即时")
        tencent_flow = money_flow[money_flow['代码'] == '00700']
        if not tencent_flow.empty:
            all_data['money_flow'] = tencent_flow.iloc[0].to_dict()
            print(f"✅ 主力净流入: {all_data['money_flow'].get('主力净流入-净额', 'N/A')}")
    except Exception as e:
        print(f"   ⚠️  资金流向获取失败: {e}")

    # 生成详细的 Markdown 报告
    print("\n" + "=" * 80)
    print("📝 生成详细分析报告...")
    print("=" * 80)

    latest = stock_hk_hist.iloc[-1]

    report = f"""# 腾讯控股 (00700.HK) 深度分析报告

## 📊 报告信息

| 项目 | 内容 |
|------|------|
| **生成时间** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| **数据来源** | AkShare (国内数据源) |
| **分析周期** | 90 天 |
| **报告类型** | 深度分析 |

---

## 💰 实时行情

### 当前价格

| 指标 | 数值 | 变化 |
|------|------|------|
| **最新价** | {all_data['spot']['最新价']} 港元 | {all_data['spot']['涨跌幅']}% ({all_data['spot']['涨跌额']} 港元) |
| **今开** | {all_data['spot']['今开']} 港元 | - |
| **最高** | {all_data['spot']['最高']} 港元 | - |
| **最低** | {all_data['spot']['最低']} 港元 | - |
| **昨收** | {all_data['spot']['昨收']} 港元 | - |

### 成交情况

| 指标 | 数值 |
|------|------|
| **成交量** | {all_data['spot']['成交量']:,.0f} 股 |
| **成交额** | {all_data['spot']['成交额']:,.0f} 港元 |
| **换手率** | {all_data['spot'].get('换手率', 'N/A')} |

---

## 📈 技术分析

### 移动平均线系统

| 周期 | 数值 | 与当前价格关系 |
|------|------|---------------|
| **MA5** | {latest['MA5']:.2f} 港元 | {'上方 ↑' if latest['收盘'] > latest['MA5'] else '下方 ↓'} |
| **MA10** | {latest['MA10']:.2f} 港元 | {'上方 ↑' if latest['收盘'] > latest['MA10'] else '下方 ↓'} |
| **MA20** | {latest['MA20']:.2f} 港元 | {'上方 ↑' if latest['收盘'] > latest['MA20'] else '下方 ↓'} |
| **MA60** | {latest['MA60']:.2f} 港元 | {'上方 ↑' if latest['收盘'] > latest['MA60'] else '下方 ↓'} |

### 技术指标

| 指标 | 数值 | 信号 |
|------|------|------|
| **RSI(14)** | {latest['RSI']:.2f} | {'超买 ⚠️' if latest['RSI'] > 70 else '超卖 ⚠️' if latest['RSI'] < 30 else '中性 ✓'} |
| **MACD** | {latest['MACD']:.4f} | {'多头 ↑' if latest['MACD'] > latest['Signal'] else '空头 ↓'} |
| **Signal** | {latest['Signal']:.4f} | - |

### 趋势判断

"""

    # 趋势分析
    current_price = latest['收盘']
    if current_price > latest['MA5'] > latest['MA10'] > latest['MA20']:
        trend = "**强势上涨趋势** 📈"
        trend_desc = "股价位于所有均线之上，多头排列，趋势强劲"
    elif current_price > latest['MA5'] > latest['MA10']:
        trend = "**温和上涨趋势** 📊"
        trend_desc = "股价位于短期均线之上，上涨动能温和"
    elif current_price < latest['MA5'] < latest['MA10'] < latest['MA20']:
        trend = "**弱势下跌趋势** 📉"
        trend_desc = "股价位于所有均线之下，空头排列，趋势疲弱"
    elif current_price < latest['MA5'] < latest['MA10']:
        trend = "**温和下跌趋势** 📊"
        trend_desc = "股价位于短期均线之下，下跌压力温和"
    else:
        trend = "**震荡整理** ↔️"
        trend_desc = "股价在均线附近波动，方向不明确"

    report += f"""
{trend}

{trend_desc}

### 价格区间（90日）

| 指标 | 数值 |
|------|------|
| **最高价** | {stock_hk_hist['最高'].max():.2f} 港元 |
| **最低价** | {stock_hk_hist['最低'].min():.2f} 港元 |
| **价格振幅** | {((stock_hk_hist['最高'].max() / stock_hk_hist['最低'].min() - 1) * 100):.2f}% |
| **90日涨跌幅** | {((latest['收盘'] / stock_hk_hist.iloc[0]['收盘'] - 1) * 100):.2f}% |

---

## ⚠️ 风险评估

### 波动性分析

"""

    returns = stock_hk_hist['收盘'].pct_change()
    volatility = returns.std() * (252 ** 0.5) * 100

    report += f"""
| 指标 | 数值 | 评级 |
|------|------|------|
| **年化波动率** | {volatility:.2f}% | {'高风险 🔴' if volatility > 40 else '中风险 🟡' if volatility > 25 else '低风险 🟢'} |
| **最大回撤** | {(returns.min() * 100):.2f}% | - |
| **平均日涨跌幅** | {(returns.mean() * 100):.2f}% | - |

### 风险提示

"""

    if volatility > 40:
        report += "- 🔴 **高波动风险**: 年化波动率超过 40%，价格波动剧烈\n"
    if latest['RSI'] > 70:
        report += "- ⚠️ **超买风险**: RSI 指标显示超买，可能面临回调压力\n"
    elif latest['RSI'] < 30:
        report += "- ⚠️ **超卖机会**: RSI 指标显示超卖，可能存在反弹机会\n"
    if current_price < latest['MA20']:
        report += "- 📉 **趋势风险**: 股价低于 20 日均线，短期趋势偏弱\n"

    report += """
---

## 📊 最近交易日表现

| 日期 | 收盘价 | 涨跌幅 | 成交量 | RSI | MACD |
|------|--------|--------|--------|-----|------|
"""

    for idx, row in stock_hk_hist.tail(10).iterrows():
        report += f"| {row['日期']} | {row['收盘']:.2f} | {row['涨跌幅']:.2f}% | {row['成交量']:,.0f} | {row['RSI']:.1f} | {row['MACD']:.4f} |\n"

    # 添加新闻部分
    if 'news' in all_data:
        report += """
---

## 📰 最新新闻资讯

"""
        for idx, row in all_data['news'].head(5).iterrows():
            report += f"### {row['新闻标题']}\n\n"
            report += f"- **发布时间**: {row['发布时间']}\n"
            report += f"- **来源**: {row.get('新闻来源', 'N/A')}\n\n"

    # 添加财务数据
    if 'financial' in all_data and not all_data['financial'].empty:
        latest_fin = all_data['financial'].iloc[-1]
        report_period = latest_fin.get('报告期', latest_fin.iloc[0] if hasattr(latest_fin, 'iloc') else '最新')
        report += f"""
---

## 💼 财务数据

### 最新财报 ({report_period})

"""
        # 显示关键财务指标
        for col in all_data['financial'].columns:
            if col != '报告期':
                try:
                    report += f"- **{col}**: {latest_fin[col]}\n"
                except:
                    pass

    report += """
---

## 💡 投资建议

### 基于技术分析的建议

"""

    # 生成投资建议
    if trend == "**强势上涨趋势** 📈" and latest['RSI'] < 70:
        report += """
✅ **建议**: 持有或适度加仓
- 趋势强劲，多头排列
- RSI 未超买，仍有上涨空间
- 建议设置止损位于 MA20 下方
"""
    elif trend == "**弱势下跌趋势** 📉" and latest['RSI'] > 30:
        report += """
⚠️ **建议**: 观望或减仓
- 趋势疲弱，空头排列
- RSI 未超卖，可能继续下跌
- 等待趋势反转信号
"""
    elif latest['RSI'] < 30:
        report += """
💡 **建议**: 关注反弹机会
- RSI 显示超卖
- 可能出现技术性反弹
- 建议小仓位试探，严格止损
"""
    elif latest['RSI'] > 70:
        report += """
⚠️ **建议**: 谨慎追高
- RSI 显示超买
- 短期可能面临回调
- 建议等待回调后再介入
"""
    else:
        report += """
📊 **建议**: 震荡整理，观望为主
- 趋势不明确
- 等待明确信号
- 可设置区间操作策略
"""

    report += """
---

## 📚 数据说明

### 技术指标解释

- **MA (移动平均线)**: 反映价格趋势的指标
  - MA5: 5日均线，反映短期趋势
  - MA10: 10日均线，反映中短期趋势
  - MA20: 20日均线，反映中期趋势
  - MA60: 60日均线，反映长期趋势

- **RSI (相对强弱指标)**: 衡量超买超卖的指标
  - RSI > 70: 超买，可能回调
  - RSI < 30: 超卖，可能反弹
  - 30-70: 正常区间

- **MACD (指数平滑异同移动平均线)**: 趋势跟踪指标
  - MACD > Signal: 多头信号
  - MACD < Signal: 空头信号

### 数据来源

- **AkShare**: 免费的中文金融数据接口
- **更新频率**: 实时更新（交易时间内）
- **数据类型**: 港股行情、财务数据、新闻资讯

---

## ⚠️ 免责声明

**重要提示**:

1. 本报告仅供参考，不构成投资建议
2. 投资有风险，入市需谨慎
3. 技术分析存在局限性，需结合基本面分析
4. 过往表现不代表未来收益
5. 请根据自身风险承受能力做出投资决策

---

*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*数据来源: AkShare*
*分析工具: Python + Pandas*

---

<div align="center">

**📈 投资有风险，决策需谨慎 📉**

</div>
"""

    # 保存报告
    with open("tencent_deep_analysis.md", "w", encoding="utf-8") as f:
        f.write(report)

    print("\n" + "=" * 80)
    print("✅ 深度分析完成！")
    print("=" * 80)
    print("\n📁 生成的文件:")
    print("  • tencent_deep_analysis.md - 完整深度分析报告")
    print("\n📊 数据统计:")
    print(f"  • 历史数据: {len(stock_hk_hist)} 天")
    if 'news' in all_data:
        print(f"  • 新闻资讯: {len(all_data['news'])} 条")
    if 'financial' in all_data:
        print(f"  • 财务数据: {len(all_data['financial'])} 期")
    print("\n💡 提示:")
    print("  • 报告包含实时行情、技术分析、新闻资讯、财务数据")
    print("  • 可以将此数据用于 TradingAgents 深度分析")
    print("  • 数据来自国内源，无速率限制，可随时更新")
    print("=" * 80)

except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    print("\n详细错误:")
    print(traceback.format_exc())
    sys.exit(1)
