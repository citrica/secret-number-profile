import os
import pytest
from main import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    client = app.test_client()

    cleanup()  # clean up before every test

    db.create_all()

    yield client


def cleanup():
    # clean up/delete the DB (drop all tables in the database)
    db.drop_all()


def test_index_not_logged_in(client):
    response = client.get('/')
    assert b'Enter your name' in response.data


def test_index_logged_in(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    response = client.get('/')
    assert b'Enter your guess' in response.data


def test_profile_check(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    response = client.get('/profile')
    assert b'Test User' in response.data


def test_profile_edit(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    response = client.get('/profile/edit')
    assert b'Edit your profile' in response.data

    response = client.post('/profile/edit', data={"profile-name": "Test New User",
                                                  "profile-email": "edit.profile.user@newuser.com"}, follow_redirects=True)

    assert b'Test New User' in response.data
    assert b'edit.profile.user@newuser.com' in response.data

