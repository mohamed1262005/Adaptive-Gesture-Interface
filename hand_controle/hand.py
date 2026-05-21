import cv2
import mediapipe as mp

try:
    from .controller import Controller
except ImportError:
    from controller import Controller

cap = cv2.VideoCapture(0)

def run_loop(controller_instance): 
    hands = mp.solutions.hands.Hands(
        static_image_mode=False, 
        max_num_hands=1, 
        min_detection_confidence=0.7
    )
    mp_draw = mp.solutions.drawing_utils

    while True:
        success, img = cap.read()
        if not success:
            break
            
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            # تحديث البيانات للكائن
            controller_instance.hand_Landmarks = results.multi_hand_landmarks[0]

            # تنفيذ الأوامر من الكائن
            controller_instance.update_fingers_status()
            controller_instance.cursor_moving()
            controller_instance.detect_scrolling()
            controller_instance.detect_zoomming()
            controller_instance.detect_clicking()

            # رسم النقاط للتأكد
            mp_draw.draw_landmarks(img, results.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS)

        # cv2.imshow("Hand Tracker", img)

        if cv2.waitKey(5) & 0xFF == 27: 
            break
    
    cap.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    test_controller = Controller()
    # run_loop(test_controller)