from app.test.test_app import client
from app.test.test_login import test_login
import json
def test_user(client):
    new_user_id=test_login(client)
    #프로필 수정
    resp = client.put(
        "http://127.0.0.1:8080/users",
        data=json.dumps({
            "user_id": new_user_id,
            "age": 25,
            "gender": 1,
            "height": 155,
            "weight": 45,
            "activity_level": 1
        }),
        content_type='application/json',
        follow_redirects=True
    )
    assert resp.status=='200 OK'

    #회원삭제
    resp = client.delete(
        f"http://127.0.0.1:8080/users/account?user_id={new_user_id}",
        follow_redirects=True
    )
    assert resp.status=='200 OK'