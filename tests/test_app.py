import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_user_registration(client):
    data = {
        "username": "testuser",
        "password": "testpass",
        "RepeatPassword": "testpass"
    }
    response = client.post('/register', json=data)
    assert response.status_code == 200
    assert b'User registered successfully' in response.data

def test_user_registration_password_mismatch(client):
    data = {
        "username": "testuser2",
        "password": "testpass",
        "RepeatPassword": "wrongpass"
    }
    response = client.post('/register', json=data)
    assert response.status_code == 400
    assert b'Passwords do not match' in response.data

def test_user_login_success(client):
    client.post('/register', json={
        "username": "testuser3",
        "password": "testpass",
        "RepeatPassword": "testpass"
    })
    response = client.post('/login', json={
        "username": "testuser3",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert b'Login successful' in response.data

def test_user_login_failure(client):
    response = client.post('/login', json={
        "username": "nonexistent",
        "password": "nopass"
    })
    assert response.status_code == 401
    assert b'Invalid credentials' in response.data

def test_add_and_get_pantry(client):
    response = client.post('/api/pantry/add', json={"ingredient": "egg"})
    assert response.status_code == 201

    response = client.get('/api/pantry')
    assert response.status_code == 200
    assert b'egg' in response.data

def test_remove_pantry_item(client):
    client.post('/api/pantry/add', json={"ingredient": "milk"})
    response = client.delete('/api/pantry/remove', json={"ingredient": "milk"})
    assert response.status_code == 200
    assert b'Ingredient removed' in response.data

    response = client.get('/api/pantry')
    assert b'milk' not in response.data

def test_add_duplicate_pantry_item(client):
    client.post('/api/pantry/add', json={"ingredient": "flour"})
    response = client.post('/api/pantry/add', json={"ingredient": "flour"})
    assert response.status_code == 409  
    assert b'Ingredient already exists' in response.data
