import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

# Import drawing and hand detection modules from mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Create a keyboard controller object
kb = Controller()

class HandDetector:
    # Initialize the class by opening the camera and creating a hands object
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.hands = mp_hands.Hands(
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5)

    # Start the hand detection process
    def start(self):
        while self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # Convert the frame to RGB format
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the frame using the hands object
            results = self.hands.process(image)

            # Convert the frame back to BGR format
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # If hand landmarks are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y and hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y and hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y and hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y:
                        kb.press(Key.space)
                    else:
                        kb.release(Key.space)
                    
                    # Draw the hand landmarks on the frame
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

            # Show the processed frame
            cv2.imshow('Hand Controller', cv2.flip(image, 1))

            # Check if the 'Esc' key has been pressed
            if cv2.waitKey(5) & 0xFF == 27:
                break
    
    # Stop the hand detection process
    def stop(self):
        self.cap.release()



