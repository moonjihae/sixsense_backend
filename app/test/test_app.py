import os
import pytest
from app.__init__ import create_app
from app.database import db,migrate
import tempfile
@pytest.fixture()
def client():
    db_fd,db_path=tempfile.mkstemp()
    app=create_app('test')
    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            migrate.init_app(app, db, render_as_batch=True)
        yield client
    os.close(db_fd)
    os.unlink(db_path)

def setup_function():
    new_user=[{'email':"test@test.com","user_name":"test"}]
    db.User(new_user)

