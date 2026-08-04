"""
game.py
Main game loop: webcam capture, hand tracking, 3-2-1 countdown, gesture
capture on "Show!", an animated computer-move reveal, scoring, and UI.

Controls:
  SPACE - start a round / play the next round
  q     - quit
  r     - reset scores
"""

import time
import cv2

from hand_tracker import HandTracker
from gesture_recognizer import classify_gesture
from ai_opponent import AIOpponent, decide_winner, MOVES

WINDOW_NAME = "AI Rock Paper Scissors"
COUNTDOWN_SECONDS = 3
ANIM_DURATION = 0.9          # seconds spent "shaking" through moves before reveal
ANIM_FRAME_SECONDS = 0.12    # speed of that shake animation

STATE_IDLE = "IDLE"
STATE_COUNTDOWN = "COUNTDOWN"
STATE_ANIMATE = "ANIMATE"
STATE_RESULT = "RESULT"


def draw_text(frame, text, pos, scale=1.0, color=(255, 255, 255), thickness=2, center=False):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if center:
        (tw, th), _ = cv2.getTextSize(text, font, scale, thickness)
        pos = (pos[0] - tw // 2, pos[1] + th // 2)
    # dark outline for readability over the video feed
    cv2.putText(frame, text, pos, font, scale, (0, 0, 0), thickness + 3, cv2.LINE_AA)
    cv2.putText(frame, text, pos, font, scale, color, thickness, cv2.LINE_AA)


def draw_panel(frame, x1, y1, x2, y2, alpha=0.45):
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (20, 20, 20), -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Could not open webcam. Check your camera connection/permissions.")
        return

    tracker = HandTracker(max_hands=1)
    ai = AIOpponent(warmup_rounds=3)

    player_score = 0
    computer_score = 0
    ties = 0

    state = STATE_IDLE
    countdown_start = None
    captured_gesture = None
    computer_move = None
    result_text = ""
    anim_start = None
    result_start = None

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Lost connection to webcam.")
            break

        frame = cv2.flip(frame, 1)  # mirror for a natural "selfie" view
        frame = tracker.find_hands(frame, draw=True)
        landmarks = tracker.get_landmark_list(frame.shape)
        handedness = tracker.get_handedness() or "Right"
        live_gesture = classify_gesture(landmarks, handedness) if landmarks else None

        h, w = frame.shape[:2]

        # --- Top score bar ---
        draw_panel(frame, 0, 0, w, 70)
        draw_text(frame, f"You: {player_score}", (20, 45), 1.0, (0, 220, 0))
        draw_text(frame, f"Ties: {ties}", (w // 2, 45), 0.9, (200, 200, 200), center=True)
        draw_text(frame, f"AI: {computer_score}", (w - 160, 45), 1.0, (0, 120, 255))

        # --- Live gesture readout ---
        if live_gesture:
            draw_text(frame, f"Detected: {live_gesture}", (20, h - 20), 0.8, (255, 255, 0))

        # --- State machine ---
        if state == STATE_IDLE:
            draw_text(frame, "Press SPACE to play a round", (w // 2, h // 2 - 40), 1.1, (255, 255, 255), center=True)
            draw_text(frame, "q: quit   r: reset score", (w // 2, h // 2 + 10), 0.7, (180, 180, 180), center=True)

        elif state == STATE_COUNTDOWN:
            elapsed = time.time() - countdown_start
            remaining = COUNTDOWN_SECONDS - elapsed
            if remaining > 0:
                label = str(int(remaining) + 1)
                draw_text(frame, label, (w // 2, h // 2), 4.0, (0, 255, 255), 6, center=True)
                draw_text(frame, "Get ready...", (w // 2, h // 2 + 90), 1.0, (255, 255, 255), center=True)
            else:
                draw_text(frame, "SHOW!", (w // 2, h // 2), 3.0, (0, 0, 255), 6, center=True)
                captured_gesture = live_gesture  # lock in the gesture at this instant
                state = STATE_ANIMATE
                anim_start = time.time()

        elif state == STATE_ANIMATE:
            elapsed = time.time() - anim_start
            frame_idx = int(elapsed / ANIM_FRAME_SECONDS)

            if elapsed < ANIM_DURATION:
                shown = MOVES[frame_idx % len(MOVES)]
                draw_text(frame, "AI choosing" + "." * (frame_idx % 4), (w // 2, h // 2 - 60), 0.9, (200, 200, 200), center=True)
                draw_text(frame, shown, (w // 2, h // 2 + 20), 2.2, (0, 165, 255), 5, center=True)
            else:
                if captured_gesture is None:
                    result_text = "No hand detected - try again!"
                    computer_move = None
                else:
                    computer_move = ai.choose_move()
                    winner = decide_winner(captured_gesture, computer_move)
                    ai.record(captured_gesture)

                    if winner == "Player":
                        player_score += 1
                        result_text = "You win this round!"
                    elif winner == "Computer":
                        computer_score += 1
                        result_text = "AI wins this round!"
                    else:
                        ties += 1
                        result_text = "It's a tie!"

                state = STATE_RESULT
                result_start = time.time()

        elif state == STATE_RESULT:
            draw_panel(frame, 0, h // 2 - 110, w, h // 2 + 110, alpha=0.55)
            if captured_gesture:
                draw_text(frame, f"You: {captured_gesture}", (w // 2, h // 2 - 60), 1.2, (0, 220, 0), center=True)
            if computer_move:
                draw_text(frame, f"AI: {computer_move}", (w // 2, h // 2 - 10), 1.2, (0, 120, 255), center=True)
            draw_text(frame, result_text, (w // 2, h // 2 + 50), 1.0, (255, 255, 255), center=True)
            draw_text(frame, "Press SPACE for next round", (w // 2, h // 2 + 95), 0.7, (180, 180, 180), center=True)

        cv2.imshow(WINDOW_NAME, frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('r'):
            player_score = computer_score = ties = 0
        elif key == ord(' '):
            if state in (STATE_IDLE, STATE_RESULT):
                state = STATE_COUNTDOWN
                countdown_start = time.time()
                captured_gesture = None
                computer_move = None
                result_text = ""

    tracker.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
