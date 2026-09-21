# 🤖 Jarvis AI Assistant & Hand Tracking Virtual Mouse

An intelligent Windows desktop application that combines a **hands-free AI voice assistant** with a **computer vision hand-tracking virtual mouse**. Control your PC using natural voice commands, precise hand gestures, or a seamless combination of both!

---

## ✨ Features

* 🎙️ **Jarvis Voice Assistant:** Open installed applications, folders, pictures, videos, and local files dynamically by name.
* 🔍 **Smart Knowledge & Web Search:** Ask questions, search Google, or receive instant offline knowledge base / Wikipedia summaries directly through speech.
* 🖐️ **Hand Tracking Virtual Mouse:** Control your cursor, left-click, right-click, double-click, scroll, and pinch-to-zoom using your webcam via MediaPipe.
* ⏸️ **Independent Pause & Resume:** Toggle hand tracking on or off anytime via voice commands, a global hotkey, or an on-screen button—while Jarvis remains online listening in the background.

---

## 🚀 Quick Download & Installation (Windows)

You do **not** need Python installed on your system to run this program.

1. Go to the **[Releases](../../releases)** section of this repository.
2. Download the latest setup executable (`Jarvis_AI_Mouse_Setup.exe`).
3. Double-click the installer and follow the setup wizard prompts.
4. Launch **Jarvis AI Mouse** directly from your Desktop or Start Menu.

---

## 🎯 Controls & Gestures Breakdown

### 🖐️ Hand Tracking Gestures

| Gesture | Action | Description |
| :--- | :--- | :--- |
| **Index Finger Point** | **Cursor Movement** | Move your index finger inside the red tracking bounding box to guide the mouse cursor smoothly across your screen. |
| **Thumb + Index Pinch** | **Left Click** | Bring your left hand's thumb and index finger tips close together to perform a standard left-click. |
| **Thumb + Pinky Pinch** | **Right Click** | Bring your left hand's thumb and pinky finger tips close together to perform a right-click. |
| **Closed Fist** | **Double Click** | Curl all fingertips close to your wrist to trigger a system double-click. |
| **Index + Middle Fingers Together** | **Vertical Scroll** | Keep your right hand's index and middle fingers together, then move your hand up or down to scroll through web pages or documents. |
| **Two-Handed Ring Pinch** | **Zoom Mode** | Pinch the thumb and ring finger on **both** hands simultaneously. Move your hands closer or further apart to zoom in/out (`Ctrl + Scroll`). |

---

### 🎙️ Voice Commands
Say **"Jarvis"** followed by your command into your microphone:

| Category | Command Examples |
| :--- | :--- |
| **Open Local Items** | *"Jarvis, open Chrome"* <br> *"Jarvis, open Downloads"* <br> *"Jarvis, open project folder"* |
| **Web & Info Search** | *"Jarvis, search about space exploration"* <br> *"Who is Iron Man?"* <br> *"What is thermodynamics?"* |
| **Pause Tracking** | *"Pause tracking"* or *"Jarvis pause"* |
| **Resume Tracking** | *"Resume tracking"* or *"Jarvis resume"* |

### ⌨️ Manual Shortcuts & Controls
* **`Ctrl + Shift + Space`**: Global hotkey to pause or resume hand tracking anywhere in Windows.
* **On-Screen Camera Button:** Click the top-left **PAUSE/RESUME** button box directly inside the OpenCV camera window.

---

## 🛠️ Building from Source (Developers)

If you wish to run or modify the Python source code directly:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Eyosias7/Jarvis-AI-Handtracking.git](https://github.com/Eyosias7/Jarvis-AI-Handtracking.git)
   cd Jarvis-AI-Handtracking
