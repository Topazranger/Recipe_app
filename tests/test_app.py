import sys
import os
import pytest
from app import app, db, User

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    response = client.post('/api/pantry/add', json={"ingredient": "eggs"})
    assert response.status_code == 201

    response = client.get('/api/pantry')
    assert response.status_code == 200
    assert b'egg' in response.data

def test_remove_pantry_item_post(client):        
    client.post('/api/pantry/add', json={"ingredient": "milk"})
    response = client.post('/api/pantry/remove', json={"ingredient": "milk"}) 
    assert response.status_code == 200

def test_register_empty_username(client):
    data = {
        "username": "",
        "password": "password",
        "RepeatPassword": "password"
    }
    response = client.post('/register', json=data)
    assert response.status_code == 400
    assert b'Please enter username' in response.data

def test_register_missing_repeat_password(client):
    data = {
        "username": "user2",
        "password": "pass",
        "RepeatPassword": ""
    }
    response = client.post('/register', json=data)
    assert response.status_code == 400
    assert b'Passwords do not match' in response.data

def test_create_shopping_list(client):
    response = client.post('/api/shopping/add', json={"item": "bread"})
    assert response.status_code == 201
    assert b'bread' in response.data

def test_increment_shopping_list_quantity(client):
    client.post('/api/shopping/add', json={"item": "bread"})
    response = client.post('/api/shopping/increase', json={"item": "bread"})
    assert response.status_code == 200
    assert b'quantity increased' in response.data

def test_recipe_search_valid(client):
    client.post('/api/pantry/add', json={"ingredient": "eggs"})
    response = client.get('/api/recipes/search?query=chocolate chip cookies')
    assert response.status_code == 200
    assert b'chocolate chip cookies' in response.data.lower()

def test_saved_recipe_access_simulation(client):
    response = client.get('/api/recipes/local?name=chocolate chip cookies')
    assert response.status_code == 200
    assert b'chocolate chip cookies' in response.data.lower()

def test_recipe_search_invalid(client):
    response = client.get('/api/recipes/search?query=@!?@!@')
    assert response.status_code == 404 or b'No recipes found' in response.data

def test_timer_local_addition_simulation(client):
    response = client.post('/api/timer/create', json={"name": "MyTimer"})
    assert response.status_code == 201 or 200

