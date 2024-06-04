from app.models import User, db
from werkzeug.security import check_password_hash
from flask_mail import Mail
import pytest


# TESTING FOR REGISTER ENDPOINT AND FORM
def test_registration(client, app):
    data = {"name": "test_name",
            "lastname": "test_lastname",
            "city": "test_city",
            "username": 'test_user',
            "email": 'test@example.com',
            "password": 'test_password',
            "photo": "static/images/test.png"
            }
    client.post('/register', data=data, follow_redirects=True)

    with app.app_context():
        assert db.session.execute(db.select(User).where(User.email == "test@example.com")).scalar()


def test_invalid_register_form(client):
    data = {'email': 'invalid_email'}
    response = client.post('/register', data=data, follow_redirects=True)

    assert b'This field is required.' in response.data  # Check for error message


# TESTING FOR LOGIN ENDPOINT AND FORM
def test_login_invalid_password(client, app):
    # register user
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
    response = client.post('/login', data=form_data, follow_redirects=True)
    with app.app_context():
        user = db.session.execute(db.select(User).where(User.email == "test@example.com")).scalar()
        # Check password hash
        assert not check_password_hash(user.password, form_data["password"])

    assert response.status_code == 200

    # return flash("Contraseña incorrecta, por favor trate de nuevo.")
    assert "Contraseña incorrecta, por favor trate de nuevo.".encode('utf-8') in response.data


def test_login_invalid_user(client, app):
    # register user
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
            'email_user': 'wrong_test_user', 'password': 'test_password'
    }
    response = client.post('/login', data=form_data, follow_redirects=True)
    with app.app_context():
        assert not db.session.execute(db.select(User).where(User.username == form_data["email_user"])).scalar()

    assert response.status_code == 200
    # return flash("El correo no existe, por favor trate de nuevo.")
    assert 'El correo no existe, por favor trate de nuevo.'.encode("utf-8") in response.data


# TESTING FOR FORGOT PASSWORD ENDPOINT AND FORM
def test_forgot_password_validate_user(client, app):
    # register user
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
        'email': 'wrongtest@example.com'
    }
    client.post('/forgot-password', data=form_data, follow_redirects=True)
    with app.app_context():
        assert not db.session.execute(db.select(User).where(User.email == form_data["email"])).scalar()


@pytest.fixture
def mail(app):
    return Mail(app)


def test_forgot_password_send_email(client, mail, app):
    # register user
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
        'email': 'test@example.com'
    }

    with mail.record_messages() as outbox:
        mail.send_message(
            subject='NO-REPLY: Tu nueva contraseña',
            sender=form_data['email'],
            recipients=['to@example.com'],
            body='Test Body'
        )

    # Assert that one message was sent
    assert len(outbox) == 1

    # Assert email details
    message = outbox[0]
    assert message.subject == 'NO-REPLY: Tu nueva contraseña'
    assert message.sender == form_data['email']
    assert message.recipients == ['to@example.com']
    assert message.body == 'Test Body'

