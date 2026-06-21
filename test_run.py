#!/usr/bin/env python
import sys
import os

print("Starting diagnostics...")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print()

# Test imports
try:
    print("Testing imports...")
    from ultralytics import YOLO
    print("✓ YOLO imported successfully")
except ImportError as e:
    print(f"✗ Failed to import YOLO: {e}")
    
try:
    import cv2
    print("✓ cv2 imported successfully")
except ImportError as e:
    print(f"✗ Failed to import cv2: {e}")

try:
    import math
    print("✓ math imported successfully")
except ImportError as e:
    print(f"✗ Failed to import math: {e}")

print()
print("Checking model path...")
model_path = "runs/detect/train/weights/best.pt"
if os.path.exists(model_path):
    print(f"✓ Model found at {model_path}")
    print(f"  File size: {os.path.getsize(model_path)} bytes")
else:
    print(f"✗ Model NOT found at {model_path}")
    print(f"  Current working directory: {os.getcwd()}")
    if os.path.exists("runs"):
        print("  ✓ runs/ directory exists")
        if os.path.exists("runs/detect"):
            print("    ✓ runs/detect/ directory exists")
            if os.path.exists("runs/detect/train"):
                print("      ✓ runs/detect/train/ directory exists")
                if os.path.exists("runs/detect/train/weights"):
                    print("        ✓ runs/detect/train/weights/ directory exists")
                    files = os.listdir("runs/detect/train/weights")
                    print(f"        Files: {files}")
                else:
                    print("        ✗ runs/detect/train/weights/ directory NOT found")
            else:
                print("      ✗ runs/detect/train/ directory NOT found")
        else:
            print("    ✗ runs/detect/ directory NOT found")
    else:
        print("  ✗ runs/ directory NOT found")

print()
print("Checking webcam availability...")
try:
    import cv2
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("✓ Webcam is available")
        cap.release()
    else:
        print("✗ Webcam is NOT available")
except Exception as e:
    print(f"✗ Error checking webcam: {e}")

print()
print("Diagnostics complete!")
