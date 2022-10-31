from app.main.model.user import User
from app.main.persistance import authdao
from app.main.services import authservice


def test_create_user():
    PASSWORD = 'test'
    user = User(email="hey@hey.be", password=PASSWORD)
    bearer1 = authservice.register(user)
    assert bearer1
    bearer2 = authservice.login(user.email, PASSWORD)
    assert bearer2
    authdao.delete_user(user.id)



