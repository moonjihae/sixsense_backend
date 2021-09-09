import os
import cv2
import numpy as np
import time
from app.utils.class_info import class_name,class_dict
from PIL import ImageFont, ImageDraw, Image
import matplotlib.pyplot as plt
import unicodedata


# size = 모델 학습할 때 설정했던 값
def image_preprocessing(img, size):
    # img = cv2.imread('kite.jpg')
    print('image shape:', img.shape)

    net_input_image = cv2.dnn.blobFromImage(img, scalefactor=1 / 255, size=size, swapRB=True, crop=False)
    print('type : ', type(img))
    print('shape :', img.shape)
    print('size :', img.size)

    return img, net_input_image


# image_preprocessing(1, (416, 416))

def load_model(origin_image, input):
    current_dir = os.path.abspath('.')
    weight_dir = os.path.join(current_dir, 'yolo_model/yolov4-custom_best.weights')
    config_dir = os.path.join(current_dir, 'yolo_model/yolov4-custom.cfg')

    yolo_net = cv2.dnn.readNetFromDarknet(config_dir, weight_dir)
    layer_name = yolo_net.getLayerNames()
    # getUnconnectedOutLayers() -> 연결되지 않은 출력이 있는 레이어의 인덱스를 반환
    outlayer_names = [layer_name[i[0] - 1] for i in yolo_net.getUnconnectedOutLayers()]
    print('output_layer_name:', outlayer_names)
    # origin_image, input = image_preprocessing(1,(416, 416))

    yolo_net.setInput(input)
    start_time = time.time()
    detect_result = yolo_net.forward(outlayer_names)  # inference 후 원하는 layer의 feature map 정보 추출 (예측된 경계상자 정보 있음)
    # print('detect_result 길이:', len(detect_result))
    # print(detect_result)

    # print('detect 시간:', round(time.time() - start_time, 2), '초')
    return get_object_info(detect_result, origin_image)
    # return detect_result -> detection 수행한 결과


def get_object_info(detect_result, image):
    row = image.shape[0]
    col = image.shape[1]

    # 이 값이 작을수록 많은 클래스를 잡아냄
    conf_threshold = 0.2
    # 이 값이 작을수록 겹쳐진 네모가 많아짐
    nms_threshold = 0.2

    class_index = []
    confidence_list = []
    boxe_list = []

    output = detect_result
    colors = np.random.uniform(0, 255, size=(len(class_name), 3))
    predict_class=[]

    # 3개의 개별 output layer별로 detection 정보 추출과 시각화
    for output_layer in output:
        print('output shape:', output_layer.shape)
        # 각 output_layer에서 검출된 객체만큼 반복
        for detection in output_layer:
            scores = detection[5:]
            # score에서 가장 높은 값이 class confidence
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > conf_threshold:
                # detection 후 반환된 좌표인 중심좌표와 너비.높이를 이미지크기에 맞게 변환하고 사각형을 그리기 위한 좌표로 변환
                center_x = int(detection[0] * col)
                center_y = int(detection[1] * row)
                width = int(detection[2] * col)
                height = int(detection[3] * row)
                x_left_top = int(center_x - width / 2)
                y_left_top = int(center_y - height / 2)

                class_index.append(class_id)
                confidence_list.append(float(confidence))
                boxe_list.append([x_left_top, y_left_top, width, height])
                print('class_id', class_id, 'confidence:', confidence)

    # 경계박스에 대해 nms를 적용하여 겹치는 박스 제거
    apply_nms_box = cv2.dnn.NMSBoxes(boxe_list, confidence_list, conf_threshold, nms_threshold)
    # print(apply_nms_box)  # 해당 인덱스의 박스만 남음

    # 이미지 위에 사각형 그리고 클래스 이름 나타내기
    draw_image = image.copy()
    if len(apply_nms_box) > 0:
        for idx in apply_nms_box.flatten():
            box = boxe_list[idx]
            x = box[0]
            y = box[1]
            width = box[2]
            height = box[3]

            border_color = colors[class_index[idx]]
            caption = "{}: {:.4f}".format(class_name[class_index[idx]], confidence_list[idx])


            predict_class.append({
                 "name":class_dict[class_index[idx]],
                 })
            # 유니코드 처리 방식을 변경 -> 자음 모음 분리문제 해결
            object_class = unicodedata.normalize('NFC', class_name[class_index[idx]])

            size, _ = cv2.getTextSize(object_class, cv2.FONT_HERSHEY_PLAIN, 1, 40)

            label_location_x = int(x + width / 2)
            label_location_y = int(y + height / 2)
            cv2.rectangle(draw_image, (label_location_x, label_location_y),
                          (label_location_x + size[0], label_location_y + size[1] + 20), border_color,
                          -1)  # 클래스 이름이 적힌 위치에 그림 그리기
            cv2.rectangle(draw_image, (int(x), int(y)), (int(x + width), int(y + height)), color=border_color,
                          thickness=4)
            # cv2.putText(draw_image, caption, (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            #### 클래스를 한글로 표현하기 위한 작업
            # content_edit = unicodedata.normalize('NFC', class_name[class_index[idx]])
            draw_image = Image.fromarray(draw_image)
            font = ImageFont.truetype('font/NanumSquare_0.ttf', 40)
            draw = ImageDraw.Draw(draw_image)
            # draw.text((x, y-size[1]-25),  object_class, font=font, fill=(0,0,0))
            draw.text((label_location_x, label_location_y), object_class, font=font, fill=(0, 0, 0))
            draw_image = np.array(draw_image)
            #######################
            print(caption, (int(x), int(y)), (int(x + width), int(y + height)))

    img_rgb = cv2.cvtColor(draw_image, cv2.IMREAD_COLOR)
    # cv2.imwrite('res.jpg', img_rgb)
    return predict_class,img_rgb


# origin_image, input = image_preprocessing(1, (416, 416))
# load_model(origin_image, input)