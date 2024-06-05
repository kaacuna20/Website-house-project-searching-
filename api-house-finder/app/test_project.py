from .main import app
from fastapi.testclient import TestClient
from .models import User, Project
from .database import get_db
from app.routers.projects import router
from os import environ


client = TestClient(app)


def test_project_by_location():
    headers = {
        "api_key":environ.get('TEST_APIKEY')
    }
     
    # Test case where project doesn't exist at the given location
    response = client.get("/api/v1/location?loc=Nonexistent Location", headers=headers)  
    assert response.status_code == 404
    assert response.json() == {"detail": "Sorry, we don't have a project at that location."}
    
    headers = {
        "api_key":"wrong_header"
    }
    # Test case where wrong api_key is given
    response = client.get("/api/v1/location?loc=ciudad mallorquin", headers=headers) 
    assert response.status_code == 403 #Sorry, that's not allowed. Make sure you have the correct api_key or apikey expired.
    assert response.json() == {"detail": "Sorry, that's not allowed. Make sure you have the correct api_key or apikey expired."}
      
def test_project_by_city():
    headers = {
        "api_key":environ.get('TEST_APIKEY')
    }
    
    # Test case where project doesn't exist at the given city
    response = client.get("/api/v1/city?city=Nonexistent city", headers=headers)  
    assert response.status_code == 404
    assert response.json() == {"detail": "Sorry, we don't have a project in that city."}
    
    
def test_project_by_company():
    headers = {
        "api_key":environ.get('TEST_APIKEY')
    }
    # Test case where project doesn't exist at the given company
    response = client.get("/api/v1/company?company=Nonexistent company", headers=headers)  
    assert response.status_code == 404
    assert response.json() == {"detail": "Sorry, we don't have projects from that company."}

def test_project():  
    # Test case where project doesn't exist at the given id
    headers = {
        "api_key":environ.get('TEST_APIKEY')
    }
    wrong_id=1
    response = client.get(f"/api/v1/project-details?project_id={wrong_id}", headers=headers)  
    assert response.status_code == 404
    assert response.json() == {"detail": "Sorry, we don't have that project."}
    
def test_post_new_project():
    headers = {
        "api_key":environ.get('TEST_APIKEY')
    }
     # Test case where add project with wrong items in area
    exist_name_project = "makani"
    
    response = client.post(f"/api/v1/add-project?name={exist_name_project}"
                           f"&logo=other_logo&location=other_location&city=other_city"
                           f"&company=other_company&address=other_address&url_map=other_url_map"
                           f"&contact=other_contact&area=60&price=12342123&type=other_type"
                           f"&img_url=other_img_url&description=other_description&url_website=other_url_website", headers=headers) 
    assert response.status_code == 500
    assert response.json() == {"detail": "Sorry, but this project already exists in the database or there is an empty or wrong item."}
    
def test_update_new_project_price():
    headers = {
        "api_key":environ.get('TEST_APIKEY'),
        "token-secret":environ.get('TEST_TOKEN')
    }
     # Test case where add project with wrong id
    wrong_id=194856730298670942
    response = client.patch(f"/api/v1/update-price?project_id={wrong_id}&new_price=123000000", headers=headers) 
    assert response.status_code == 404
    assert response.json() == {"detail": "Sorry, a project with that id was not found in the database."}
    
    
    
def test_delete_project():
    headers = {
        "api_key":environ.get('TEST_APIKEY'),
        "token-secret":environ.get('TEST_TOKEN')
    }
     # Test case where add project with wrong id
    wrong_id=1439894856329485
    response = client.delete(f"/api/v1/project-closed?project_id={wrong_id}", headers=headers) 
    assert response.status_code == 404
    assert response.json() == {"detail": "Sorry, a project with that id was not found in the database."}