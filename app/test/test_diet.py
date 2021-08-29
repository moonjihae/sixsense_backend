from app.test.test_app import client
from app.test.test_login import test_login
import json
from app.models.diet import Diet

def test_diet_post(client):
    new_user_id=test_login(client)
    # 식단 등록
    resp = client.post(
        "http://127.0.0.1:8080/diets",
        data=json.dumps({
            "user_id": new_user_id,
            "created_at":"2021-08-10",
            "meal":2,
            "food_list": [{"name": "샌드위치", "amount": 1}, {"name": "블랙커피", "amount": 1}]
        }),
        content_type='application/json',
        follow_redirects=True
    )
    resp_json= json.loads(resp.data.decode('utf-8'))
    assert resp_json['diet_id'] is not None
    #리스트 조회
    list_resp = client.post(
        "http://127.0.0.1:8080/diets/list",
        data=json.dumps({
            "user_id": new_user_id,
            "created_at": "2021-08-10",
            "meal": 4
        }),
        content_type='application/json',
        follow_redirects=True
    )

    list_resp_json = json.loads(list_resp.data.decode('utf-8'))
    assert len(list_resp_json['diet_list'])>=1

    #그래프 조회
    grape_resp = client.post(
        "http://127.0.0.1:8080/diets/grape",
        data=json.dumps({
            "user_id": new_user_id,
            "start_date": "2021-08-10",
            "end_date": "2021-08-10"
        }),
        content_type='application/json',
        follow_redirects=True
    )
    grape_resp_json=json.loads(grape_resp.data.decode('utf-8'))
    assert len(grape_resp_json['nutrition_list'])>=1

    #식단 추천
    rec_resp = client.get(
        f"http://127.0.0.1:8080/diets/recommend?user_id={new_user_id}",
        content_type='application/json',
        follow_redirects=True
    )

    assert rec_resp.status=='200 OK'

    #식단 추천 좋아요
    like_resp = client.get(
        f"http://127.0.0.1:8080/diets/recommend/like?user_id={new_user_id}&no=2",
        content_type='application/json',
        follow_redirects=True
    )

    assert like_resp.status == '200 OK'


def test_diet_get(client):
    #식단 개별 조회
    new_user_id = test_login(client)
    diet = Diet.query.order_by(Diet.diet_id.desc()).first()
    diet_id=diet.diet_id
    resp = client.get(
        f"http://127.0.0.1:8080/diets?diet_id={diet_id}",

        follow_redirects=True
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    print(resp_json)
    assert resp_json['diet_id']==diet_id

    return diet_id,new_user_id
def test_diet_put(client):
    #식단 수정

    diet_id ,new_user_id= test_diet_get(client)
    resp = client.put(
        "http://127.0.0.1:8080/diets",
        data=json.dumps({
            "user_id": new_user_id,
            "diet_id": diet_id,
            "food_info":[
      {
            "no": 10557,
            "cal": 218.0,
            "name": "샌드위치",
            "amount": 1.5
        },
        {
            "no": 10790,
            "cal": 2.0,
            "name": "블랙커피",
            "amount": 1
        }
  ]
        }),
        content_type='application/json',
        follow_redirects=True
    )
    assert resp.status == '200 OK'



def test_diet_delete(client):
    #식단 삭제
    new_user_id = test_login(client)
    diet=Diet.query.order_by(Diet.diet_id.desc()).first()
    diet_id=diet.diet_id
    delete_resp = client.delete(
        f"http://127.0.0.1:8080/diets?diet_id={diet_id}&user_id={new_user_id}",
        follow_redirects=True
    )
    assert delete_resp.status=='200 OK'

def test_diet_search(client):
    search_resp = client.get(
        f"http://127.0.0.1:8080/diets/search?food_name=샌드위치",
        follow_redirects=True
    )
    assert search_resp.status == '200 OK'