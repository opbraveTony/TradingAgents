# TradingAgents 架构说明文档

> **面向开发者的技术架构指南**  
> 版本: v0.2.4  
> 更新日期: 2026-05-04

---

## 目录

1. [系统概述](#系统概述)
2. [核心架构](#核心架构)
3. [模块详解](#模块详解)
4. [数据流设计](#数据流设计)
5. [扩展开发指南](#扩展开发指南)
6. [AKShare 集成](#akshare-集成)

---

## 系统概述

### 设计理念

TradingAgents 是一个基于多智能体协作的量化交易框架，模拟真实交易公司的组织结构和决策流程。系统采用 **分层决策架构**，通过专业化的 LLM 智能体协作完成从数据分析到交易执行的完整流程。

### 核心特性

- **多智能体协作**: 分析师团队 → 研究员辩论 → 交易员决策 → 风险管理 → 投资组合管理
- **LLM 提供商无关**: 支持 OpenAI、Anthropic、Google、xAI、DeepSeek 等多个 LLM 提供商
- **数据源抽象**: 统一的数据接口，支持 yfinance、Alpha Vantage、AKShare 等多个数据源
- **检查点恢复**: 基于 LangGraph 的状态持久化，支持崩溃恢复
- **结构化输出**: 使用 Pydantic 模型确保输出一致性
- **持久化记忆**: 基于 Markdown 的决策日志系统

### 技术栈

- **核心框架**: LangGraph (状态管理和工作流编排)
- **LLM 集成**: LangChain (多提供商抽象层)
- **数据验证**: Pydantic (结构化输出和配置管理)
- **数据源**: yfinance, Alpha Vantage, AKShare
- **日志系统**: Python logging + 自定义 Markdown 记忆日志

---

## 核心架构

### 1. 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                     TradingAgentsGraph                          │
│                    (主编排器 / Orchestrator)                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Agents    │  │  Dataflows  │  │    Graph    │
│   (智能体)   │  │  (数据流)    │  │  (工作流)    │
└─────────────┘  └─────────────┘  └─────────────┘
         │               │               │
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ LLM Clients │  │ Data Vendors│  │ LangGraph   │
│ (LLM 客户端) │  │ (数据供应商) │  │ (状态机)     │
└─────────────┘  └─────────────┘  └─────────────┘
```

### 2. 决策流程

```
数据收集 → 分析师团队 → 研究员辩论 → 交易员决策 → 风险评估 → 投资组合管理
   ↓           ↓            ↓            ↓           ↓            ↓
[Tools]   [Analysts]  [Researchers]  [Trader]  [Risk Mgmt] [Portfolio Mgr]
```

**详细流程**:

1. **数据收集阶段** (Data Collection)
   - 通过统一的数据接口获取市场数据
   - 支持多数据源切换 (yfinance/Alpha Vantage/AKShare)
   - 数据缓存机制减少 API 调用

2. **分析师团队** (Analyst Team)
   - **基本面分析师** (Fundamentals Analyst): 财务报表、估值指标
   - **技术分析师** (Technical Analyst): 技术指标、图表形态
   - **新闻分析师** (News Analyst): 新闻事件、宏观经济
   - **情绪分析师** (Sentiment Analyst): 社交媒体、市场情绪

3. **研究员辩论** (Researcher Debate)
   - **多头研究员** (Bull Researcher): 看涨观点和论据
   - **空头研究员** (Bear Researcher): 看跌观点和论据
   - 多轮辩论机制 (可配置轮数)
   - **研究经理** (Research Manager): 综合双方观点，形成投资计划

4. **交易员决策** (Trader Decision)
   - 基于研究经理的投资计划
   - 输出具体交易建议 (Buy/Hold/Sell)
   - 包含仓位建议和执行策略

5. **风险管理** (Risk Management)
   - **风险分析师** (Risk Analysts): 多角度风险评估
   - 风险讨论和辩论
   - **风险经理** (Risk Manager): 综合风险评估报告

6. **投资组合管理** (Portfolio Management)
   - 最终决策者
   - 五级评级系统: Buy/Overweight/Hold/Underweight/Sell
   - 批准或拒绝交易提案

---

## 模块详解

### 3.1 Agents 模块 (`tradingagents/agents/`)

智能体模块是系统的核心，包含所有决策智能体的实现。

#### 目录结构

```
agents/
├── __init__.py           # 模块导出
├── schemas.py            # Pydantic 结构化输出模型
├── analysts/             # 分析师团队
│   ├── fundamentals.py   # 基本面分析师
│   ├── technical.py      # 技术分析师
│   ├── news.py           # 新闻分析师
│   └── sentiment.py      # 情绪分析师
├── researchers/          # 研究员团队
│   ├── bull.py           # 多头研究员
│   └── bear.py           # 空头研究员
├── managers/             # 管理层
│   ├── research_mgr.py   # 研究经理
│   └── portfolio_mgr.py  # 投资组合经理
├── trader/               # 交易员
│   └── trader.py         # 交易员智能体
├── risk_mgmt/            # 风险管理
│   ├── risk_analyst.py   # 风险分析师
│   └── risk_manager.py   # 风险经理
└── utils/                # 工具函数
    ├── agent_states.py   # 状态定义
    ├── agent_utils.py    # 工具函数
    └── memory.py         # 记忆系统
```

#### 结构化输出 (schemas.py)

使用 Pydantic 模型确保输出一致性：

```python
class PortfolioRating(str, Enum):
    """五级评级系统"""
    BUY = "Buy"
    OVERWEIGHT = "Overweight"
    HOLD = "Hold"
    UNDERWEIGHT = "Underweight"
    SELL = "Sell"

class ResearchPlan(BaseModel):
    """研究经理的投资计划"""
    recommendation: PortfolioRating
    rationale: str
    strategic_actions: str
    key_risks: str
```

**设计优势**:
- 跨 LLM 提供商的一致性输出
- 利用各提供商的原生结构化输出能力
- 字段描述即输出指令，简化 prompt
- 可渲染回 Markdown 格式，保持系统兼容性

#### 智能体工具 (agent_utils.py)

所有智能体共享的数据获取工具：

```python
# 核心工具函数
get_stock_data()           # 获取股票价格数据
get_indicators()           # 获取技术指标
get_fundamentals()         # 获取基本面数据
get_balance_sheet()        # 获取资产负债表
get_cashflow()             # 获取现金流量表
get_income_statement()     # 获取利润表
get_news()                 # 获取公司新闻
get_insider_transactions() # 获取内部交易
get_global_news()          # 获取全球新闻
```

这些工具通过 `dataflows/interface.py` 路由到具体的数据供应商实现。

### 3.2 Dataflows 模块 (`tradingagents/dataflows/`)

数据流模块负责数据获取和供应商抽象。

#### 架构设计

```
┌─────────────────────────────────────────────────────────┐
│              interface.py (统一接口层)                    │
│  - 工具分类管理                                           │
│  - 供应商路由                                             │
│  - 配置驱动的数据源选择                                    │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  yfinance    │ │ Alpha Vantage│ │   AKShare    │
│  (默认)       │ │  (备选)       │ │  (中国市场)   │
└──────────────┘ └──────────────┘ └──────────────┘
```

#### 工具分类 (TOOLS_CATEGORIES)

```python
TOOLS_CATEGORIES = {
    "core_stock_apis": {
        "description": "OHLCV 股票价格数据",
        "tools": ["get_stock_data"]
    },
    "technical_indicators": {
        "description": "技术分析指标",
        "tools": ["get_indicators"]
    },
    "fundamental_data": {
        "description": "公司基本面",
        "tools": ["get_fundamentals", "get_balance_sheet", ...]
    },
    "news_data": {
        "description": "新闻和内部交易",
        "tools": ["get_news", "get_global_news", ...]
    }
}
```

#### 供应商路由机制

通过配置文件 (`default_config.py`) 控制数据源：

```python
DEFAULT_CONFIG = {
    # 分类级别配置 (默认)
    "data_vendors": {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",
        "news_data": "yfinance",
    },
    # 工具级别配置 (优先级更高)
    "tool_vendors": {
        "get_stock_data": "alpha_vantage",  # 覆盖分类默认值
    },
}
```

**路由逻辑**:
1. 检查 `tool_vendors` 是否有工具级别配置
2. 如果没有，使用 `data_vendors` 的分类级别配置
3. 根据配置从 `VENDOR_METHODS` 映射表获取具体实现

#### 数据供应商实现

**yfinance** (默认，免费):
- `y_finance.py`: 股票数据、基本面、技术指标
- `yfinance_news.py`: 新闻数据
- 优点: 免费、无速率限制、数据全面
- 缺点: 非官方 API，稳定性依赖 Yahoo Finance

**Alpha Vantage** (备选，需 API Key):
- `alpha_vantage_stock.py`: 股票数据
- `alpha_vantage_indicator.py`: 技术指标
- `alpha_vantage_fundamentals.py`: 基本面数据
- `alpha_vantage_news.py`: 新闻数据
- 优点: 官方 API、数据质量高
- 缺点: 免费版有速率限制 (5 calls/min, 100 calls/day)

**AKShare** (中国市场，免费):
- 专门针对中国市场的数据源
- 支持 A 股、港股、美股中概股
- 无速率限制，数据实时更新
- 详见 [AKShare 集成](#akshare-集成) 章节

### 3.3 Graph 模块 (`tradingagents/graph/`)

工作流编排模块，基于 LangGraph 实现状态机和流程控制。

#### 核心组件

```
graph/
├── trading_graph.py      # 主编排器
├── setup.py              # 图构建和初始化
├── propagation.py        # 数据传播逻辑
├── conditional_logic.py  # 条件分支逻辑
├── signal_processing.py  # 信号处理
├── reflection.py         # 反思和优化
└── checkpointer.py       # 检查点管理
```

**TradingAgentsGraph** (trading_graph.py):
- 系统的主入口类
- 初始化所有智能体和 LLM 客户端
- 构建 LangGraph 状态机
- 提供 `propagate()` 方法执行完整的交易决策流程

**GraphSetup** (setup.py):
- 构建 LangGraph 的节点和边
- 定义状态转换逻辑
- 配置条件分支

**Checkpointer** (checkpointer.py):
- 基于 SQLite 的状态持久化
- 支持崩溃后从最后一个成功节点恢复
- 线程 ID 管理

#### 状态定义 (agents/utils/agent_states.py)

```python
class AgentState(TypedDict):
    """主状态对象，在所有节点间传递"""
    ticker: str                    # 股票代码
    analysis_date: str             # 分析日期
    analyst_reports: List[str]     # 分析师报告列表
    research_plan: str             # 研究经理的投资计划
    trader_decision: str           # 交易员决策
    risk_assessment: str           # 风险评估
    final_decision: str            # 最终决策
    # ... 更多状态字段
```

### 3.4 LLM Clients 模块 (`tradingagents/llm_clients/`)

LLM 提供商抽象层，支持多个 LLM 提供商的统一接口。

#### 架构设计

```
llm_clients/
├── factory.py            # 工厂模式创建客户端
├── base_client.py        # 抽象基类
├── openai_client.py      # OpenAI/xAI 客户端
├── anthropic_client.py   # Anthropic Claude 客户端
├── google_client.py      # Google Gemini 客户端
├── azure_client.py       # Azure OpenAI 客户端
├── model_catalog.py      # 模型目录和映射
└── validators.py         # 配置验证
```

#### 工厂模式 (factory.py)

```python
def create_llm_client(
    provider: str,
    model: str,
    base_url: Optional[str] = None,
    **kwargs
) -> BaseLLMClient:
    """根据提供商创建对应的客户端"""
    if provider == "openai":
        return OpenAIClient(model, base_url, **kwargs)
    elif provider == "anthropic":
        return AnthropicClient(model, base_url, **kwargs)
    elif provider == "google":
        return GoogleClient(model, base_url, **kwargs)
    # ...
```

#### 提供商特性支持

| 提供商 | 结构化输出 | 思考模式 | 流式输出 |
|--------|-----------|---------|---------|
| OpenAI | json_schema | reasoning_effort | ✓ |
| Anthropic | tool_use | extended_thinking | ✓ |
| Google | response_schema | thinking_level | ✓ |
| xAI | json_schema | - | ✓ |
| DeepSeek | json_schema | thinking_mode | ✓ |

---

## 数据流设计

### 4.1 完整数据流图

```
用户输入 (ticker, date)
        ↓
┌───────────────────────────────────────────────────────────┐
│ 1. 数据收集阶段 (Data Collection)                          │
│    - get_stock_data()      → 价格数据                      │
│    - get_indicators()      → 技术指标                      │
│    - get_fundamentals()    → 基本面数据                    │
│    - get_news()            → 新闻数据                      │
└────────────────────┬──────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────────────┐
│ 2. 分析师团队 (Analyst Team)                               │
│    并行执行 4 个分析师智能体                                │
│    ├─ Fundamentals Analyst → 基本面报告                   │
│    ├─ Technical Analyst    → 技术分析报告                 │
│    ├─ News Analyst         → 新闻分析报告                 │
│    └─ Sentiment Analyst    → 情绪分析报告                 │
└────────────────────┬──────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────────────┐
│ 3. 研究员辩论 (Researcher Debate)                          │
│    多轮辩论循环 (max_debate_rounds)                        │
│    ├─ Bull Researcher  → 看涨论据                         │
│    ├─ Bear Researcher  → 看跌论据                         │
│    └─ Research Manager → 综合投资计划 (ResearchPlan)      │
└────────────────────┬──────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────────────┐
│ 4. 交易员决策 (Trader Decision)                            │
│    基于投资计划生成交易提案                                 │
│    输出: TraderDecision (Buy/Hold/Sell + 仓位建议)         │
└────────────────────┬──────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────────────┐
│ 5. 风险管理 (Risk Management)                              │
│    多轮风险讨论 (max_risk_discuss_rounds)                  │
│    ├─ Risk Analysts → 多角度风险分析                       │
│    └─ Risk Manager  → 综合风险评估                        │
└────────────────────┬──────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────────────┐
│ 6. 投资组合管理 (Portfolio Management)                     │
│    最终决策者                                              │
│    输出: PortfolioDecision (5级评级 + 执行计划)            │
└────────────────────┬──────────────────────────────────────┘
                     ↓
        最终决策 + 完整报告
```

### 4.2 状态传递机制

LangGraph 使用 `AgentState` 在节点间传递状态：

```python
# 初始状态
state = {
    "ticker": "AAPL",
    "analysis_date": "2024-04-15",
    "analyst_reports": [],
    # ...
}

# 每个节点接收状态，处理后返回更新
def analyst_node(state: AgentState) -> AgentState:
    report = generate_analyst_report(state)
    state["analyst_reports"].append(report)
    return state

# LangGraph 自动合并状态更新
```

### 4.3 记忆系统 (Memory System)

**TradingMemoryLog** (agents/utils/memory.py):
- 基于 Markdown 的持久化决策日志
- 记录每次交易决策的完整上下文
- 支持检索历史决策作为参考

```markdown
## Decision Log Entry

**Ticker**: AAPL  
**Date**: 2024-04-15  
**Decision**: Buy (Overweight)  
**Rationale**: Strong fundamentals, positive technical signals...

### Key Factors
- Revenue growth: +15% YoY
- RSI: 45 (not overbought)
- Positive news sentiment

### Risks
- Market volatility
- Regulatory concerns

---
```

---

## 扩展开发指南

### 5.1 添加新的分析师

**步骤**:

1. 在 `tradingagents/agents/analysts/` 创建新文件
2. 定义分析师类和 prompt
3. 实现数据获取和分析逻辑
4. 在 `trading_graph.py` 中注册新分析师

**示例**: 添加宏观经济分析师

```python
# tradingagents/agents/analysts/macro.py

from langchain_core.messages import SystemMessage

MACRO_ANALYST_PROMPT = """
You are a Macro Economic Analyst...
"""

def create_macro_analyst(llm, tools):
    """创建宏观经济分析师"""
    return llm.bind_tools(tools).with_config({
        "system": MACRO_ANALYST_PROMPT
    })
```

### 5.2 添加新的数据源

**步骤**:

1. 在 `tradingagents/dataflows/` 创建新的供应商模块
2. 实现所需的数据获取函数
3. 在 `interface.py` 的 `VENDOR_METHODS` 中注册
4. 在 `default_config.py` 中添加配置选项

**示例**: 集成 AKShare

```python
# tradingagents/dataflows/akshare_stock.py

import akshare as ak

def get_akshare_stock(ticker: str, start_date: str, end_date: str):
    """使用 AKShare 获取股票数据"""
    # 转换股票代码格式
    symbol = convert_ticker_to_akshare_format(ticker)
    
    # 获取数据
    df = ak.stock_zh_a_hist(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        adjust="qfq"
    )
    
    return format_data(df)
```

```python
# tradingagents/dataflows/interface.py

from .akshare_stock import get_akshare_stock

VENDOR_METHODS = {
    "get_stock_data": {
        "yfinance": get_YFin_data_online,
        "alpha_vantage": get_alpha_vantage_stock,
        "akshare": get_akshare_stock,  # 新增
    },
    # ...
}
```

### 5.3 自定义 LLM 提供商

**步骤**:

1. 在 `tradingagents/llm_clients/` 创建新客户端
2. 继承 `BaseLLMClient` 抽象类
3. 实现 `get_llm()` 方法
4. 在 `factory.py` 中注册

**示例**: 添加自定义提供商

```python
# tradingagents/llm_clients/custom_client.py

from .base_client import BaseLLMClient
from langchain_community.chat_models import ChatCustom

class CustomClient(BaseLLMClient):
    def get_llm(self):
        return ChatCustom(
            model=self.model,
            api_key=os.getenv("CUSTOM_API_KEY"),
            base_url=self.base_url,
            **self.kwargs
        )
```

### 5.4 配置最佳实践

**环境变量**:
```bash
# LLM API Keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."

# 数据源 API Keys
export ALPHA_VANTAGE_API_KEY="..."

# 自定义配置
export TRADINGAGENTS_RESULTS_DIR="./results"
export TRADINGAGENTS_CACHE_DIR="./cache"
```

**配置文件**:
```python
# 自定义配置
custom_config = DEFAULT_CONFIG.copy()
custom_config.update({
    "llm_provider": "anthropic",
    "deep_think_llm": "claude-sonnet-4-6",
    "quick_think_llm": "claude-haiku-4-5",
    "max_debate_rounds": 3,
    "output_language": "Chinese",
    "data_vendors": {
        "core_stock_apis": "akshare",  # 使用 AKShare
    }
})

ta = TradingAgentsGraph(config=custom_config)
```

---

## AKShare 集成

### 6.1 AKShare 简介

**AKShare** 是专门针对中国金融市场的开源数据接口：
- **免费**: 完全免费，无需 API Key
- **无速率限制**: 可以频繁调用
- **数据全面**: 支持 A 股、港股、美股中概股、期货、基金等
- **实时更新**: 交易时间内实时更新数据
- **中文友好**: 数据字段使用中文，易于理解

### 6.2 集成架构

```
用户脚本 (analyze_tencent.py)
        ↓
TradingAgentsGraph
        ↓
dataflows/interface.py (路由层)
        ↓
dataflows/akshare_*.py (AKShare 实现)
        ↓
AKShare API
```

### 6.3 已实现的脚本

**数据获取脚本**:

1. **get_tencent_data_akshare.py**
   - 获取腾讯控股 (00700.HK) 实时行情
   - 获取历史数据 (60 天)
   - 计算技术指标 (MA5/MA10/MA20)
   - 生成 Markdown 分析报告

2. **get_tencent_deep_data.py**
   - 深度数据获取
   - 包含更多技术指标 (RSI, MACD, 布林带)
   - 财务数据和公司信息
   - 综合分析报告

**分析脚本**:

1. **analyze_tencent.py**
   - 基础分析流程
   - 使用 TradingAgents 完整流程
   - 输出中文分析报告

2. **analyze_tencent_detailed.py**
   - 详细分析流程
   - 启用检查点恢复
   - 更多轮次的辩论和风险讨论

3. **analyze_tencent_hk.py**
   - 使用香港股票代码 (0700.HK)
   - 3 轮深度辩论
   - 针对港股市场优化

4. **analyze_tencent_wait.py**
   - 带等待机制的分析
   - 避免 API 速率限制
   - 适合批量分析

### 6.4 使用示例

**快速开始**:

```bash
# 1. 安装 AKShare
pip install akshare

# 2. 获取腾讯股票数据
python get_tencent_data_akshare.py

# 3. 运行完整分析
python analyze_tencent.py
```

**自定义配置**:

```python
import akshare as ak
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 配置使用 AKShare
config = DEFAULT_CONFIG.copy()
config["data_vendors"]["core_stock_apis"] = "akshare"
config["output_language"] = "Chinese"

# 初始化
ta = TradingAgentsGraph(config=config)

# 分析腾讯
ticker = "00700.HK"  # 港股代码
date = "2024-04-15"
_, decision = ta.propagate(ticker, date)
```

### 6.5 AKShare vs yfinance vs Alpha Vantage

| 特性 | AKShare | yfinance | Alpha Vantage |
|------|---------|----------|---------------|
| **费用** | 免费 | 免费 | 免费版有限 |
| **速率限制** | 无 | 无 | 5 calls/min |
| **中国市场** | ✓✓✓ | ✓ | ✓ |
| **美国市场** | ✓ | ✓✓✓ | ✓✓✓ |
| **实时数据** | ✓ | ✓ | ✓ |
| **技术指标** | ✓✓ | ✓ | ✓✓✓ |
| **财务数据** | ✓✓ | ✓✓ | ✓✓✓ |
| **新闻数据** | ✓ | ✓ | ✓✓ |
| **API 稳定性** | ✓✓ | ✓ | ✓✓✓ |

**推荐使用场景**:
- **中国市场 (A 股、港股)**: 优先使用 AKShare
- **美国市场**: 优先使用 yfinance 或 Alpha Vantage
- **需要官方 API**: 使用 Alpha Vantage
- **高频调用**: 使用 AKShare 或 yfinance

### 6.6 数据格式转换

AKShare 使用中文字段名，需要转换为英文：

```python
def convert_akshare_to_standard(df):
    """转换 AKShare 数据格式"""
    column_mapping = {
        "日期": "Date",
        "开盘": "Open",
        "收盘": "Close",
        "最高": "High",
        "最低": "Low",
        "成交量": "Volume",
        "涨跌幅": "Change%",
    }
    return df.rename(columns=column_mapping)
```

---

## 附录

### A. 目录结构总览

```
TradingAgents/
├── tradingagents/              # 核心包
│   ├── agents/                 # 智能体模块
│   │   ├── analysts/           # 分析师
│   │   ├── researchers/        # 研究员
│   │   ├── managers/           # 管理层
│   │   ├── trader/             # 交易员
│   │   ├── risk_mgmt/          # 风险管理
│   │   └── utils/              # 工具函数
│   ├── dataflows/              # 数据流模块
│   │   ├── y_finance.py        # yfinance 实现
│   │   ├── alpha_vantage*.py   # Alpha Vantage 实现
│   │   └── interface.py        # 统一接口
│   ├── graph/                  # 工作流编排
│   │   ├── trading_graph.py    # 主编排器
│   │   ├── setup.py            # 图构建
│   │   └── checkpointer.py     # 检查点
│   ├── llm_clients/            # LLM 客户端
│   │   ├── factory.py          # 工厂模式
│   │   ├── openai_client.py    # OpenAI
│   │   ├── anthropic_client.py # Anthropic
│   │   └── google_client.py    # Google
│   └── default_config.py       # 默认配置
├── analyze_tencent*.py         # 分析脚本 (AKShare)
├── get_tencent_*.py            # 数据获取脚本
├── main.py                     # CLI 入口
├── test.py                     # 测试脚本
└── README.md                   # 项目文档
```

### B. 关键配置参数

```python
DEFAULT_CONFIG = {
    # 目录配置
    "results_dir": "~/.tradingagents/logs",
    "data_cache_dir": "~/.tradingagents/cache",
    "memory_log_path": "~/.tradingagents/memory/trading_memory.md",
    
    # LLM 配置
    "llm_provider": "openai",           # openai/anthropic/google/xai/deepseek
    "deep_think_llm": "gpt-5.4",        # 复杂推理模型
    "quick_think_llm": "gpt-5.4-mini",  # 快速任务模型
    
    # 提供商特定配置
    "google_thinking_level": None,      # high/minimal
    "openai_reasoning_effort": None,    # high/medium/low
    "anthropic_effort": None,           # high/medium/low
    
    # 工作流配置
    "checkpoint_enabled": False,        # 检查点恢复
    "output_language": "English",       # 输出语言
    "max_debate_rounds": 1,             # 辩论轮数
    "max_risk_discuss_rounds": 1,       # 风险讨论轮数
    
    # 数据源配置
    "data_vendors": {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",
        "news_data": "yfinance",
    },
    "tool_vendors": {},  # 工具级别覆盖
}
```

### C. 常见问题

**Q: 如何切换 LLM 提供商？**
```python
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "anthropic"
config["deep_think_llm"] = "claude-sonnet-4-6"
config["quick_think_llm"] = "claude-haiku-4-5"
```

**Q: 如何使用 AKShare 获取中国股票数据？**
```python
config["data_vendors"]["core_stock_apis"] = "akshare"
# 或者针对特定工具
config["tool_vendors"]["get_stock_data"] = "akshare"
```

**Q: 如何启用检查点恢复？**
```python
config["checkpoint_enabled"] = True
# 崩溃后重新运行相同的 ticker 和 date 会自动恢复
```

**Q: 如何增加辩论轮数？**
```python
config["max_debate_rounds"] = 3  # 更深入的分析
config["max_risk_discuss_rounds"] = 2  # 更全面的风险评估
```

**Q: 如何输出中文报告？**
```python
config["output_language"] = "Chinese"
# 注意：内部辩论仍使用英文以保证推理质量
```

### D. 性能优化建议

1. **使用缓存**: 启用数据缓存减少 API 调用
2. **选择合适的模型**: 
   - 复杂推理: GPT-5.4, Claude Sonnet 4.6, Gemini 3.1 Pro
   - 快速任务: GPT-5.4-mini, Claude Haiku 4.5, Gemini 3.1 Flash
3. **并行执行**: 分析师团队默认并行执行
4. **检查点**: 长时间运行启用检查点避免重复计算
5. **数据源选择**: 
   - 中国市场优先 AKShare (无速率限制)
   - 美国市场优先 yfinance (免费且稳定)

### E. 开发路线图

**已完成** (v0.2.4):
- ✓ 多 LLM 提供商支持
- ✓ 结构化输出
- ✓ 检查点恢复
- ✓ 持久化记忆日志
- ✓ 多数据源支持

**计划中**:
- [ ] AKShare 完整集成到 dataflows
- [ ] 实时交易执行接口
- [ ] 回测框架增强
- [ ] Web UI 界面
- [ ] 更多技术指标
- [ ] 机器学习模型集成

---

## 总结

TradingAgents 是一个模块化、可扩展的多智能体交易框架。通过清晰的架构分层和抽象接口，开发者可以轻松：

1. **添加新的智能体**: 扩展分析能力
2. **集成新的数据源**: 支持更多市场
3. **切换 LLM 提供商**: 优化成本和性能
4. **自定义决策流程**: 适应不同交易策略

本文档提供了从系统概述到具体实现的完整指南，帮助开发者快速理解和扩展 TradingAgents 框架。

---

**文档版本**: v1.0  
**最后更新**: 2026-05-04  
**维护者**: TradingAgents 开发团队  
**许可证**: MIT
