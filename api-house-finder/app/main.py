from fastapi import FastAPI
from app.routers import projects

app = FastAPI(title="House Finder API_REST Service",
    description="Api service from the webapp house finder",
    summary="This is api space where developers can get and post about housing projects in Atlantico-Colombia.",
    version="0.0.1",
    terms_of_service="http://localhost/api-documentation",
    contact={
        "name": "kaacuna",
        "url": "https://kaacunaword.com/",
        "email": "kaacuna20@gmail.com",
    },
    )

app.include_router(projects.router)