from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.db_models import Project, User
from app.database import get_db
from app.utils.auth import combined_auth
from app.helper.download_img import dowmload_bg_images_from_urls
from app.helper.normalize_text import normalize_text
from app.models.pydantic_models import ProjectCreate, ProjectResponse, ProjectListResponse
from cryptography.fernet import Fernet
from os import environ
from app.logs_system.log import Logger

logger = Logger()

ENCRYPTION_KEY = environ.get('ENCRYPTION_KEY')
cipher_suite = Fernet(ENCRYPTION_KEY)

router = APIRouter(prefix='/api/v1', tags=['Housing Projects'])

@router.get("/location", response_model=ProjectListResponse, status_code=status.HTTP_200_OK)
async def project_by_location(loc: str, db: Session = Depends(get_db), user: User = Depends(combined_auth)):
    query_loc = normalize_text(loc.title())
    locate_project = db.query(Project).filter(Project.location == query_loc).all()
    if locate_project:
        logger.info(f"/api/v1/location?loc={loc} - status_code=200")
        return {"projects": locate_project}
    else:
        logger.warning(f"/api/v1/location?loc={loc} - status_code=404")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry, we don't have a project at that location.")

@router.get("/city", response_model=ProjectListResponse, status_code=status.HTTP_200_OK)
async def project_by_city(city: str, db: Session = Depends(get_db), user: User = Depends(combined_auth)):
    query_city = normalize_text(city.title())
    locate_project = db.query(Project).filter(Project.city == query_city).all()
    if locate_project:
        logger.info(f"/api/v1/city?city={city} - status_code=200")
        return {"projects": locate_project}
    else:
        logger.warning(f"/api/v1/city?city={city} - status_code=404")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry, we don't have a project in that city.")

@router.get("/company", response_model=ProjectListResponse, status_code=status.HTTP_200_OK)
async def project_by_company(company: str, db: Session = Depends(get_db), user: User = Depends(combined_auth)):
    query_company = normalize_text(company.upper())
    locate_project = db.query(Project).filter(Project.company == query_company).all()
    if locate_project:
        logger.info(f"/api/v1/company?city={company} - status_code=200")
        return {"projects": locate_project}
    else:
        logger.warning(f"/api/v1/company?company={company} - status_code=404")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry, we don't have projects from that company.")

@router.get("/project-details", response_model=ProjectResponse, status_code=status.HTTP_200_OK)
async def project(project_id: int, db: Session = Depends(get_db), user: User = Depends(combined_auth)):
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if project:
        logger.info(f"/api/v1/project-details?project_id={project_id} - status_code=200")
        return project
    else:
        logger.warning(f"/api/v1/project-details?project_id={project_id} - status_code=404")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry, we don't have that project.")

@router.post("/add-project", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def post_new_project(project: ProjectCreate = Depends(), db: Session = Depends(get_db), user: User = Depends(combined_auth)):
    try:
        bg_url = dowmload_bg_images_from_urls(
                        url=project.img_url, 
                        project=project.name.lower(), 
                        company=project.company.lower(), 
                        destination_folder="background"
                        )
        
        logo_url = dowmload_bg_images_from_urls(
                        url=project.logo, 
                        project=project.name.lower(), 
                        company=project.company.lower(), 
                        destination_folder="logos"
                        )
        
        new_project = Project(
            name=normalize_text(project.name.title()),
            logo=logo_url,
            location=normalize_text(project.location.title()),
            city=normalize_text(project.city.title()),
            company=normalize_text(project.company.upper()),
            address=project.address.title(),
            contact=project.contact.lower(),
            area=project.area,
            price=project.price,
            type=project.type.upper(),
            img_url=bg_url,
            description=project.description,
            url_website=project.url_website,
            latitude=project.latitude,
            longitude=project.longitude
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        logger.info(f"/api/v1/add-project?{project} - status_code=201")
        return new_project
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Sorry, but this project already exists in the database or there is an empty or wrong item.")

@router.patch("/update-price", response_model=ProjectResponse, status_code=status.HTTP_200_OK)
async def update_new_project_price(project_id: int, new_price: int, admin_api_key: str, db: Session = Depends(get_db), user: User = Depends(combined_auth)):
    decrypted_key = cipher_suite.decrypt(user.admin_api_key.encode('utf-8')).decode('utf-8')
    if not decrypted_key == admin_api_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid admin_api_key!")
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if project:
        project.price = new_price
        db.commit()
        logger.info(f"/api/v1/update-price?project_id={project_id}&new_price={new_price}&admin_api_key={admin_api_key}  - status_code=200")
        return project
    else:
        logger.warning(f"/api/v1/update-price?project_id={project_id}&new_price={new_price}&admin_api_key={admin_api_key}  - status_code=404")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry, a project with that id was not found in the database.")

@router.delete("/project-closed", status_code=status.HTTP_200_OK)
async def delete_project(project_id: int, admin_api_key: str, db: Session = Depends(get_db), user: User = Depends(combined_auth)):
    decrypted_key = cipher_suite.decrypt(user.admin_api_key.encode('utf-8')).decode('utf-8')
    if not decrypted_key == admin_api_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid admin_api_key!")
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if project:
        db.delete(project)
        db.commit()
        logger.info(f"/api/v1/project-closed?project_id={project_id}&admin_api_key={admin_api_key}  - status_code=200")
        return {"response": "Successfully deleted the project from the database."}
    else:
        logger.warning(f"/api/v1/project-closed?project_id={project_id}&admin_api_key={admin_api_key}  - status_code=404")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry, a project with that id was not found in the database.")

