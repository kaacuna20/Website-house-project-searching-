from fastapi import FastAPI
from app.routers import projects

app = FastAPI(title="House Finder API_REST Service",
    description="Api service from the webapp house finder",
    summary="""This section was made for developers use the API to get or
            post housing projects from Atlántico-Colombia.
            Type of request used mainly for suggestions (based on incomplete names).
            Users just can make request if registered and logged section to enable the section of
            "Generate API Credentials" and get the public_api_key and secret_api_key, be aware that api_key 
            is valid for 3 months, after that, you have to refresh on same section.""",
    version="0.0.1",
    terms_of_service="#",
    contact={
        "name": "kaacuna",
        "url": "https://kaacunaword.com",
        "email": "kaacuna20@gmail.com",
    },
    )

app.include_router(projects.router)