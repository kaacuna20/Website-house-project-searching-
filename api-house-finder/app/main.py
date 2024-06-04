from fastapi import FastAPI
from app.routers import projects

app = FastAPI(title="House Finder API_REST Service",
    description="Api service from the webapp house finder",
    summary="This is api space where developers can get and post about housing projects in Atlantico-Colombia.",
    version="0.0.1",
    terms_of_service="http://localhost:5003/api-documentation",
    contact={
        "name": "kaacuna",
        "url": "http://kaacunadev.com",
        "email": "kaacuna20@gmail.com",
    },
    )

app.include_router(projects.router)