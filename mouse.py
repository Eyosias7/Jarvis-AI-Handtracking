import cv2
import numpy as np
import pyautogui
import os
import glob
import urllib.request
import mediapipe as mp
import threading
import speech_recognition as sr
import win32com.client  
import webbrowser
import wikipedia  
import pythoncom  
import random  
import keyboard  # Requires: pip install keyboard
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ==========================================================
# GLOBAL STATE
# ==========================================================
is_paused = False

def toggle_pause_shortcut():
    global is_paused
    is_paused = not is_paused
    print(f"[System]: Tracking {'PAUSED' if is_paused else 'RESUMED'} via shortcut.")

# Register global hotkey: Ctrl + Shift + Space
keyboard.add_hotkey('ctrl+shift+space', toggle_pause_shortcut)

# ==========================================================
# JARVIS AI VOICE ASSISTANT (Background Thread)
# ==========================================================
def jarvis_listener():
    global is_paused
    pythoncom.CoInitialize() 

    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Rate = 1  
    
    def speak(text):
        print(f"[Jarvis]: {text}")
        speaker.Speak(text)

    def open_target_by_name(target_name):
        """Searches for apps, pictures, videos, and folders matching target_name across user directories."""
        target_name = target_name.lower().strip()
        user_home = os.path.expanduser("~")
        
        search_roots = [
            os.path.join(user_home, "Desktop"),
            os.path.join(user_home, "Downloads"),
            os.path.join(user_home, "Documents"),
            os.path.join(user_home, "Pictures"),
            os.path.join(user_home, "Videos"),
            os.path.join(user_home, "Music"),
            "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs",
            os.path.join(user_home, "AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs")
        ]
        
        found_path = None

        for root_dir in search_roots:
            if not os.path.exists(root_dir):
                continue
                
            for root, dirs, files in os.walk(root_dir):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() not in ['node_modules', 'appdata', 'venv', '__pycache__']]

                for d in dirs:
                    if target_name in d.lower():
                        found_path = os.path.join(root, d)
                        break
                if found_path:
                    break
                    
                for f in files:
                    if target_name in f.lower():
                        found_path = os.path.join(root, f)
                        break
                if found_path:
                    break
            
            if found_path:
                break

        if found_path:
            item_name = os.path.basename(found_path)
            speak(f"Right away. Opening {item_name}.")
            os.startfile(found_path)
        else:
            speak(f"Sorry, I couldn't find any file, picture, video, or folder named {target_name}.")

    knowledge_base = {
        "llm": "An LLM, or Large Language Model, is an AI trained on vast amounts of text to understand and generate human language.",
        "iron man": "Iron Man is Tony Stark, a genius billionaire who created a powered suit of armor. I am his AI system.",
        "thermodynamics": "Thermodynamics is the branch of physics that deals with heat, work, and temperature, and their relation to energy.",
        "tokamak": "A Tokamak is a device which uses a powerful magnetic field to confine plasma in the shape of a torus, primarily for nuclear fusion research.",
        "digital sat": "The Digital SAT is an adaptive computer-based test for college admissions focusing on Reading, Writing, and Math."
    }

    r = sr.Recognizer()
    r.pause_threshold = 1.5  
    r.energy_threshold = 300 
    r.dynamic_energy_threshold = True 

    speak("System online. Jarvis is ready. Hello there, how can I help you?")

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=2)
        
        while True:
            try:
                audio = r.listen(source)
                command = r.recognize_google(audio).lower()
                print(f"You said: {command}")
                
                if "thank you" in command or "thanks" in command:
                    replies = ["You're welcome!", "Anytime!", "Always a pleasure.", "At your service!"]
                    speak(random.choice(replies))

                # --- PAUSE / RESUME VOICE COMMANDS ---
                if "pause tracking" in command or "pause hand tracking" in command or "jarvis pause" in command:
                    is_paused = True
                    speak("Hand tracking paused.")
                
                elif "resume tracking" in command or "resume hand tracking" in command or "jarvis resume" in command:
                    is_paused = False
                    speak("Hand tracking resumed.")
                
                elif "jarvis" in command:
                    if "open youtube" in command:
                        speak("Right away. Opening YouTube.")
                        webbrowser.open("https://www.youtube.com")
                    
                    elif "open chrome" in command or "open google" in command:
                        speak("Opening browser.")
                        webbrowser.open("https://www.google.com")
                    
                    elif "open" in command:
                        target = command.split("open")[1].strip()
                        open_target_by_name(target)
                    
                    elif "search" in command or "what is" in command or "who is" in command:
                        if "search about" in command:
                            query = command.split("search about")[1].strip()
                        elif "search" in command:
                            query = command.split("search")[1].strip()
                        elif "what is" in command:
                            query = command.split("what is")[1].strip()
                        elif "who is" in command:
                            query = command.split("who is")[1].strip()
                        else:
                            query = command.replace("jarvis", "").strip()

                        speak(f"Searching for {query}")
                        webbrowser.open(f"https://www.google.com/search?q={query}")
                        
                        answered = False
                        for key, answer in knowledge_base.items():
                            if key in query:
                                speak(answer)
                                answered = True
                                break
                        
                        if not answered:
                            try:
                                wiki_answer = wikipedia.summary(query, sentences=1) 
                                speak(wiki_answer)
                            except wikipedia.exceptions.DisambiguationError:
                                speak("That could refer to a few different things. I've displayed the search results for you.")
                            except wikipedia.exceptions.PageError:
                                speak("I couldn't find a quick summary, but the web results are on your screen.")
                            except Exception:
                                speak(f"I have displayed the web results for {query} on your screen.")

            except sr.UnknownValueError:
                pass  
            except sr.RequestError:
                print("[Jarvis Error] Connection to Google Voice API failed.")
            except Exception as e:
                print(f"[Jarvis Error]: {e}")

