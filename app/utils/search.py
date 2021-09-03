from app.database import db,conn
import json
from sqlalchemy.exc import NoResultFound
def search_food(name=None,purpose=None,carbs=None,protein=None,fat=None,no=None):
    #purpose가 식단 등록일때
    cursor=conn.cursor()
    if purpose=="write":

        cursor.execute("select no,name,cal,carbs,protein,fat from 식품영양성분db where name like %s and Commercial_products='품목대표';",(name,))
        exist = cursor.fetchall()
        if not exist:
            cursor.execute("select no, name,cal,carbs,protein,fat from 식품영양성분db where name like %s;",(name,))
            exist = cursor.fetchall()

            if not exist:
                name='%'+name+'%'
                cursor.execute("select no,name,cal,carbs,protein,fat from 식품영양성분db where name like %s;",(name,))
                exist = cursor.fetchall()
            else:
                pass
        else:
            pass


        cursor.close()
        return exist
    #purpose가 음식 검색 일때
    if purpose=='search':
        name ='%'+name+'%'
        cursor.execute(
            "select no,name,cal from 식품영양성분db where name like %s and Commercial_products='품목대표';",(name,))
        exist = cursor.fetchall()
        if not exist:

            cursor.execute(
                "select no,name,cal from 식품영양성분db where name like %s and Commercial_products='상용제품';",(name,))
            exist=cursor.fetchall()
        else:
            pass
        row_headers=[column[0]for column in cursor.description]
        json_data=[]
        for idx in exist:
            json_data.append(dict(zip(row_headers,idx)))
        cursor.close()

        return json_data

    if purpose=="delete" or purpose=="modify":
        cursor.execute(
            "select no,name,cal,carbs,protein,fat from 식품영양성분db where no=%s;",
            (name,))

        exist=cursor.fetchall()
        cursor.close()
        return exist

    if purpose=='recommend':
        cursor.execute(
            "select no,name,cal,carbs,protein,fat,Category from 식품영양성분db where Commercial_products='품목대표'"
            "and Category not in ('곡류 및 서류','음료 및 차류','과자류','포류','농축산물') "
            "and Detailed_classification not in ('케이크류','튀김빵류(도넛, 꽈배기 등)','크림빵류','페이스트리류','앙금빵류')"
            " and carbs between %s and %s and protein between %s and %s and fat between %s and %s group by Category;",
            (carbs*0.6,carbs*1.4,protein*0.6,protein*1.4,fat*0.85,fat*1.15))
        exist=cursor.fetchall()
        if not exist:
            return 0
        row_headers = [column[0] for column in cursor.description]
        json_data = []
        for idx in exist:
            json_data.append(dict(zip(row_headers, idx)))
        cursor.close()

        return json_data

    if purpose=='like':
        cursor.execute("select name from 식품영양성분db where no= %s ;",(no))
        exist=cursor.fetchall()
        cursor.close()
        if not exist:
            return 0
        else:
            return exist


