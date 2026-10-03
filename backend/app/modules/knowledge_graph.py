import logging
from fastapi import APIRouter, HTTPException, Query, Request
from ..schemas import GraphSnapshot

router = APIRouter(prefix="/knowledge-graph", tags=["知识图谱"])

@router.get("/snapshot", response_model=GraphSnapshot)
def snapshot(request: Request, limit: int = Query(default=50, ge=1, le=200)):
    try:
        return request.app.state.graph.snapshot(limit)
    except Exception:
        logging.getLogger(__name__).exception("Graph query failed")
        raise HTTPException(503, "图谱数据源不可用，请检查服务端连接配置；未切换为演示数据。")
