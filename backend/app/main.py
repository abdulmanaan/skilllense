from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.api.auth import router as auth_router
from app.api.graphql_schema import schema
from app.api.rest import router as rest_router
from app.core.database import async_session
from app.core.deps import get_user_by_token

app = FastAPI(title="SkillLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://skilllense-ten.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_graphql_context(request: Request) -> dict:
    """Get the context for GraphQL requests, including the authenticated user if available."""
    user = None
    auth = request.headers.get("authorization")
    if auth and auth.startswith("Bearer "):
        token = auth.removeprefix("Bearer ")
        async with async_session() as session:
            user = await get_user_by_token(token, session)
    return {"user": user}


app.include_router(rest_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")
app.include_router(GraphQLRouter(schema, context_getter=get_graphql_context), prefix="/graphql")
