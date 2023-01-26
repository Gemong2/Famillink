import threading

import cv2
import numpy as np
import paho.mqtt.client as mqtt
import json
from json import JSONEncoder
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        t1 = threading.Thread(target=opencv_publish)
        t1.start()
    else:
        print("Bad connection Returned code=", rc)


def opencv_publish():
    global camera, client
    while True:
        ret, image = camera.read()
        if not ret:
            print("dont read cam")
            break
        # client.publish("/local/opencv/", json.dumps(image, cls=NumpyArrayEncoder), 2)

        # Show the image in a window
        # cv2.imshow('Webcam Image', image)

        ############################
        #                          #
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        with mp_face_detection.FaceDetection(
                model_selection=0, min_detection_confidence=0.5) as face_detection:

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image)

            # Draw the face detection annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.detections:
                for detection in results.detections:
                    # mp_drawing.draw_detection(image, detection)
                    # bbox_drawing_spec = mp_drawing.DrawingSpec()
                    # mp_drawing.draw_detection(image, detection)
                    image_rows, image_cols, _ = image.shape
                    location = detection.location_data
                    relative_bounding_box = location.relative_bounding_box
                    rect_start_point = mp_drawing._normalized_to_pixel_coordinates(
                        relative_bounding_box.xmin, relative_bounding_box.ymin, image_cols,
                        image_rows)
                    rect_end_point = mp_drawing._normalized_to_pixel_coordinates(
                        relative_bounding_box.xmin + relative_bounding_box.width,
                        relative_bounding_box.ymin + relative_bounding_box.height, image_cols,
                        image_rows)

                    if rect_start_point is None or rect_end_point is None:
                        image = np.zeros((224, 224, 3), np.uint8)
                        break
                    if None in rect_start_point or None in rect_end_point:
                        image = np.zeros((224, 224, 3), np.uint8)
                        break

                    image = image[rect_start_point[1]:rect_end_point[1], rect_start_point[0]:rect_end_point[0]]
                    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
            else:
                image = np.zeros((224, 224, 3), np.uint8)
            # Flip the image horizontally for a selfie-view display.
        # cv2.imshow("dd", image)
        ############################
        data = {
            "image": image
        }
        client.publish("/local/opencv/", json.dumps(data, cls=NumpyArrayEncoder), 2) # TODO: 해제
        print("publish opencv data")
        cv2.waitKey(150)  # MQTT 성능에 따라 유도리 있게 설정


camera = cv2.VideoCapture(1)

client = mqtt.Client()

# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
client.on_connect = on_connect

# address : localhost, port: 1883 에 연결
client.connect('localhost', 1883)
client.loop_start()

while True:
    pass