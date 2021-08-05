import cv2
import numpy as np
import tensorflow
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from time import sleep
import datetime
from uuid import uuid4
import os
import firebase_admin
from firebase_admin import credentials, storage, db

now = datetime.datetime.now().strftime('%Y-%m-%d')

PROJECT_ID = "image-6a44b"
cred = credentials.Certificate("C:/Users/KNU/Desktop/DeepLearning/image-6a44b-firebase-adminsdk-e9t0o-daac75880e.json") #(키 이름 ) 부분에 본인의 키이름을 적어주세요.
default_app = firebase_admin.initialize_app(cred,{'storageBucket':"image-6a44b.appspot.com", 'databaseURL' : 'https://image-6a44b-default-rtdb.firebaseio.com/'})


#버킷은 바이너리 객체의 상위 컨테이너이다. 버킷은 Storage에서 데이터를 보관하는 기본 컨테이너이다.




bucket = storage.bucket()#기본 버킷 사용

def fileUpload(file):
    blob = bucket.blob('image_store/'+ file) #저장한 사진을 파이어베이스 storage의 image_store라는 이름의 디렉토리에 저장
    #new token and metadata 설정
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token} #access token이 필요하다.
    blob.metadata = metadata
    #upload file
    blob.upload_from_filename(filename=file, content_type='image/png') #파일이 저장된 주소와 이미지 형식(jpeg도 됨)
    #debugging hello
    print("hello ")
    print(blob.public_url)



face_detection = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
emotion_classifier = load_model('emotion_model.hdf5', compile=False)
EMOTIONS = ["Angry", "Disgusting", "Fearful", "Happy", "Sad", "Surprising", "Neutral"]

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detection.detectMultiScale(gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(30, 30))

    canvas = np.zeros((250, 300, 3), dtype="uint8")

    if len(faces) > 0:
        face = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = face
        # Resize the image to 48x48 for neural network
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (48, 48))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        preds = emotion_classifier.predict(roi)[0]
        emotion_probability = np.max(preds)
        label = EMOTIONS[preds.argmax()]

        cv2.putText(frame, label, (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        cv2.rectangle(frame, (fX, fY), (fX + fW, fY + fH), (0, 0, 255), 2)

        # 확률, 감정 print
        for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
            text = "{}: {:.2f}%".format(emotion, prob * 100)
            w = int(prob * 300)
            cv2.rectangle(canvas, (7, (i * 35) + 5), (w, (i * 35) + 35), (0, 0, 255), -1)
            cv2.putText(canvas, text, (10, (i * 35) + 23), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)


    cv2.imshow('Emotion Recognition', frame)
    cv2.imshow("Probabilities", canvas)
    
    
    
    # c to capture
    if cv2.waitKey(1) & 0xFF == ord('c'):
        sleep(1)
        cv2.imwrite("C:/Users/KNU/Desktop/" + str(now) + str(label) + ".png", frame)
        fileUpload("C:/Users/KNU/Desktop/" + str(now) + str(label) + ".png")
        ref = db.reference(str(now))
        ref.update({"emotion":label})
        print(label)
        cv2.imshow('capture!', frame)

    # # q to quit
    # elif cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

camera.release()

cv2.destroyAllWindows()
