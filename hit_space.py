import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import keyboard

# Initialize the webcam
cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=0.8, maxHands=2)  # Allow detecting both hands

# State variables to track the current gesture states
left_hand_one_finger_raised = False
right_hand_open = False

while True:
    # Get the frame from the webcam
    success, img = cap.read()
    if not success:
        break

    # Detect hands
    hands, img = detector.findHands(img)

    # Initialize gesture status
    gesture_status = "No hand detected"

    if hands:
        for hand in hands:
            handType = hand["type"]  # 'Left' or 'Right'
            fingers = detector.fingersUp(hand)

            if handType == "Left":
                # Check if only the index finger is raised
                if fingers == [1, 1, 1, 1, 1]:  # Index finger raised
                    if not left_hand_one_finger_raised:
                        keyboard.press_and_release('f8')
                        gesture_status = "Left hand - One finger raised - F8 pressed and released"
                        left_hand_one_finger_raised = True
                else:  # No fingers or multiple fingers raised
                    left_hand_one_finger_raised = False

            if handType == "Right":
                # Check if the hand is open
                if fingers == [1, 1, 1, 1, 1]:  # Open hand
                    if not right_hand_open:
                        keyboard.press_and_release('space')
                        gesture_status = "Right hand - Hand open - Space pressed and released"
                        right_hand_open = True
                else:  # Hand is closed or other gesture
                    right_hand_open = False

    # Display gesture status on the frame
    cv2.putText(img, gesture_status, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Hand Gesture Control", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
