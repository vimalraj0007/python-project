import cv2     # OpenCV for camera access
import numpy as np   # Numpy array handling
import sqlite3  # SQLite database for storing user data
import os  # For creating directories

# Load the pre-trained Haar Cascade for face detection
facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default (1).xml')
cam = cv2.VideoCapture(0)  # 0 is for the default webcam

# Ensure that the 'dataset' folder exists
if not os.path.exists('dataset'):
    os.makedirs('dataset')

def insertorupdate(Id, Name, age):
    """Function to insert or update user data in the SQLite database."""
    conn = sqlite3.connect("sqlite.db")  # Connect to the SQLite database
    cursor = conn.cursor()

    # Create the STUDENTS table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS STUDENTS (
        Id INTEGER PRIMARY KEY,
        Name TEXT,
        age INTEGER
    )
    ''')
    conn.commit()

    # Check if the record exists
    cursor.execute("SELECT * FROM STUDENTS WHERE Id=?", (Id,))
    isRecordExist = cursor.fetchone()  # Fetch the first result (or None if no result)

    if isRecordExist:  # If record exists, update it
        cursor.execute("UPDATE STUDENTS SET Name=? WHERE Id=?", (Name, Id))
        cursor.execute("UPDATE STUDENTS SET age=? WHERE Id=?", (age, Id))
    else:  # If no record exists, insert a new record
        cursor.execute("INSERT INTO STUDENTS (Id, Name, age) VALUES (?, ?, ?)", (Id, Name, age))

    conn.commit()  # Commit changes to the database
    conn.close()   # Close the connection

# Input user details
Id = input('Enter User Id: ')
Name = input('Enter User Name: ')
age = int(input('Enter User Age: '))  # Convert age input to an integer

# Insert or update the user data in the database
insertorupdate(Id, Name, age)

# Start capturing faces from the webcam
sampleNum = 0  # Counter for the number of samples captured
while True:
    ret, img = cam.read()  # Capture an image from the webcam
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale
    faces = facedetect.detectMultiScale(gray, 1.3, 5)  # Detect faces in the image

    for (x, y, w, h) in faces:
        sampleNum += 1  # Increment the sample count
        # Save the face sample as a grayscale image
        cv2.imwrite(f"dataset/user.{Id}.{sampleNum}.jpg", gray[y:y+h, x:x+w])
        # Draw a rectangle around the detected face
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.waitKey(100)  # Delay to avoid too fast capturing

    # Display the frame with detected faces
    cv2.imshow("Face", img)
    cv2.waitKey(1)  # Wait for a key press for 1 ms

    if sampleNum >= 20:  # Stop after capturing 20 samples
        break

# Release the webcam and close the OpenCV windows
cam.release()
cv2.destroyAllWindows()
