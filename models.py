from pydantic import BaseModel, Field, conlist
from typing import Optional, Dict
from datetime import datetime

class Contributor(BaseModel):
    name: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    roles: conlist(str, min_length=1)

class ProjectMeta(BaseModel):
    name: str = Field(..., min_length=3, pattern=r"^[A-Z][a-z0-9_-]+$")
    description: Optional[str]
    dependencies: Dict[str, str]
    contributors: list[Contributor]
    created_at: datetime = datetime.now()

    @classmethod
    def from_yaml(cls, path: str):
        import yaml
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)
