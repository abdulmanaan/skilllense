from pydantic import BaseModel

class SkillDemand(BaseModel):
    name: str
    category: str | None
    demand: int

class RoleOut(BaseModel):
    slug: str
    name: str
    job_count: int

class JobOut(BaseModel):
    id: int
    title: str
    company: str | None
    location: str | None
    url: str | None
    source: str
    role: str | None
    skills: list[str]

    model_config = {"from_attributes": True}
