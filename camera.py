import cv2
import mediapipe as mp

# Set up media pipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Squat variables
rep_count = 0
squatting = False
squat_feedback = ""

# Open camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read() # Capture frame by frame
    if not ret:
        break

    # Convert BGR frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame for pose detection
    result = pose.process(rgb_frame)

    # Draw pose landmarks
    if result.pose_landmarks:
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Measure squat depth
        hip_y = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y
        knee_y = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y
        ankle_y = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y


        # Higher Y Values are lower in the image
        squat_feedback = f"Reps: {rep_count}"
        if abs(hip_y - knee_y) < 0.05: 
            if not squatting:
                squatting = True # User in down phase
            squat_feedback += " - Good depth!"
        else:
            if squatting and abs(hip_y - knee_y) > 0.2:
                rep_count += 1
                squatting = False # Reset to up phase
            squat_feedback += " - Squat!!!!"


        # # Measure torso angle
        # shoulder_y = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
        # hip_y = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y
        # torso_length = abs(shoulder_y - hip_y)

        # knee_y = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y
        # leg_length = abs(hip_y - knee_y)

        # if torso_length / leg_length < 0.5:
        #     print("Fix Posture")

        # Text overlay with metrics
        cv2.putText(frame, squat_feedback, (50, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, (0, 0, 255), 2, cv2.LINE_AA)


    cv2.imshow('Squat Counter', frame) # Show Frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()