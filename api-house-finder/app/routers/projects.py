from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import Project, User
from app.database import get_db
from app.utils.auth import api_key_auth, token_auth
from app.helper.download_img import dowmload_bg_images_from_urls
from app.helper.normalize_text import normalize_text

router = APIRouter()

@router.get("/api/v1/location")
async def project_by_location(loc: str, db: Session = Depends(get_db), user: User = Depends(api_key_auth)):
    query_loc = normalize_text(loc.title())
    locate_project = db.query(Project).filter(Project.location == query_loc).all()
    if locate_project:
        return {"projects": [project.to_dict() for project in locate_project]}, 200
    else:
        raise HTTPException(status_code=404, detail="Sorry, we don't have a project at that location.")

@router.get("/api/v1/city")
async def project_by_city(city: str, db: Session = Depends(get_db), user: User = Depends(api_key_auth)):
    query_city = normalize_text(city.title())
    locate_project = db.query(Project).filter(Project.city == query_city).all()
    if locate_project:
        return {"projects": [project.to_dict() for project in locate_project]}, 200
    else:
        raise HTTPException(status_code=404, detail="Sorry, we don't have a project in that city.")

@router.get("/api/v1/company")
async def project_by_company(company: str, db: Session = Depends(get_db), user: User = Depends(api_key_auth)):
    query_company = normalize_text(company.upper())
    locate_project = db.query(Project).filter(Project.company == query_company).all()
    if locate_project:
        return {"projects": [project.to_dict() for project in locate_project]}, 200
    else:
        raise HTTPException(status_code=404, detail="Sorry, we don't have projects from that company.")

@router.get("/api/v1/project-details")
async def project(project_id: int, db: Session = Depends(get_db), user: User = Depends(api_key_auth)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        return {project.name: project.to_dict()}, 200
    else:
        raise HTTPException(status_code=404, detail="Sorry, we don't have that project.")

@router.post("/api/v1/add-project")
async def post_new_project(
    name: str, logo: str, location: str, city: str, company: str, address: str, url_map: str,
    contact: str, area: float, price: int, type: str, img_url: str, description: str, url_website: str,
    db: Session = Depends(get_db), user: User = Depends(api_key_auth)
):
    try:
        
        bg_url = dowmload_bg_images_from_urls(
                        url=img_url, 
                        project=name.lower(), 
                        company=company.lower(), 
                        destination_folder="background"
                        )
        
        logo_url = dowmload_bg_images_from_urls(
                        url=logo, 
                        project=name.lower(), 
                        company=company.lower(), 
                        destination_folder="logos"
                        )
        
        new_project = Project(
            name=normalize_text(name.title()),
            logo=logo_url,
            location=normalize_text(location.title()),
            city=normalize_text(city.title()),
            company=normalize_text(company.upper()),
            address=address.title(),
            url_map=url_map,
            contact=contact.lower(),
            area=area,
            price=price,
            type=type.upper(),
            img_url=bg_url,
            description=description,
            url_website=url_website
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return {"response": "Successfully added the new project."}, 200
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail="Sorry, but this project already exists in the database or there is an empty or wrong item.")

@router.patch("/api/v1/update-price")
async def update_new_project_price(project_id: int, new_price: int, db: Session = Depends(get_db), user: User = Depends(token_auth)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        project.price = new_price
        db.commit()
        return {"response": "Successfully updated the price."}, 200
    else:
        raise HTTPException(status_code=404, detail="Sorry, a project with that id was not found in the database.")

@router.delete("/api/v1/project-closed")
async def delete_project(project_id: int, db: Session = Depends(get_db), user: User = Depends(token_auth)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        db.delete(project)
        db.commit()
        return {"response": "Successfully deleted the project from the database."}, 200
    else:
        raise HTTPException(status_code=404, detail="Sorry, a project with that id was not found in the database.")