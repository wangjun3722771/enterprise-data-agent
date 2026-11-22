
# Enterprise Data Agent

基于 Python 开发的企业经营数据分析 Agent 项目。

## 项目目标

- 自然语言查询企业业务数据库
- 使用 Agent 调用数据库工具
- SQL 安全检查与错误纠正
- Agent 自动化评测

## 技术栈

- Python
- FastAPI（后续添加）
- DB-GPT（后续集成）
- SQLAlchemy（后续添加）
- Pytest

## 环境配置

推荐 Python 3.11。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## 运行测试

```powershell
python -m pytest -v
```
