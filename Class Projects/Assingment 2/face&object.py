import cv2
import os
import numpy as np
from ultralytics import YOLO
model = YOLO('yolov8n.pt')

haar_file='haarcascade_frontalface_default.xml'
datasets='C:/Users/acer/PycharmProjects/facedetect/dataset/'
(images,labels,names,id)=([],[],{},0)
for(subdir,dirs,files) in os.walk(datasets):
    for subdir in dirs:
        names[id]=subdir
        subjectpath=os.path.join(datasets,subdir)
        for filename in os.listdir(subjectpath):
            path = os.path.join(subjectpath, filename)
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1

    (width, height) = (640, 480)

    (images, labels) = [np.array(lists) for lists in [images, labels]]

    model1 = cv2.face.LBPHFaceRecognizer_create()
    model1.train(images, labels)

    face_cascade = cv2.CascadeClassifier(haar_file)
    cap = cv2.VideoCapture(0)

    print('Classifier trained!')
    print('Attempting to detecting faces...')

    while True:
        ret, frame = cap.read()
        if ret == True:
            img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(img_gray, 1.4, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                face = img_gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (width, height))
                prediction = model1.predict(face_resize)

                if prediction[1] < 74:
                    cv2.putText(frame, '%s' % (names[prediction[0]].strip()), (x + 5, (y + 25) + h),
                                cv2.FONT_HERSHEY_PLAIN, 1.5, (20, 185, 20), 2)
                else:
                    cv2.putText(frame, 'Unknown', (x + 5, (y + 25) + h), cv2.FONT_HERSHEY_PLAIN, 1.5, (65, 65, 255), 2)
                    print("Predicted person: Unknown")

            result = model.track(frame, persist=True)

            # plot results
            frame = result[0].plot()

            # visulaize
            # cv2.imshow('frame', frame_)
            cv2.imshow('frame', frame)
            # cv2.imshow('OpenCV Face Recognition', frame)
            if cv2.waitKey(1)==ord("q"):
                break
cap.release()
cv2.destroyAllWindows()