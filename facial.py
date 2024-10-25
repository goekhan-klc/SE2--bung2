import threading
from skimage.measure import compare_ssim as ssim
import cv2
import img2pdf


# Global variables for sharing data between threads
faces = []

def captureFace(frame):
    for (x, y, w, h) in faces:
        # Crop and save the detected face
        face = frame[y:y+h, x:x+w]
        cv2.imwrite('reference_face.jpg', face)  # Save the reference face image
        break  # Only save the first detected face

def matchFace(frame):
    # Load the reference face
    reference_face = cv2.imread('reference_face.jpg', cv2.IMREAD_COLOR)

    for (x, y, w, h) in faces:
        # Crop the detected face for comparison
        current_face = frame[y:y+h, x:x+w]
        
        # Calculate the SSIM
        ssim_value = ssim(reference_face, current_face, multichannel=True)
        
        if ssim_value > 0.7:  # Adjust the threshold as needed
            cv2.putText(frame, 'Match', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Function to handle user input
def input_thread():
    while True:
        user_input = input("Command: <capture> <match> <x>")

        if user_input == "capture":
            captureFace(frame)  # Pass the current frame to the function
        elif user_input == "match":
            matchFace(frame)  # Pass the current frame to the function
        elif user_input == "x":
            break
        # Handle the input or perform actions as needed
        print(f"You entered: {user_input}")

def main():
    print("Start")

    # Create a separate thread for input
    input_thread_obj = threading.Thread(target=input_thread)
    input_thread_obj.start()

    global frame  # Make the 'frame' variable accessible to the matchFace and captureFace functions

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('FaceID', cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces[:] = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the camera feed with rectangles
        cv2.imshow('FaceID', frame)

        # Check for the 'x' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
