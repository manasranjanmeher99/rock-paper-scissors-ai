"""
hand_tracker.py
Wraps MediaPipe Hands to detect and track a single hand and its 21 landmarks.
"""
import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.6):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles
        self.results = None

    def find_hands(self, frame_bgr, draw=True):
        """Process a BGR frame, optionally draw landmarks, return the frame."""
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        self.results = self.hands.process(frame_rgb)
        frame_rgb.flags.writeable = True

        if draw and self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame_bgr,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_styles.get_default_hand_landmarks_style(),
                    self.mp_styles.get_default_hand_connections_style(),
                )
        return frame_bgr

    def get_landmark_list(self, frame_shape):
        """
        Returns a list of (id, x_px, y_px) for the first detected hand,
        or an empty list if no hand is found.
        """
        landmark_list = []
        if self.results and self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            h, w = frame_shape[:2]
            for idx, lm in enumerate(hand.landmark):
                landmark_list.append((idx, int(lm.x * w), int(lm.y * h)))
        return landmark_list

    def get_handedness(self):
        """Returns 'Left' or 'Right' for the first detected hand, or None."""
        if self.results and self.results.multi_handedness:
            return self.results.multi_handedness[0].classification[0].label
        return None

    def has_hand(self):
        return bool(self.results and self.results.multi_hand_landmarks)

    def close(self):
        self.hands.close()
