from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import time
import dlib
import cv2

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Parametrii clipirii
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3

# Contoare
COUNTER = 0
TOTAL = 0

# Încarcă predictorul și modelul de recunoaștere (cu num_jitters=0 pentru viteză)
predictor_path = "shape_predictor_68_face_landmarks.dat"
facerec_path = "dlib_face_recognition_resnet_model_v1.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(facerec_path)

# Indici ochi
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Encoding fața cunoscută (cu num_jitters=0)
known_image = cv2.imread("my_face.jpeg")
known_gray = cv2.cvtColor(known_image, cv2.COLOR_BGR2GRAY)
known_rgb = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)
known_rects = detector(known_gray, 0)
if len(known_rects) > 0:
    known_shape = predictor(known_gray, known_rects[0])
    known_encoding = facerec.compute_face_descriptor(known_rgb, known_shape, 0)
else:
    raise ValueError("Nu s-a detectat nicio față în my_face.jpeg.")

# Pornește webcam-ul
vs = VideoStream(src=0).start()
time.sleep(1.0)

frame_skip = 0  # Pentru procesare la fiecare 2 frame-uri
last_recognition = "Necunoscut"  # Ultimul rezultat pentru frame-urile sărite

while True:
    frame = vs.read()
    frame = cv2.resize(frame, (450, int(frame.shape[0] * 450 / frame.shape[1])))  # Rezoluție mai mică pentru viteză
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    rects = detector(gray, 0)
    
    frame_skip += 1
    do_encoding = (frame_skip % 2 == 0)  # Calculează encoding la fiecare 2 frame-uri
    
    for rect in rects:
        shape = predictor(gray, rect)
        
        # Calculează EAR pentru blink (sempre, e rapid)
        shape_np = face_utils.shape_to_np(shape)
        leftEye = shape_np[lStart:lEnd]
        rightEye = shape_np[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        
        # Blink detection (rămâne la fel)
        if ear < EYE_AR_THRESH:
            COUNTER += 1
        else:
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                TOTAL += 1
            COUNTER = 0
        
        # Recunoaștere facială (doar dacă facem encoding în acest frame)
        if do_encoding:
            face_encoding = facerec.compute_face_descriptor(rgb_frame, shape, 0)  # num_jitters=0
            face_distance = np.linalg.norm(np.array(face_encoding) - np.array(known_encoding))
            tolerance = 0.6
            if face_distance < tolerance:
                last_recognition = "Carmen"
                color = (0, 255, 0)
            else:
                last_recognition = "Necunoscut"
                color = (0, 0, 255)
        else:
        
            color = (0, 255, 0) if last_recognition == "Carmen" else (0, 0, 255)
        
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        
        top = rect.top()
        right = rect.right()
        bottom = rect.bottom()
        left = rect.left()
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, last_recognition, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    

    cv2.putText(frame, f"Blinks: {TOTAL}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    cv2.imshow("Hakuna Matata", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

vs.stop()
cv2.destroyAllWindows()
