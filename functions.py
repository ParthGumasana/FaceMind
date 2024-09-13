from tensorflow.keras.models import load_model
import cv2

global face_cascade, model

model = load_model('ck+.h5')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def detect_face(img):
    res_labels = {0:'Anger',1:'contempt',2:'disgust',3:'fear',4:'happy',5:'sadness',6:'surprise'}
    face_img = img.copy()
    face_rects = face_cascade.detectMultiScale(face_img)
    if len(face_rects)>0:
        x,y,h,w = face_rects[0]
        face = img[y:y+h,x:x+w]
        face_resized = cv2.resize(face,(48,48))
        face_resized = face_resized.reshape(1,48,48,3)
        res = model.predict(face_resized)
        idx = res[0].argmax()
        for (x,y,h,w) in face_rects:
            cv2.rectangle(face_img,(x,y),(x+w,y+h),(255,255,255),10)
            text = res_labels[idx]
            cv2.putText(face_img,text,(x,y-5),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
        return face_img
    else:
        return face_img