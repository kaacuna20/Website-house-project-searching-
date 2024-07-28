from pydantic import BaseModel, HttpUrl
from typing import List

class ProjectCreate(BaseModel):
    name: str
    logo: HttpUrl
    location: str
    city: str
    company: str
    address: str
    contact: str
    area: float
    price: int
    type: str
    img_url: HttpUrl
    description: str
    url_website: HttpUrl
    latitude: float
    longitude: float

class ProjectResponse(BaseModel):
    project_id: int
    name: str
    logo: str 
    location: str
    city: str
    company: str
    address: str
    contact: str
    area: float
    price: int
    type: str
    img_url: str
    description: str
    url_website: str
    slug: str
    latitude: float
    longitude: float

    class Config:
        orm_mode: True

class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]

    class Config:
        orm_mode: True
