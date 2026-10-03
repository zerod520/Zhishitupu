from typing import Literal
from pydantic import BaseModel

class Node(BaseModel):
    id: str
    name: str
    labels: list[str]

class Edge(BaseModel):
    source: str
    target: str
    type: str

class GraphSnapshot(BaseModel):
    mode: Literal["demo", "neo4j"]
    read_only: bool = True
    nodes: list[Node]
    edges: list[Edge]

class ModuleStatus(BaseModel):
    module: str
    status: Literal["placeholder"] = "placeholder"
    capabilities: list[str]
    implemented: list[str] = []
