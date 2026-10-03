from fastapi import APIRouter
from ..schemas import ModuleStatus

router = APIRouter(prefix="/model-governance", tags=["模型治理"])

@router.get("/status", response_model=ModuleStatus)
def status():
    return ModuleStatus(module="model-governance", capabilities=["模型登记", "版本与评估记录", "发布审批", "prediction 服务契约管理"])
