
# 🖱️ Virtual Mouse using Hand Gestures

Control your computer mouse using just your hand gestures! This project uses **OpenCV**, **MediaPipe**, and **AutoPy** to detect hand landmarks in real-time and simulate mouse movement and clicks.

---

## 📸 Demo

> Hand tracking controls the mouse pointer and supports left click, right click, and even pressing keys like `Esc`.  

---

## 🚀 Features

- 🖐️ Track hand landmarks using **MediaPipe**
- 🖱️ Move mouse cursor using **index finger**
- 👆 Click with **index + middle finger pinch**
- 🤜 Right-click with **thumb + index pinch**
- ✋ Press `Esc` key when all fingers (except thumb) are up
- 👍 Exit the program when **only thumb** is up
- 🖥️ Smooth movement using interpolation

---

## 📦 Requirements

Install dependencies via pip:

```bash
pip install opencv-python mediapipe autopy numpy
```

---

## 📁 Project Structure

```
.
├── config.py             # Configuration constants (e.g., frame size, margins)
├── gesture_detection.py  # Hand gesture recognition logic using MediaPipe
├── main.py               # Main script to run the virtual mouse
├── mouse_actions.py      # Mouse action implementations (move, click, exit)
├── requirements.txt      # Required Python packages
└── Readme.md             # Project documentation          
```

---

## ⚙️ How It Works

1. OpenCV captures video frames from your webcam.
2. MediaPipe detects hand landmarks in real-time.
3. Mouse cursor movement is controlled based on the **index finger tip**.
4. Custom logic interprets gestures like:
    - **Index up**: Move cursor
    - **Index + Middle pinch**: Left click
    - **Thumb + Index pinch**: Right click
    - **All fingers up (except thumb)**: Press `Esc`
    - **Only thumb up**: Exit program

---

## 🎮 Gesture Controls

| Gesture                        | Action             |
|-------------------------------|--------------------|
| ☝️ Index finger only           | Move cursor        |
| ✌️ Index + middle finger       | Left click         |
| 🤏 Thumb + index finger pinch  | Right click        |
| ✋ All fingers except thumb     | Press `Esc` key    |
| 👍 Thumb only                  | Exit the program   |

---

## 🔧 Configuration

Inside `main.py`, you can tweak the following parameters:

```python
width = 640       # Camera width
height = 480      # Camera height
frameR = 100      # Movement frame boundary
smoothening = 8   # Cursor movement smoothening
```

---
## How to Run
    python main.py

## 💡 Notes

- Make sure your camera is working properly.
- The hand should be clearly visible against a plain background for best results.
- Works best under good lighting.

---

