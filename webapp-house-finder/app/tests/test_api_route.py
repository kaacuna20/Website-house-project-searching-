from app.models import User, db


def test_generate_token(client, app):
    data = {"name": "test_name",
            "lastname": "test_lastname",
            "city": "test_city",
            "username": 'test_user',
            "email": 'test@example.com',
            "password": 'test_password',
            "photo": "static/images/test.png"
            }
    
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200
    print("Registration Response:", response.data.decode('utf-8'))
    
    
    # Simulate login to get access token
    form_data = {
        'email_user': 'test_user', 'password': 'test_password'
    }
    response = client.post('/login', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    print("Registration Response:", response.data.decode('utf-8'))
    

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


