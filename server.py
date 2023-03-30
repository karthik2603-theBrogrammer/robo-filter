import socket
import cv2
import pickle
import numpy as np
import struct 


# Haarcascade from opencv (its Inbuilt ig)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

HOST=''
PORT=8485

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind((HOST,PORT))
print('Your Make A Robot Face Application is now ready!')
s.listen(10)
print('Robot now Listening for Client....')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # Converting the frames to grayscale increases the processing way more -->  Other forms are - Heat and normal. 
    # Grayscale is faster because RGB(3 possible from 0,255) but grayscale is only 0,255 - ie only 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        # roi in CV is called Region of Interest
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5)
        
        for (ex, ey, ew, eh) in eyes:
            correlation_percentage = round((ew/w) * 100, 2)
            if correlation_percentage >= 20:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
                correlation_percentage = round((ew / w) * 100, 2)
                text = f"Eyesss"
                cv2.putText(roi_color, text, (ex, ey-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=20)

        # Draw a rectangle around each detected smile within the face region
        # for (sx, sy, sw, sh) in smiles:
        #     cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 255, 0), 2)
        #     correlation_percentage = round((sw / w) * 100, 2)
        #     text = f"Say Cheeeseeeeese: {correlation_percentage }%"
        #     cv2.putText(roi_color, text, (sx, sy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        for (sx, sy, sw, sh) in smiles:
            correlation_percentage = round((sw / w) * 100, 2)
            if correlation_percentage >= 30:
                cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 255, 0), 2)
                text = f"Smile: {correlation_percentage}%"
                cv2.putText(roi_color, text, (sx, sy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)
                text = f"Not a smile: {correlation_percentage}%"
                cv2.putText(roi_color, text, (sx, sy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)


        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            text = f"You Cant See Me!"
            cv2.putText(roi_color, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            
    cv2.imshow('Pose As A Robot!',frame)
    cv2.waitKey(1)
