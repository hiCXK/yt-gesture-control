import os
os.environ["DISPLAY"] = ":0"
os.environ['WAYLAND_DISPLAY'] = ''

os.environ["XDG_SESSION_TYPE"] = "xcb"

import cv2   
import mediapipe as mp
import pyautogui  ,time
# import keyboard        

# Initialize mediapipe hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)

# Function to count the number of fingers up
def count_fingers(landmarks):
    # Thumb
    thumb_is_open = landmarks[4].x < landmarks[3].x
    
    # Fingers
    finger_is_open = [
        landmarks[8].y < landmarks[6].y,  # Index finger
        landmarks[12].y < landmarks[10].y,  # Middle finger
        landmarks[16].y < landmarks[14].y,  # Ring finger
        landmarks[20].y < landmarks[18].y,  # Little finger
    ]
    
    return sum([thumb_is_open] + finger_is_open)  # Count the number of open fingers

# Variable to track if space was pressed
spacebar_pressed = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB (mediapipe requires RGB input)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame for hand detection
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Count how many fingers are up
            num_fingers_up = count_fingers(hand_landmarks.landmark)

            # Open palm (5 fingers up) is considered as the spacebar press gesture
            if num_fingers_up == 5:
                if not spacebar_pressed:  # Avoid multiple presses
                    # pyautogui.press('space')   # Simulate spacebar press
                    # time.sleep(2) 
                    spacebar_pressed  = True

            else:
                spacebar_pressed = False
            pyautogui.press('space')  
            print(spacebar_pressed)

    # Display the resulting frame
    cv2.imshow('YouTube Gesture Control', frame)

    # Break the loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
