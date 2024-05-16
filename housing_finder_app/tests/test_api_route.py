from housing_finder_app.models import User, Project, db


def test_generate_token(client, app):
    data = {"name": "test_name",
            "lastname": "test_lastname",
            "city": "test_city",
            "username": 'test_user',
            "email": 'test@example.com',
            "password": 'test_password',
            "photo": "static/images/test.png"
            }
    client.post('/register', data=data, follow_redirects=True)
    # Simulate login to get access token
    form_data = {
        'email_user': 'test_user', 'password': 'test_password'
    }
    client.post('/login', data=form_data, follow_redirects=True)

    with app.app_context():
        user = db.session.execute(db.select(User).where(User.email == "test@example.com")).scalar()
        user_id = user.id
        user = db.get_or_404(User, user_id)
        assert user

    client.get("/api_key")

    response = client.get('api/token-generate')

    # Check if status code is 200 and response contains 'api_key'
    assert response.status_code == 200
    assert 'api_key' in response.json


# this apply in search by city and company
def test_search_by_location(client, app):
    project = Project(
        name="test_name_project",
        logo="test_logo_project",
        location="test_location_project",
        city="test_city_project",
        company="test_company_project",
        address="test_address_project",
        url_map="test_url_map_project",
        contact="test_contact_project",
        area=30.0,  # area is Float Field
        price=15000000,  # price is Integer Field
        type="test_type_project",
        img_url="test_img_url_project",
        description="test_description_project",
        url_website="test_url_website_project",
    )
    db.session.add(project)
    db.session.commit()

    data = {"name": "test_name",
            "lastname": "test_lastname",
            "city": "test_city",
            "username": 'test_user',
            "email": 'test@example.com',
            "password": 'test_password',
            "photo": "static/images/test.png"
            }
    client.post('/register', data=data, follow_redirects=True)
    # Simulate login to get access token
    form_data = {
        'email_user': 'test_user', 'password': 'test_password'
    }
    client.post('/login', data=form_data, follow_redirects=True)

    with app.app_context():
        user = db.session.execute(db.select(User).where(User.email == "test@example.com")).scalar()
        user_id = user.id
        user = db.get_or_404(User, user_id)
        assert user

    client.get("/api_key")

    client.get('api/token-generate')

    with app.app_context():
        user = db.session.execute(db.select(User).where(User.email == "test@example.com")).scalar()
        assert user.api_key

    response = client.get(f"/api/location?api_key=wrong_api_key&loc=wrong_location")
    assert response.status_code == 403
    assert 'error' in response.json

    with app.app_context():
        project = db.session.execute(db.select(Project).where(Project.location == "test_location_project")).scalar()
        assert project.location == "test_location_project"

    response = client.get(f"/api/location?api_key={user.api_key}&loc=wrong_location")
    assert response.status_code == 404
    assert response.json["error"] == {'Not found': "Sorry, we don't have a project at that location."}


def test_post_project(client, app):
    project = Project(
        name="test_name_project",
        logo="test_logo_project",
        location="test_location_project",
        city="test_city_project",
        company="test_company_project",
        address="test_address_project",
        url_map="test_url_map_project",
        contact="test_contact_project",
        area=30.0,  # area is Float Field
        price=15000000,  # price is Integer Field
        type="test_type_project",
        img_url="test_img_url_project",
        description="test_description_project",
        url_website="test_url_website_project",
    )
    db.session.add(project)
    db.session.commit()

    data = {"name": "test_name",
            "lastname": "test_lastname",
            "city": "test_city",
            "username": 'test_user',
            "email": 'test@example.com',
            "password": 'test_password',
            "photo": "static/images/test.png"
            }
    client.post('/register', data=data, follow_redirects=True)
    # Simulate login to get access token
    form_data = {
        'email_user': 'test_user', 'password': 'test_password'
    }
    client.post('/login', data=form_data, follow_redirects=True)

    with app.app_context():
        user = db.session.execute(db.select(User).where(User.email == "test@example.com")).scalar()
        user_id = user.id
        user = db.get_or_404(User, user_id)
        assert user

    client.get("/api_key")

    client.get('api/token-generate')

    with app.app_context():
        user = db.session.execute(db.select(User).where(User.email == "test@example.com")).scalar()
        assert user.api_key

    with app.app_context():
        project = db.session.execute(db.select(Project).where(Project.name == "test_name_project")).scalar()
        assert project.name == "test_name_project"

    response = client.post(f"/api/add?api_key={user.api_key}&name={project.name}"
                           f"&logo=other_logo&location=other_location&city=other_city"
                           f"&company=other_company&address=other_address&url_map=other_url_map"
                           f"&contact=other_contact&area=45.0&price=12342123&type=other_type"
                           f"&img_url=other_img_url&description=other_description&url_website=other_url_website")
    assert response.status_code == 500
    assert response.json["error"] == {'Internal Server Error':
                                          "Sorry, but this project already exist on the database or there is an empty  or wrong item."}


