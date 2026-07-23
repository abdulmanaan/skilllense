from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.rest import router as rest_router
from app.api.auth import router as auth_router
from strawberry.fastapi import GraphQLRouter
from app.api.graphql_schema import schema

app = FastAPI(title="Skilllens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rest_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")
app.include_router(GraphQLRouter(schema), prefix="/graphql")
