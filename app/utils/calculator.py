def calculate_nutrition(gender,age,weight,heihgt,activity_level):
    #여성일 경우
    if gender==1:
        #비활동적
        if activity_level==0:
            activity_point=1.0
        #저활동적
        elif activity_level==1:
            activity_point = 1.12
        #활동적
        elif activity_level == 2:
            activity_point = 1.27
        #매우 활동적
        elif activity_level == 3:
            activity_point = 1.45
        height=heihgt*0.01
        cal=354-(6.91*age)+activity_point*(9.36*weight+726*height)

    elif gender==2:

        # 비활동적
        if activity_level == 0:
            activity_point = 1.0
        # 저활동적
        elif activity_level == 1:
            activity_point = 1.11
        # 활동적
        elif activity_level == 2:
            activity_point = 1.25
        # 매우 활동적
        elif activity_level == 3:
            activity_point = 1.48
        height=heihgt*0.01
        cal = 662 - (9.53 * age) + activity_point * (15.91 * weight + 539.6 * height)

    carbs=cal*0.5/4
    protein=cal*0.2/4
    fat=cal*0.3/9
    return cal,carbs,protein,fat