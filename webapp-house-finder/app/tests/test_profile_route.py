from io import BytesIO
from app.models import User, db
from werkzeug.security import check_password_hash


def test_update_file_pdf_photo_profile(client, app):
    data = {"name": "test_name",
            "lastname": "test_lastname",
            "city": "test_city",
            "username": 'test_user',
            "email": 'test@example.com',
            "password": 'test_password',
            "photo": "static/images/test.png"
            }
    client.post('/register', data=data, follow_redirects=True)

    form_data = {
        'username': 'test_user', 'password': 'test_password'
    }
    client.post('/login', data=form_data, follow_redirects=True)
    client.get("/profile")

    data = {
        'image_file': (BytesIO(b'my file contents'), 'test.pdf')
    }
    response = client.post('/profile', content_type='multipart/form-data', data=data, follow_redirects=True)

    assert response.status_code == 200
    # return flash("Archivo no valido.")
    assert b"Archivo no valido." in response.data


def test_change_password(client, app):
    data = {"name": "test_name",
            "lastname": "test_lastname",
            "city": "test_city",
            "username": 'test_user',
            "email": 'test@example.com',
            "password": 'test_password',
            "photo": "static/images/test.png"
            }
    client.post('/register', data=data, follow_redirects=True)

    form_data = {
        'email_user': 'test_user', 'password': 'wrong_password'
    }
    client.post('/login', data=form_data, follow_redirects=True)
    client.get("/change-password")

    data = {
        "current_password": "wrong_password",
        "new_password": "new_password",
        "verificate_password": "new_password",
    }

    response = client.post("/change-password", data=data, follow_redirects=True)

    with app.app_context():
        user = db.session.execute(db.select(User).where(User.email == "test@example.com")).scalar()
        # Check password hash
        assert not check_password_hash(user.password, data["current_password"])

    assert response.status_code == 200
    # return flash("Contraseña incorrecta, por favor trate de nuevo.")
    assert "Contraseña incorrecta, por favor trate de nuevo.".encode('utf-8') in response.data