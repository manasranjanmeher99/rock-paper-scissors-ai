"""
gesture_recognizer.py
Classifies a hand landmark list into "Rock", "Paper", "Scissors", or None.

MediaPipe landmark indices (21 total):
0: wrist
Thumb:  1(CMC) 2(MCP) 3(IP) 4(TIP)
Index:  5(MCP) 6(PIP) 7(DIP) 8(TIP)
Middle: 9(MCP) 10(PIP) 11(DIP) 12(TIP)
Ring:   13(MCP) 14(PIP) 15(DIP) 16(TIP)
Pinky:  17(MCP) 18(PIP) 19(DIP) 20(TIP)
"""

FINGER_TIPS = [4, 8, 12, 16, 20]
FINGER_PIPS = [3, 6, 10, 14, 18]  # joint two below each tip (used for the extension test)


def _fingers_up(landmarks, handedness_label="Right"):
    """
    Returns a list of 5 booleans [thumb, index, middle, ring, pinky]
    indicating whether each finger is extended.
    `landmarks` is a list of (id, x, y) in pixel coordinates (y grows downward).
    """
    if len(landmarks) < 21:
        return [False] * 5

    pts = {idx: (x, y) for idx, x, y in landmarks}
    fingers = []

    # Thumb: compare x of tip vs. ip/mcp joints. Direction flips with handedness
    # because the webcam feed is mirrored (selfie view).
    tip_x, _ = pts[4]
    ip_x, _ = pts[3]
    mcp_x, _ = pts[2]
    if handedness_label == "Right":
        thumb_up = tip_x < ip_x < mcp_x or tip_x < mcp_x
    else:
        thumb_up = tip_x > ip_x > mcp_x or tip_x > mcp_x
    fingers.append(thumb_up)

    # Other four fingers: extended if tip is above (smaller y) than its pip joint.
    for tip_id, pip_id in zip(FINGER_TIPS[1:], FINGER_PIPS[1:]):
        tip_y = pts[tip_id][1]
        pip_y = pts[pip_id][1]
        fingers.append(tip_y < pip_y)

    return fingers


def classify_gesture(landmarks, handedness_label="Right"):
    """
    Returns one of "Rock", "Paper", "Scissors", or None if the pose
    doesn't clearly match any of the three.
    """
    if not landmarks:
        return None

    thumb, index, middle, ring, pinky = _fingers_up(landmarks, handedness_label)
    up_count = sum([thumb, index, middle, ring, pinky])

    # Rock: closed fist (thumb may or may not tuck in, nothing else extended).
    if up_count <= 1 and not (index and middle):
        return "Rock"

    # Scissors: index + middle extended, ring + pinky folded.
    if index and middle and not ring and not pinky:
        return "Scissors"

    # Paper: all (or all but thumb) fingers extended.
    if index and middle and ring and pinky:
        return "Paper"

    return None