jarvis_thread = threading.Thread(target=jarvis_listener, daemon=True)
jarvis_thread.start()

# ==========================================================
# OPENCV MOUSE CALLBACK FOR GUI BUTTON
# ==========================================================
def on_mouse_click(event, x, y, flags, param):
    global is_paused
    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if click is inside the top-left Pause/Resume button (x: 20-160, y: 20-60)
        if 20 <= x <= 160 and 20 <= y <= 60:
            is_paused = not is_paused
            print(f"[System]: Tracking {'PAUSED' if is_paused else 'RESUMED'} via button click.")

# ==========================================================
# HAND TRACKING MOUSE SYSTEM
# ==========================================================

model_path = 'hand_landmarker.task'
if not os.path.exists(model_path):
    print("Downloading hand tracking model...")
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    urllib.request.urlretrieve(url, model_path)

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
detector = vision.HandLandmarker.create_from_options(options)

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
screen_w, screen_h = pyautogui.size()
screen_aspect_ratio = screen_w / screen_h

cap = cv2.VideoCapture(0)

# Register OpenCV Window and Mouse Callback
cv2.namedWindow('Hand Tracking AI Mouse')
cv2.setMouseCallback('Hand Tracking AI Mouse', on_mouse_click)

prev_x, prev_y = 0, 0
smoothening = 2.5

