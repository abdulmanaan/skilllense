import strawberry

@strawberry.type
class SkillType:
    name: str
    category: str | None
    demand: int

@strawberry.type
class JobType:
    id: int
    title: str
    company: str | None
    location: str | None
    url: str | None
    source: str

@strawberry.type
class RoleType:
    slug: str
    name: str
    job_count: int
    top_skills: list[SkillType]
