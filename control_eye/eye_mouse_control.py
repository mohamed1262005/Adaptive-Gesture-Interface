import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import winsound
import json
import os
import time
from collections import deque


class EyeController:
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self.running = False

        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8
        )

        self.cap = None
        self.screen_w, self.screen_h = pyautogui.size()
        pyautogui.FAILSAFE = False

        self.smooth_x = self.screen_w // 2
        self.smooth_y = self.screen_h // 2
        self.alpha = 0.18

        self.calibration_data = {
            "left": 0.4,
            "right": 0.6,
            "top": 0.4,
            "bottom": 0.6
        }

        self.deadzone_px = 8
        self.buffer = deque(maxlen=8)

    # =========================
    # START
    # =========================
    def start(self):
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.run()

    # =========================
    # STOP
    # =========================
    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    # =========================
    # CORE LOOP
    # =========================
    def run(self):
        while self.running and self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb)

            if results.multi_face_landmarks:
                lm = results.multi_face_landmarks[0].landmark
                nose = lm[4]

                self.move_mouse(nose)

                if self.is_blink(lm):
                    pyautogui.click()

            # cv2.imshow("Eye Control", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                self.stop()

    # =========================
    # MOVE MOUSE
    # =========================
    def move_mouse(self, nose):
        cx = self.calibration_data["left"]
        rx = self.calibration_data["right"]
        ty = self.calibration_data["top"]
        by = self.calibration_data["bottom"]

        nx = np.clip((nose.x - cx) / (rx - cx), 0, 1)
        ny = np.clip((nose.y - ty) / (by - ty), 0, 1)

        tx = nx * self.screen_w
        ty = ny * self.screen_h

        self.smooth_x = self.alpha * tx + (1 - self.alpha) * self.smooth_x
        self.smooth_y = self.alpha * ty + (1 - self.alpha) * self.smooth_y

        pyautogui.moveTo(int(self.smooth_x), int(self.smooth_y), _pause=False)

    # =========================
    # BLINK DETECTION (بسيط)
    # =========================
    def is_blink(self, lm):
        left = abs(lm[145].y - lm[159].y)
        right = abs(lm[374].y - lm[386].y)

        if left < 0.018 and right > 0.018:
            return True
        return False