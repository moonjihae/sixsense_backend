def is_valid(diet_id="",user_id="",param=""):
    if diet_id is None:
        return {"message": "diet_id를 입력해주세요"}
    if user_id is None:
        return {"message": "user_id를 입력해주세요"}
    if param is None:
        return {"message":f"{param}을 입력해주세요"}
