# 模块与接口边界

前端：原生 HTML/CSS/JavaScript，入口 `frontend/index.html`，由 FastAPI 同源托管。后端：Python 3.11+ / FastAPI / Uvicorn，入口 `backend/app/main.py:app`。统一启动 `python run.py`，无 Node 构建步骤。

| 模块 | API | V0.1 状态 | 后续归属 |
|---|---|---|---|
| 系统 | GET /api/v1/health | 存活检查，不检查数据库 | 服务状态 |
| 知识图谱 | GET /api/v1/knowledge-graph/snapshot?limit=50 | 演示/Neo4j 只读，limit 1–200，关系最多 1000 条 | 本体、实体关系、查询、编辑、因果知识 |
| 数据治理 | GET /api/v1/data-governance/status | 占位能力清单，implemented 为空 | 数据源、字段映射、质量、审核与溯源 |
| 模型治理 | GET /api/v1/model-governance/status | 占位能力清单，implemented 为空 | 模型元数据、版本、评估记录、发布审批 |

OpenAPI：`/openapi.json`；交互文档：`/docs`。错误遵循 FastAPI 的 `{detail: ...}`；参数错误 422；数据库失败 503，绝不静默使用演示数据。Neo4j `elementId` 只用于当前查询，未来跨库或长期关联必须采用业务 UUID。

## 数据与服务边界

`GraphRepository` 是图谱读取接口，演示与 Neo4j 实现可替换。V0.1 没有数据库写入、文件导入、模型训练、模型推理、LLM 或内存编辑持久化。演示数据仅用于验证启动，不代表企业真实资产。Neo4j 查询使用参数和 READ 访问模式；还应为应用配置数据库只读账号。

Zhishitupu 管理企业知识、数据治理流程与模型治理元数据。prediction 独立负责预测算法、训练、推理和寿命计算；本仓库不复制预测算法或其数据库。`PREDICTION_BASE_URL` 仅预留配置，未执行任何 HTTP 调用。

未来对接需双方确认契约：请求含 request_id、asset_id、model_version、带单位的特征和 observation_time；响应含 request_id、model_version、结果/单位、不确定度与计算时间。预测服务应负责输入合法性和计算，主项目负责资产授权、调用审计与结果展示。具体 URL、鉴权、超时与错误码未约定，不能视为已实现接口。

## 上线前扩展

先增加鉴权和角色授权、审计、数据迁移与审核，再启用写入与导入；不得把当前本地只读骨架直接作为公网业务服务。迁移时用环境变量连接远程 Neo4j，保留本地数据库与正式数据库的隔离，不需要改变查询模块的边界。
