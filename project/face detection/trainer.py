import os  #read and write file
import cv2  #open camera
import numpy as np  #array
from PIL import Image  #image file read and write

recognizer = cv2.face.LBPHFaceRecognizer_create()  #it recognizes the face in the camera
detector = cv2.CascadeClassifier("haarcascade_frontalface_default (1).xml")
path = "dataset"


def get_images_with_id(path):
    images_paths = [os.path.join(path, f) for f in os.listdir(path)]  #set images path to the os
    faces = []
    ids = []
    for single_image_path in images_paths:
        faceImg = Image.open(single_image_path).convert('L')  #image converted into black and white images L=luminence
        faceNp = np.array(faceImg, np.uint8)
        id = int(os.path.split(single_image_path)[-1].split(".")[1])
        faces.append(faceNp)
        ids.append(id)
        cv2.imshow("training", faceNp)
        cv2.waitKey(10)

    return np.array(ids), faces


ids, faces = get_images_with_id(path)
recognizer.train(faces,ids)
recognizer.save("recognizer/trainingdata.yml")
cv2.destroyAllWindows()
