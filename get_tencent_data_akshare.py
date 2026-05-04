#!/usr/bin/env python3
"""
使用 AkShare 获取腾讯股票数据并进行分析
AkShare 是国内免费的金融数据接口，无速率限制
"""
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import sys

print("🚀 使用 AkShare 获取腾讯股票数据")
print("=" * 80)

try:
    # 获取腾讯股票数据（港股）
    print("\n📊 正在获取腾讯控股 (00700) 数据...")

    # 获取实时行情
    print("  • 获取实时行情...")
    stock_hk_spot = ak.stock_hk_spot_em()
    tencent_spot = stock_hk_spot[stock_hk_spot['代码'] == '00700']

    if not tencent_spot.empty:
        print("\n✅ 腾讯控股实时行情:")
        print("-" * 80)
        print(f"  • 股票代码: {tencent_spot['代码'].values[0]}")
        print(f"  • 股票名称: {tencent_spot['名称'].values[0]}")
        print(f"  • 最新价: {tencent_spot['最新价'].values[0]} 港元")
        print(f"  • 涨跌幅: {tencent_spot['涨跌幅'].values[0]}%")
        print(f"  • 涨跌额: {tencent_spot['涨跌额'].values[0]} 港元")
        print(f"  • 成交量: {tencent_spot['成交量'].values[0]}")
        print(f"  • 成交额: {tencent_spot['成交额'].values[0]}")
        print(f"  • 今开: {tencent_spot['今开'].values[0]} 港元")
        print(f"  • 最高: {tencent_spot['最高'].values[0]} 港元")
        print(f"  • 最低: {tencent_spot['最低'].values[0]} 港元")
        print(f"  • 昨收: {tencent_spot['昨收'].values[0]} 港元")
        print("-" * 80)

    # 获取历史数据
    print("\n📈 正在获取历史数据（最近 60 天）...")
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=60)).strftime("%Y%m%d")

    stock_hk_hist = ak.stock_hk_hist(
        symbol="00700",
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust="qfq"  # 前复权
    )

    if not stock_hk_hist.empty:
        print(f"\n✅ 获取到 {len(stock_hk_hist)} 天的历史数据")
        print("\n最近 5 个交易日:")
        print("-" * 80)
        recent_data = stock_hk_hist.tail(5)
        for idx, row in recent_data.iterrows():
            print(f"  {row['日期']}: 收盘 {row['收盘']:.2f}, 涨跌幅 {row['涨跌幅']:.2f}%, 成交量 {row['成交量']}")
        print("-" * 80)

        # 计算技术指标
        print("\n📊 技术指标分析:")
        print("-" * 80)

        # 计算移动平均线
        stock_hk_hist['MA5'] = stock_hk_hist['收盘'].rolling(window=5).mean()
        stock_hk_hist['MA10'] = stock_hk_hist['收盘'].rolling(window=10).mean()
        stock_hk_hist['MA20'] = stock_hk_hist['收盘'].rolling(window=20).mean()

        latest = stock_hk_hist.iloc[-1]
        print(f"  • 5日均线 (MA5): {latest['MA5']:.2f} 港元")
        print(f"  • 10日均线 (MA10): {latest['MA10']:.2f} 港元")
        print(f"  • 20日均线 (MA20): {latest['MA20']:.2f} 港元")

        # 判断趋势
        current_price = latest['收盘']
        if current_price > latest['MA5'] > latest['MA10'] > latest['MA20']:
            trend = "强势上涨 📈"
        elif current_price > latest['MA5'] > latest['MA10']:
            trend = "温和上涨 📊"
        elif current_price < latest['MA5'] < latest['MA10'] < latest['MA20']:
            trend = "弱势下跌 📉"
        elif current_price < latest['MA5'] < latest['MA10']:
            trend = "温和下跌 📊"
        else:
            trend = "震荡整理 ↔️"

        print(f"  • 趋势判断: {trend}")
        print("-" * 80)

        # 计算波动率
        returns = stock_hk_hist['收盘'].pct_change()
        volatility = returns.std() * (252 ** 0.5) * 100  # 年化波动率
        print(f"\n📊 风险指标:")
        print("-" * 80)
        print(f"  • 年化波动率: {volatility:.2f}%")
        print(f"  • 60日最高价: {stock_hk_hist['最高'].max():.2f} 港元")
        print(f"  • 60日最低价: {stock_hk_hist['最低'].min():.2f} 港元")
        print(f"  • 60日涨跌幅: {((latest['收盘'] / stock_hk_hist.iloc[0]['收盘'] - 1) * 100):.2f}%")
        print("-" * 80)

    # 获取公司信息
    print("\n🏢 正在获取公司基本信息...")
    try:
        stock_info = ak.stock_hk_main_board_spot_em()
        tencent_info = stock_info[stock_info['代码'] == '00700']
        if not tencent_info.empty:
            print("\n✅ 公司基本信息:")
            print("-" * 80)
            print(f"  • 公司名称: {tencent_info['名称'].values[0]}")
            print(f"  • 总市值: {tencent_info['总市值'].values[0]}")
            print(f"  • 流通市值: {tencent_info['流通市值'].values[0]}")
            print("-" * 80)
    except Exception as e:
        print(f"  ⚠️  无法获取公司信息: {e}")

    # 生成 Markdown 报告
    print("\n📝 生成分析报告...")

    report = f"""# 腾讯控股 (00700.HK) 数据分析报告

## 📊 基本信息

| 项目 | 内容 |
|------|------|
| **股票代码** | 00700.HK |
| **股票名称** | 腾讯控股 |
| **数据来源** | AkShare (国内数据源) |
| **报告生成** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |

---

## 💰 实时行情

| 指标 | 数值 |
|------|------|
| **最新价** | {tencent_spot['最新价'].values[0]} 港元 |
| **涨跌幅** | {tencent_spot['涨跌幅'].values[0]}% |
| **涨跌额** | {tencent_spot['涨跌额'].values[0]} 港元 |
| **今开** | {tencent_spot['今开'].values[0]} 港元 |
| **最高** | {tencent_spot['最高'].values[0]} 港元 |
| **最低** | {tencent_spot['最低'].values[0]} 港元 |
| **昨收** | {tencent_spot['昨收'].values[0]} 港元 |
| **成交量** | {tencent_spot['成交量'].values[0]} |
| **成交额** | {tencent_spot['成交额'].values[0]} |

---

## 📈 技术分析

### 移动平均线

| 指标 | 数值 |
|------|------|
| **5日均线 (MA5)** | {latest['MA5']:.2f} 港元 |
| **10日均线 (MA10)** | {latest['MA10']:.2f} 港元 |
| **20日均线 (MA20)** | {latest['MA20']:.2f} 港元 |

### 趋势判断

**当前趋势**: {trend}

### 价格区间（60日）

| 指标 | 数值 |
|------|------|
| **最高价** | {stock_hk_hist['最高'].max():.2f} 港元 |
| **最低价** | {stock_hk_hist['最低'].min():.2f} 港元 |
| **60日涨跌幅** | {((latest['收盘'] / stock_hk_hist.iloc[0]['收盘'] - 1) * 100):.2f}% |

---

## ⚠️ 风险指标

| 指标 | 数值 | 说明 |
|------|------|------|
| **年化波动率** | {volatility:.2f}% | 波动率越高，风险越大 |

---

## 📊 最近 5 个交易日表现

| 日期 | 收盘价 | 涨跌幅 | 成交量 |
|------|--------|--------|--------|
"""

    for idx, row in recent_data.iterrows():
        report += f"| {row['日期']} | {row['收盘']:.2f} | {row['涨跌幅']:.2f}% | {row['成交量']} |\n"

    report += """
---

## 💡 数据说明

### 数据来源
- **AkShare**: 免费的中文金融数据接口
- **数据类型**: 港股实时行情 + 历史数据
- **更新频率**: 实时更新（交易时间内）

### 技术指标说明
- **MA5/MA10/MA20**: 5日/10日/20日移动平均线
- **年化波动率**: 基于历史价格波动计算的风险指标
- **前复权**: 已调整历史价格以反映分红、配股等影响

---

## ⚠️ 免责声明

本报告仅供参考，不构成投资建议。投资有风险，入市需谨慎。

---

*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*数据来源: AkShare*
"""

    # 保存报告
    with open("tencent_akshare_report.md", "w", encoding="utf-8") as f:
        f.write(report)

    print("\n" + "=" * 80)
    print("✅ 数据获取成功！")
    print("=" * 80)
    print("\n📁 生成的文件:")
    print("  • tencent_akshare_report.md - 完整数据分析报告")
    print("\n💡 提示:")
    print("  • AkShare 数据来自国内源，无速率限制")
    print("  • 数据实时更新，可随时重新运行")
    print("  • 可以将此数据用于 TradingAgents 分析")
    print("=" * 80)

except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    print("\n详细错误:")
    print(traceback.format_exc())
    sys.exit(1)
