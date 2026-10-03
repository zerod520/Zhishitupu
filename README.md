# Zhishitupu · 燃气安全知识图谱系统

可运行的 V0.1 企业知识图谱、数据治理和模型治理主项目骨架。保留本地 PyCharm + Neo4j 使用方式，预测算法由独立 prediction 项目负责。

## 技术栈与目录

- 后端：Python 3.11+、FastAPI、Uvicorn；入口 `backend/app/main.py:app`。
- 前端：HTML/CSS/JavaScript；入口 `frontend/index.html`，后端同源托管，无需 npm。
- 数据源：默认只读合成演示数据，可配置 Neo4j 5+ / Cypher `elementId`。

```text
Zhishitupu/
├── backend/app/
│   ├── main.py                 # 应用、路由与前端托管
│   ├── config.py               # 环境变量校验
│   ├── schemas.py              # API 数据结构
│   ├── graph_repository.py     # 演示 / Neo4j 适配器
│   └── modules/               # 知识图谱、数据治理、模型治理
├── frontend/                   # index.html、app.js、styles.css
├── tests/                      # API 和配置冒烟检查
├── docs/architecture.md        # 模块与 prediction 职责边界
├── .env.example                # 配置清单
├── requirements.txt            # 运行依赖
├── requirements-dev.txt        # 测试依赖
└── run.py                      # 统一启动入口
```

## Windows / PyCharm 启动

在仓库根目录执行（Python 3.11 或更新版本）：

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe run.py
```

PyCharm：打开仓库根目录，解释器选择 `.venv/Scripts/python.exe`，运行文件选择 `run.py`，工作目录选择仓库根目录。直接运行后端文件会破坏包导入，请使用统一入口。

## macOS / Linux 启动

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
.venv/bin/python run.py
```

访问 `http://127.0.0.1:8000`；API 文档 `http://127.0.0.1:8000/docs`；存活检查 `http://127.0.0.1:8000/api/v1/health`。停止：终端 Ctrl+C。端口被占用时，在 `.env` 中修改 `PORT=8001`，再访问对应端口。

默认无需启动 Neo4j。知识图谱显示 3 个合成节点与 2 条关系；数据治理、模型治理仅显示待实现能力，不提供导入、审批或训练功能。

## 连接本地 Neo4j

启动 Neo4j 后修改根目录 `.env` 并重启应用：

```dotenv
GRAPH_BACKEND=neo4j
NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=填入本地密码
NEO4J_DATABASE=neo4j
```

图谱查询仅执行读事务。当前骨架没有任何写库功能。连接失败返回 503，并在页面显示错误，不会回退演示数据。健康接口仅说明应用正在运行，不表示数据库连接成功；实际连接通过图谱查询验证。真实数据库为空时返回空图谱。

## 环境变量

| 变量 | 默认值 | 用途 |
|---|---|---|
| APP_NAME | 燃气安全知识图谱系统 | API 标题（前端标题是静态文案） |
| HOST | 127.0.0.1 | 本地监听地址 |
| PORT | 8000 | 监听端口，1–65535 |
| RELOAD | false | 本地开发热重载 |
| GRAPH_BACKEND | demo | demo / neo4j；其他值启动报错 |
| NEO4J_URI | bolt://127.0.0.1:7687 | 数据库地址 |
| NEO4J_USER | neo4j | 数据库账号 |
| NEO4J_PASSWORD | 空 | neo4j 模式必填 |
| NEO4J_DATABASE | neo4j | 数据库名 |
| PREDICTION_BASE_URL | 空 | 预留；V0.1 不调用预测服务 |

系统环境变量优先于 `.env`。`.env` 已被 Git 忽略，请勿提交数据库密码。无需 DeepSeek API Key。

## 验证

```bash
# Windows 将 .venv/bin/python 替换为 .\.venv\Scripts\python.exe
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
```

测试覆盖：前端入口、静态文件、健康接口、三模块接口、演示关系完整性、参数校验、Neo4j 故障不回退与配置校验。真实 Neo4j 连接需在自己的环境验证。

职责和未来接口契约见 [docs/architecture.md](docs/architecture.md)。V0.1 为本地只读骨架；现有 Patch 项目尚未迁入，账号权限、图谱编辑、数据导入、模型训练与正式部署将在后续实现。
