import serial
from uuid import uuid4
import os
import firebase_admin
from firebase_admin import credentials, storage, db
import datetime

now = datetime.datetime.now().strftime('%Y-%m-%d')

PROJECT_ID = "graphtest-2c3b1"
cred = credentials.Certificate("C:/Users/KNU/Desktop/0804/graphtest-2c3b1-firebase-adminsdk-ewcum-6c93cecc8e.json") #(키 이름 ) 부분에 본인의 키이름을 적어주세요.
default_app = firebase_admin.initialize_app(cred,{ 'databaseURL' : 'https://graphtest-2c3b1-default-rtdb.firebaseio.com/'})

arduino = serial.Serial('COM3', 9600)
count = 0




while True:

    print("In measurement...")
    count = 0

    while True:
        y = arduino.readline()
        result = (y.decode())[:-2]
        count = count+1
        if count==1:
            print(result)
            break

    h = result[2:4]
    t = result[6:8]
    b = result[10:12]
    c = result[14:]

    print(h)
    print(t)
    print(b)
    print(c)
    ref = db.reference(str(now))
    ref.update({"humidity":h})
    ref.update({"temperature":t})
    ref.update({"heartRate":b})
    ref.update({"bodyTemperature":c})

    print("measurement finish")
