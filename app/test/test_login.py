from app.test.test_app import client
import json
def test_login(client):
    new_user = {
    "email":"gg@naver.com",
    "user_name":"hee"
}
    resp=client.post(
        "http://127.0.0.1:8080/login",
        data=json.dumps(new_user),
        content_type='application/json',
        follow_redirects=True
    )
    assert resp.status_code==200

    resp_json = json.loads(resp.data.decode('utf-8'))
    return (resp_json['user_id'])

