# Adaptive Gesture Interface (AGI) 👁️🖐️

An AI-powered assistive system that enables completely hands-free computer control using eye tracking and hand gestures.

Built with **Python, OpenCV, and MediaPipe**, the project performs real-time gaze estimation and gesture recognition to control mouse movement, clicks, scrolling, and shortcuts without physical interaction.

Designed to improve accessibility and provide a futuristic human-computer interaction experience for individuals with mobility impairments.

---

## 🚀 Features

- **Eye-Controlled Cursor Movement**  
  Real-time gaze tracking for smooth and responsive mouse control.

- **Hand Gesture Recognition**  
  Detects hand gestures and maps them to mouse actions such as:
  - Left Click
  - Right Click
  - Scroll
  - Custom Shortcuts

- **Real-Time Performance**  
  Optimized frame processing for low-latency interaction.

- **Accessibility-Focused Design**  
  Provides a touchless interface for users with physical disabilities or limited mobility.

---

## 📂 Project Structure

- `control_eye/` → Eye tracking and gaze estimation modules.
- `hand_control/` → Hand tracking and gesture recognition logic.
- `icons/` → UI assets and interface icons.

---

## 💻 Tech Stack

- **Python 3**
- **OpenCV**
- **MediaPipe**
- **NumPy**
- **PyAutoGUI**

---

## ⚙️ Installation

```bash
git clone https://github.com/mohamed1262005/Adaptive-Gesture-Interface.git
cd Adaptive-Gesture-Interface
pip install -r requirements.txt
python main.py
