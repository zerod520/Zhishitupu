from pathlib import Path
from typing import Literal
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", env_file_encoding="utf-8", extra="ignore")
    app_name: str = "燃气安全知识图谱系统"
    host: str = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)
    reload: bool = False
    graph_backend: Literal["demo", "neo4j"] = "demo"
    neo4j_uri: str = "bolt://127.0.0.1:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""
    neo4j_database: str = "neo4j"
    prediction_base_url: str = ""

    @model_validator(mode="after")
    def require_credentials(self):
        if self.graph_backend == "neo4j" and not self.neo4j_password:
            raise ValueError("NEO4J_PASSWORD is required in neo4j mode")
        return self
