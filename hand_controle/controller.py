import pyautogui

class Controller:
    def __init__(self):
        # المتغيرات دي بقت تابعة للكائن (Instance Variables)
        self.prev_hand = None
        self.right_clicked = False
        self.left_clicked = False
        self.double_clicked = False

        self.hand_Landmarks = None 

        self.little_finger_down = None
        self.little_finger_up = None
        self.index_finger_down = None
        self.index_finger_up = None
        self.middle_finger_down = None
        self.middle_finger_up = None
        self.ring_finger_down = None
        self.ring_finger_up = None

        self.Thump_finger_down = None 
        self.Thump_finger_up = None

        self.all_fingers_down = None
        self.all_fingers_up = None

        self.index_finger_within_Thumb_finger = None
        self.middle_finger_within_Thumb_finger = None
        self.little_finger_within_Thumb_finger = None
        self.ring_finger_within_Thumb_finger = None

        self.screen_width, self.screen_height = pyautogui.size()

    # =========================
    def update_fingers_status(self):
        if self.hand_Landmarks is None:
            return
        
        lm = self.hand_Landmarks.landmark

        self.little_finger_down = lm[20].y > lm[17].y
        self.little_finger_up = lm[20].y < lm[17].y

        self.index_finger_down = lm[8].y > lm[5].y
        self.index_finger_up = lm[8].y < lm[5].y

        self.middle_finger_down = lm[12].y > lm[9].y
        self.middle_finger_up = lm[12].y < lm[9].y

        self.ring_finger_down = lm[16].y > lm[13].y
        self.ring_finger_up = lm[16].y < lm[13].y

        self.Thump_finger_down = lm[4].y > lm[13].y
        self.Thump_finger_up = lm[4].y < lm[13].y

        self.all_fingers_down = (
            self.index_finger_down and
            self.middle_finger_down and
            self.ring_finger_down and
            self.little_finger_down
        )

        self.all_fingers_up = (
            self.index_finger_up and
            self.middle_finger_up and
            self.ring_finger_up and
            self.little_finger_up
        )

        self.index_finger_within_Thumb_finger = lm[8].y > lm[4].y and lm[8].y < lm[2].y
        self.middle_finger_within_Thumb_finger = lm[12].y > lm[4].y and lm[12].y < lm[2].y
        self.little_finger_within_Thumb_finger = lm[20].y > lm[4].y and lm[20].y < lm[2].y
        self.ring_finger_within_Thumb_finger = lm[16].y > lm[4].y and lm[16].y < lm[2].y

    # =========================
    def get_position(self, hand_x, hand_y):
        old_x, old_y = pyautogui.position()

        current_x = int(hand_x * self.screen_width)
        current_y = int(hand_y * self.screen_height)

        if self.prev_hand is None:
            self.prev_hand = (current_x, current_y)

        delta_x = current_x - self.prev_hand[0]
        delta_y = current_y - self.prev_hand[1]

        self.prev_hand = [current_x, current_y]

        current_x = old_x + delta_x
        current_y = old_y + delta_y

        threshold = 5
        current_x = max(threshold, min(current_x, self.screen_width - threshold))
        current_y = max(threshold, min(current_y, self.screen_height - threshold))

        return current_x, current_y

    # =========================
    def cursor_moving(self):
        if self.hand_Landmarks is None:
            return
            
        point = 9
        x = self.hand_Landmarks.landmark[point].x
        y = self.hand_Landmarks.landmark[point].y

        x, y = self.get_position(x, y)

        cursor_freezed = self.all_fingers_up and self.Thump_finger_down

        if not cursor_freezed:
            pyautogui.moveTo(x, y, duration=0)

    # =========================
    def detect_scrolling(self):
        if self.hand_Landmarks is None:
            return
            
        if self.little_finger_up and self.index_finger_down and self.middle_finger_down and self.ring_finger_down:
            pyautogui.scroll(120)
            print("Scrolling UP")

        if self.index_finger_up and self.middle_finger_down and self.ring_finger_down and self.little_finger_down:
            pyautogui.scroll(-120)
            print("Scrolling DOWN")

    # =========================
    def detect_zoomming(self):
        if self.hand_Landmarks is None:
            return
            
        zoom_pose = self.index_finger_up and self.middle_finger_up and self.ring_finger_down and self.little_finger_down

        window = 0.05
        lm = self.hand_Landmarks.landmark

        index_touches_middle = abs(lm[8].x - lm[12].x) <= window

        if zoom_pose and index_touches_middle:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(-50)
            pyautogui.keyUp('ctrl')
            print("Zoom Out")

        if zoom_pose and not index_touches_middle:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(50)
            pyautogui.keyUp('ctrl')
            print("Zoom In")

    # =========================
    def detect_clicking(self):
        if self.hand_Landmarks is None:
            return
            
        lm = self.hand_Landmarks.landmark

        left_click = (
            self.index_finger_within_Thumb_finger and
            self.middle_finger_up and
            self.ring_finger_up and
            self.little_finger_up
        )

        if not self.left_clicked and left_click:
            pyautogui.click()
            self.left_clicked = True
            print("Left Click")
        elif not self.index_finger_within_Thumb_finger:
            self.left_clicked = False

        right_click = (
            self.middle_finger_within_Thumb_finger and
            self.index_finger_up and
            self.ring_finger_up and
            self.little_finger_up
        )

        if not self.right_clicked and right_click:
            pyautogui.rightClick()
            self.right_clicked = True
            print("Right Click")
        elif not self.middle_finger_within_Thumb_finger:
            self.right_clicked = False

        double_click = (
            self.ring_finger_within_Thumb_finger and
            self.index_finger_up and
            self.middle_finger_up and
            self.little_finger_up
        )

        if not self.double_clicked and double_click:
            pyautogui.doubleClick()
            self.double_clicked = True
            print("Double Click")
        elif not self.ring_finger_within_Thumb_finger:
            self.double_clicked = False