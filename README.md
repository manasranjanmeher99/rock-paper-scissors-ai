# ✊✋✌️ Rock Paper Scissors AI using Computer Vision

A real-time **Rock Paper Scissors** game built using **Python**, **OpenCV**, and **MediaPipe**. The game detects the player's hand gesture through a webcam, classifies it as Rock, Paper, or Scissors, and competes against an AI opponent.

---

## 📌 Features

- 🎥 Real-time webcam hand tracking
- ✋ Hand landmark detection using MediaPipe
- 🤖 AI opponent
- 🎮 Rock, Paper, and Scissors gesture recognition
- ⚡ Fast gesture prediction
- 📊 Modular project structure
- 🖥️ Easy to extend with animations, scoreboard, countdown, and GUI

---

## 📂 Project Structure

```
rock-paper-scissors-ai/
│
├── ai_opponent.py          # AI logic for computer move
├── game.py                 # Main game controller
├── gesture_recognizer.py   # Detects Rock, Paper & Scissors
├── hand_tracker.py         # MediaPipe hand tracking
├── requirements.txt        # Project dependencies
└── README.md
```

---

## 🛠️ Technologies Used

- Python 3.x
- OpenCV
- MediaPipe
- NumPy

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/manasranjanmeher99/rock-paper-scissors-ai.git
```

### 2️⃣ Navigate to the Project

```bash
cd rock-paper-scissors-ai
```

### 3️⃣ Create a Virtual Environment (Optional)

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

```bash
python game.py
```

---

## 🧠 How It Works

1. OpenCV captures video from the webcam.
2. MediaPipe detects the hand and extracts 21 landmarks.
3. The gesture recognition module classifies the hand as:
   - ✊ Rock
   - ✋ Paper
   - ✌️ Scissors
4. The AI opponent selects its move.
5. The game compares both moves and declares the winner.

---

## 📁 Modules

### `hand_tracker.py`

- Detects hands
- Extracts landmarks
- Tracks finger positions

### `gesture_recognizer.py`

- Recognizes Rock
- Recognizes Paper
- Recognizes Scissors

### `ai_opponent.py`

- Generates the computer's move
- Can be extended with smarter AI strategies

### `game.py`

- Runs the main game loop
- Captures webcam frames
- Displays the game
- Determines the winner

---

## 🚀 Future Improvements

- ✅ Animated countdown
- ✅ Scoreboard
- ✅ Sound effects
- ✅ Difficulty levels
- ✅ Gesture confidence score
- ✅ Better AI prediction
- ✅ Computer hand animations
- ✅ Game history
- ✅ GUI using Tkinter or Streamlit

---

## 📸 Demo

### Webcam Detection

> Add a screenshot here

```
images/webcam_demo.png
```

### Gesture Recognition

> Add a screenshot here

```
images/gesture_demo.png
```

### Gameplay

> Add a screenshot here

```
images/gameplay.png
```

---

## 📋 Requirements

```
opencv-python
mediapipe
numpy
```

Or install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

---

## 👨‍💻 Author

**Manas Ranjan Meher**


- 💻 Aspiring Software Engineer
- 🤖 AI & Computer Vision Enthusiast

- GitHub:
https://github.com/manasranjanmeher99
- Linkedin:
https://www.linkedin.com/in/manas-ranjan-meher-606181280/
---
