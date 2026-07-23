import re
from app.services.skills_catalog import SKILLS_CATALOG

# Compile all regex patterns once for better performance.
_COMPILED: dict[str, list[re.Pattern]] = {
    skill: [re.compile(p, re.IGNORECASE) for p in patterns]
    for skill, (_, patterns) in SKILLS_CATALOG.items()
}

# Matches HTML tags like <p>, <div>, <li>, etc.
_HTML_TAG = re.compile(r"<[^>]+>")

def clean_text(text: str | None) -> str:
    """Remove HTML tags from job descriptions."""
    if not text:
        return ""
    return _HTML_TAG.sub(" ", text)

def extract_skills(title: str, description: str | None) -> set[str]:
    """Extract canonical skill names from a job title and description."""
    text = f"{title} {clean_text(description)}"
    # Use a set to avoid duplicate skills.
    found = set()
    # Check every skill against its compiled regex patterns.
    for skill, patterns in _COMPILED.items():
        if any(p.search(text) for p in patterns):
            found.add(skill)

    return found

# Role definitions
ROLES: dict[str, tuple[str, list[str], list[str]]] = {
    "backend": ("Backend Developer",
                ["backend", "back-end", "back end", "api engineer",
                 "python developer", "java developer", "php developer",
                 "ruby on rails", "rails developer", "node developer",
                 "node.js developer", ".net developer", "django developer"],
                ["Django", "FastAPI", "Flask", "Node.js", "Spring", "Laravel", ".NET", "Ruby on Rails"]),
    "frontend": ("Frontend Developer",
                 ["frontend", "front-end", "front end", "ui developer", "ui engineer",
                  "react developer", "vue developer", "angular developer",
                  "web developer", "javascript developer"],
                 ["React", "Vue", "Angular", "Next.js", "CSS", "Tailwind CSS"]),
    "fullstack": ("Full Stack Developer",
                  ["full stack", "full-stack", "fullstack"],
                  []),
    "mobile": ("Mobile Developer",
               ["mobile", "android developer", "ios developer", "app developer",
                "android engineer", "ios engineer", "swift developer", "kotlin developer",
                "flutter developer"],
               ["Flutter", "React Native", "Kotlin", "Swift", "Android", "iOS"]),
    "data": ("Data Scientist / Engineer",
             ["data scientist", "data engineer", "machine learning", "ml engineer",
              "ai engineer", "data analyst", "ai architect"],
             ["Pandas", "NumPy", "TensorFlow", "PyTorch", "Machine Learning", "LLMs"]),
    "devops": ("DevOps / SRE",
               ["devops", "site reliability", "sre", "platform engineer",
                "infrastructure engineer", "cloud engineer"],
               ["Docker", "Kubernetes", "Terraform", "CI/CD", "AWS", "Azure", "GCP"]),
    "qa": ("QA Engineer",
           ["qa", "quality assurance", "quality engineer", "test engineer",
            "sdet", "automation engineer"],
           []),
    "software": ("Software Engineer (General)",
                 ["software engineer", "software developer", "programmer"],
                 []),
}

def classify_role(title: str, skills: set[str]) -> str | None:
    """Return the best matching developer role, or None if no role matches."""
    title_lower = title.lower()
    # Stores the score for each matching role.
    scores: dict[str, int] = {}

    # Calculate a score for every role
    for slug, (_, keywords, skill_hints) in ROLES.items():
        if any(kw in title_lower for kw in keywords):
            scores[slug] = 3 + sum(1 for s in skill_hints if s in skills)

    if not scores:
        return None

    return max(scores, key=lambda slug: (scores[slug], slug != "software"))