def test_update_price(client, app):
    project = Project(
        name="test_name_project",
        logo="test_logo_project",
        location="test_location_project",
        city="test_city_project",
        company="test_company_project",
        address="test_address_project",
        url_map="test_url_map_project",
        contact="test_contact_project",
        area=30.0,  # area is Float Field
        price=15000000,  # price is Integer Field
        type="test_type_project",
        img_url="test_img_url_project",
        description="test_description_project",
        url_website="test_url_website_project",
    )
    db.session.add(project)
    db.session.commit()

    data = {"name": "test_name",
            "lastname": "test_lastname",
            "city": "test_city",
            "username": 'test_user',
            "email": 'test@example.com',
            "password": 'test_password',
            "photo": "static/images/test.png"
            }
    client.post('/register', data=data, follow_redirects=True)
    # Simulate login to get access token
    form_data = {
        'email_user': 'test_user', 'password': 'test_password'
    }
    client.post('/login', data=form_data, follow_redirects=True)

    with app.app_context():
        user = db.session.execute(db.select(User).where(User.email == "test@example.com")).scalar()
        user_id = user.id
        user = db.get_or_404(User, user_id)
        assert user

    client.get("/api_key")

    client.get('api/token-generate')

    with app.app_context():
        user = db.session.execute(db.select(User).where(User.email == "test@example.com")).scalar()
        assert user.api_key

    with app.app_context():
        project = db.session.execute(db.select(Project).where(Project.price == 15000000)).scalar()
        assert project.price == 15000000

    wrong_id = 6

    response = client.patch(f"/api/update-price?api_key={user.api_key}&new_price=16000000&project_id={wrong_id}")
    assert response.status_code == 404
    assert response.json["error"] == {'Not found': "Sorry a project with that id was not found in the database."}


def test_delete_project(client, app):
    project = Project(
        name="test_name_project",
        logo="test_logo_project",
        location="test_location_project",
        city="test_city_project",
        company="test_company_project",
        address="test_address_project",
        url_map="test_url_map_project",
        contact="test_contact_project",
        area=30.0,  # area is Float Field
        price=15000000,  # price is Integer Field
        type="test_type_project",
        img_url="test_img_url_project",
        description="test_description_project",
        url_website="test_url_website_project",
    )
    db.session.add(project)
    db.session.commit()

    data = {"name": "test_name",
            "lastname": "test_lastname",
            "city": "test_city",
            "username": 'test_user',
            "email": 'test@example.com',
            "password": 'test_password',
            "photo": "static/images/test.png"
            }
    client.post('/register', data=data, follow_redirects=True)
    # Simulate login to get access token
    form_data = {
        'email_user': 'test_user', 'password': 'test_password'
    }
    client.post('/login', data=form_data, follow_redirects=True)

    with app.app_context():
        user = db.session.execute(db.select(User).where(User.email == "test@example.com")).scalar()
        user_id = user.id
        user = db.get_or_404(User, user_id)
        assert user

    client.get("/api_key")

    client.get('api/token-generate')

    with app.app_context():
        user = db.session.execute(db.select(User).where(User.email == "test@example.com")).scalar()
        assert user.api_key

    with app.app_context():
        project = db.session.execute(db.select(Project).where(Project.id == 1)).scalar()
        assert project.id == 1

    response = client.delete(f"/api/project-closed?api_key={user.api_key}&project_id=1")
    assert response.status_code == 403
    assert response.json == {'message': "You are not the administrator, you are not authorized!"}

