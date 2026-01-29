from fastapi import FastAPI, File, UploadFile, HTTPException
import cv2
import numpy as np
from ultralytics import YOLO
import io 
from PIL import Image 

app = FastAPI(title="VisionGuide AI - Korea Edition")

# load model
model = YOLO('yolov8n.pt')

def fresh_test(roi):
    # HSV Color Space Analysis: Detection of Brown (rot) and White (mold)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    #  decay mask (Brown)
    mask_decay = cv2.inRange(hsv, np.array([0, 20, 20]), np.array([30, 255, 100])) 
    # Mold Mask (White) - The 180-255 range is ideal for better white coverage.
    mask_mold = cv2.inRange(hsv, np.array([0, 0, 160]), np.array([180, 40, 255]))

    total_decay = np.sum(mask_decay > 0) + np.sum(mask_mold > 0)
    return total_decay / roi.size 


@app.post("/predict")
async def predict_freshness(file: UploadFile = File(...)):
    # Endpoint to receive an image and return object detection + freshness analysis.
    try:
        request_object_con = await file.read()
        img = Image.open(io.BytesIO(request_object_con)).convert("RGB")
        frame = np.array(img)
        # for Opencv change RGB from BGR to
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file!")

    # Execute AI Inference
    results = model(frame)
    detections = []

    for r in results:
        for box in r.boxes:
            label = model.names[int(box.cls[0])]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            # Crop the object area (Region of Interest)
            roi = frame[y1:y2, x1:x2]

            status = "Normal" # İf not fruit everything is okey

            # Freshness check logic for specific fruits/vegetables
            if label in ["carrot", "orange", "apple"]:
                if roi.size > 0:
                    disorder = fresh_test(roi)
                    status = "Sseogeun (Rotten)" if disorder > 0.12 else "Sinsunhan (Fresh)"

            # Construct JSON response for each detected object
            detections.append({
                "object": label, 
                "status": status,
                "confidence": round(float(box.conf[0]), 2)})

    return {"results": detections, "count": len (detections)}            