is_left_clicked = False
is_right_clicked = False
is_double_clicked = False
prev_scroll_y = 0
prev_zoom_dist = 0

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # --- DRAW PAUSE / RESUME BUTTON ---
    btn_color = (0, 0, 255) if is_paused else (0, 255, 0)
    btn_text = "RESUME" if is_paused else "PAUSE"
    cv2.rectangle(frame, (20, 20), (160, 60), btn_color, -1)
    cv2.putText(frame, btn_text, (35, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # --- IF PAUSED: DISPLAY OVERLAY AND SKIP TRACKING ---
    if is_paused:
        cv2.putText(frame, "TRACKING PAUSED", (w // 2 - 160, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.putText(frame, "Press Ctrl+Shift+Space or say 'Resume'", (w // 2 - 200, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.imshow('Hand Tracking AI Mouse', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # --- BOUNDING BOX FOR MOUSE CONTROL ---
    box_w = int(w * 0.45) 
    box_h = int(box_w / screen_aspect_ratio)

    if box_h > h * 0.8:
        box_h = int(h * 0.8)
        box_w = int(box_h * screen_aspect_ratio)

    margin_x = w - box_w - 80 
    margin_y = (h - box_h) // 2

    cv2.rectangle(frame, (margin_x, margin_y), (margin_x + box_w, margin_y + box_h), (0, 0, 255), 2)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    result = detector.detect(mp_image)

    def get_pt(hand, idx):
        lm = hand[idx]
        return int(lm.x * w), int(lm.y * h)

    screen_left_hand = None
    screen_right_hand = None

    if result.hand_landmarks and result.handedness:
        for i in range(len(result.hand_landmarks)):
            hand_landmarks = result.hand_landmarks[i]
            handedness = result.handedness[i][0].category_name
            
            if handedness == "Left":
                screen_right_hand = hand_landmarks
            elif handedness == "Right":
                screen_left_hand = hand_landmarks

    is_zooming = False

    if screen_left_hand and screen_right_hand:
        l_thumb = get_pt(screen_left_hand, 4)
        l_ring = get_pt(screen_left_hand, 16)
        r_thumb = get_pt(screen_right_hand, 4)
        r_ring = get_pt(screen_right_hand, 16)

        l_pinch = np.hypot(l_ring[0] - l_thumb[0], l_ring[1] - l_thumb[1])
        r_pinch = np.hypot(r_ring[0] - r_thumb[0], r_ring[1] - r_thumb[1])

        if l_pinch < 45 and r_pinch < 45:
            is_zooming = True
            l_wrist = get_pt(screen_left_hand, 0)
            r_wrist = get_pt(screen_right_hand, 0)
            curr_zoom_dist = np.hypot(r_wrist[0] - l_wrist[0], r_wrist[1] - l_wrist[1])

            cv2.line(frame, l_wrist, r_wrist, (255, 165, 0), 4)
            cv2.putText(frame, "ZOOM MODE", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 3)

            if prev_zoom_dist != 0:
                zoom_delta = curr_zoom_dist - prev_zoom_dist
                if zoom_delta > 15:  
                    pyautogui.keyDown('ctrl')
                    pyautogui.scroll(150)
                    pyautogui.keyUp('ctrl')
                    prev_zoom_dist = curr_zoom_dist
                elif zoom_delta < -15: 
                    pyautogui.keyDown('ctrl')
                    pyautogui.scroll(-150)
                    pyautogui.keyUp('ctrl')
                    prev_zoom_dist = curr_zoom_dist
            else:
                prev_zoom_dist = curr_zoom_dist
        else:
            prev_zoom_dist = 0

    if screen_right_hand and not is_zooming:
        x_index, y_index = get_pt(screen_right_hand, 8)
        x_middle, y_middle = get_pt(screen_right_hand, 12)

        screen_x = np.interp(x_index, (margin_x, margin_x + box_w), (0, screen_w))
        screen_y = np.interp(y_index, (margin_y, margin_y + box_h), (0, screen_h))
        
        screen_x = np.clip(screen_x, 0, screen_w)
        screen_y = np.clip(screen_y, 0, screen_h)

        curr_x = prev_x + (screen_x - prev_x) / smoothening
        curr_y = prev_y + (screen_y - prev_y) / smoothening

        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y

        cv2.circle(frame, (x_index, y_index), 8, (255, 255, 0), cv2.FILLED)

        x_idx_base, y_idx_base = get_pt(screen_right_hand, 5)
        x_mid_base, y_mid_base = get_pt(screen_right_hand, 9)
        
        knuckle_gap = np.hypot(x_mid_base - x_idx_base, y_mid_base - y_idx_base)
        finger_gap = np.hypot(x_middle - x_index, y_middle - y_index)

        if finger_gap < (knuckle_gap * 1.15):
            cv2.line(frame, (x_index, y_index), (x_middle, y_middle), (0, 255, 0), 3)
            cv2.putText(frame, "SCROLLING", (w - 200, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            if prev_scroll_y != 0:
                scroll_delta = prev_scroll_y - y_index
                if abs(scroll_delta) > 4:
                    pyautogui.scroll(int(scroll_delta * 12))
            prev_scroll_y = y_index
        else:
            prev_scroll_y = 0

    if screen_left_hand and not is_zooming:
        x_wrist, y_wrist = get_pt(screen_left_hand, 0)
        x_thumb, y_thumb = get_pt(screen_left_hand, 4)
        x_index, y_index = get_pt(screen_left_hand, 8)
        x_mcp, y_mcp = get_pt(screen_left_hand, 9)
        x_pinky, y_pinky = get_pt(screen_left_hand, 20)
        x_middle, y_middle = get_pt(screen_left_hand, 12)
        x_ring, y_ring = get_pt(screen_left_hand, 16)

        left_click_dist = np.hypot(x_index - x_thumb, y_index - y_thumb)
        right_click_dist = np.hypot(x_pinky - x_thumb, y_pinky - y_thumb)

        palm_size = np.hypot(x_mcp - x_wrist, y_mcp - y_wrist)
        d_index = np.hypot(x_index - x_wrist, y_index - y_wrist)
        d_middle = np.hypot(x_middle - x_wrist, y_middle - y_wrist)
        d_ring = np.hypot(x_ring - x_wrist, y_ring - y_wrist)
        d_pinky = np.hypot(x_pinky - x_wrist, y_pinky - y_wrist)
        avg_tip_dist = (d_index + d_middle + d_ring + d_pinky) / 4.0

        if avg_tip_dist < (palm_size * 1.25):
            cv2.putText(frame, "DOUBLE CLICK", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 3)
            if not is_double_clicked:
                pyautogui.doubleClick()
                is_double_clicked = True
        else:
            is_double_clicked = False

            if left_click_dist < 40:
                cv2.circle(frame, (x_index, y_index), 12, (0, 0, 255), cv2.FILLED)
                if not is_left_clicked:
                    pyautogui.click()
                    is_left_clicked = True
            else:
                is_left_clicked = False

            if right_click_dist < 40:
                cv2.circle(frame, (x_pinky, y_pinky), 12, (0, 255, 0), cv2.FILLED)
                if not is_right_clicked:
                    pyautogui.rightClick()
                    is_right_clicked = True
            else:
                is_right_clicked = False

    cv2.imshow('Hand Tracking AI Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()