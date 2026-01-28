import cv2
import numpy as np
from ultralytics import YOLO
from gtts import gTTS
import playsound
import os
import time
import threading

# --- BAŞLATMA ---
model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

is_recording = False 
out = None

dictionary = {
    "apple": "Sagwa", "banana": "Banana", "orange": "Orenji",
    "cell phone": "Hyudaepon", "person": "Saram", "cup": "Keop",
    "bottle": "Byeong", "carrot": "Danggeun"
}

def play_audio(filename):
    try:
        playsound.playsound(filename)
        # Let's not delete the file immediately, sometimes the library does not release the file
        time.sleep(0.1) 
        if os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        print(f"Play Error: {e}")

def speak(text, lang='ko'):
    try:
        print(f"🌍 Voice Output: {text}")
        tts = gTTS(text=text, lang=lang)
        # Each audio file must be given a unique name to avoid conflicts
        filename = f"voice_{int(time.time() * 1000)}.mp3"
        tts.save(filename)
        threading.Thread(target=play_audio, args=(filename,), daemon=True).start()
    except Exception as e:
        print(f"Audio Error: {e}")

def fresh_test(roi):
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask_decay = cv2.inRange(hsv, np.array([0, 20, 20]), np.array([30, 255, 100]))
    mask_mold = cv2.inRange(hsv, np.array([0, 0, 160]), np.array([180, 40, 255]))
    total_decay = np.sum(mask_decay > 0) + np.sum(mask_mold > 0) 
    return total_decay / roi.size

last_voice_time = 0
print("🚀 Asistant Ready! [R]: Record start/stop | [Q]: Exit")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break 

    results = model(frame, stream=True)

    for r in results:
        annotated_frame = r.plot()
        
        # KAYIT MANTIĞI DÜZELTİLDİ
        if is_recording and out is not None:
            cv2.putText(annotated_frame, "● RECORDING", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            out.write(annotated_frame)

        if time.time() - last_voice_time > 4:
            target_box = None
            boxes = r.boxes
            labels = [model.names[int(b.cls[0])] for b in boxes]

            # Meyve önceliği
            for i, label in enumerate(labels):
                if label in ["carrot", "orange", "apple"]:
                    target_box = (label, boxes[i])
                    break 

            if not target_box:
                for i, label in enumerate(labels):
                    if label in dictionary:
                        target_box = (label, boxes[i])
                        break 

            if target_box:
                label, box = target_box
                status = ""
                if label in ["carrot", "orange"]:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    roi = frame[y1:y2, x1:x2]
                    if roi.size > 0:
                        disorder = fresh_test(roi)
                        status = "Sseogeun " if disorder > 0.12 else "Sinsunhan "

                k_name = dictionary.get(label, "Bilinmeyen")
                speak(f"{status}{k_name}", lang='ko')
                last_voice_time = time.time()
                break 

    cv2.imshow('Global Vision AI - Korea Edition', annotated_frame) 
    
    key = cv2.waitKey(1) & 0xFF 
    if key == ord('q'):
        break 
    elif key == ord('r'):
        if not is_recording:
            # Recording start
            out = cv2.VideoWriter(f'demo_{int(time.time())}.mp4', fourcc, 20.0, (width, height))
            is_recording = True 
            print("🔴 Recording Start!")
        else:
            # Recording stop
            is_recording = False
            if out: out.release()
            print("✅ Record complete!")

cap.release()
if out: out.release()
cv2.destroyAllWindows()
