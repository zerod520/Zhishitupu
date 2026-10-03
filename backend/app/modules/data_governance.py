from fastapi import APIRouter
from ..schemas import ModuleStatus

router = APIRouter(prefix="/data-governance", tags=["数据治理"])

@router.get("/status", response_model=ModuleStatus)
def status():
    return ModuleStatus(module="data-governance", capabilities=["数据源登记", "字段映射", "质量校验", "审核发布与溯源"])
