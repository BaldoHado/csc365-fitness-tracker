from fastapi import FastAPI
from src.api import workouts, users, analysis
from starlette.middleware.cors import CORSMiddleware

description = "Fitness Analyzer App for CSC 365"

app = FastAPI(
    title="Fitness-Analyzer",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Adam Ta",
        "email": "ajta@calpoly.edu",
    },
)

origins = ["https://example.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(workouts.router)
app.include_router(users.router)
app.include_router(analysis.router)


@app.get("/")
async def root():
    return {"message": "Fitness Tracker Root Endpoint"}
