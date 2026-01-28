# VisionAssist-AI-Powered-Life-Assistant
Empowering the Visually Impaired with Computer Vision
📝 Project Overview / 프로젝트 개요
EN: VisionAssist is a real-time object recognition and biological decay detection system designed for the visually impaired. Using YOLOv8 and HSV Color Analysis, it not only identifies items like carrots and oranges but also assesses their freshness in the user's native language. KO: VisionAssist는 시각 장애인을 위한 실시간 사물 인식 및 생물학적 부패 감지 시스템입니다. YOLOv8과 HSV 색상 분석을 사용하여 당근이나 오렌지와 같은 품목을 식별할 뿐만 아니라 사용자의 모국어로 신선도를 평가합니다.

🚀 Key Features / 주요 특징
Multi-Language Voice Support: Currently optimized for Korean (Hangul), with easy expansion to English and other languages.

Freshness Detection: Advanced algorithm to detect brown rot and white mold using pixel density analysis.

Manual Recording [R]: Instant video capture for sharing or debugging.

Priority Focus: Intelligent logic that prioritizes fruits/vegetables over background noise.

🛠️ Tech Stack / 기술 스택
AI: Ultralytics YOLOv8 (Object Detection)

Vision: OpenCV (Image Processing & HSV Analysis)

Speech: gTTS (Google Text-to-Speech)

Logic: Python Multithreading (Zero-lag performance)

📖 How to Use / 사용 방법
Run the script: python huseyin_ai.py

Detection: Point the camera at a carrot or orange.

Feedback: Listen for "Sinsunhan" (Fresh) or "Sseogeun" (Rotten).

Translate: Can be easily translated to English or any other language by changing the lang parameter.
