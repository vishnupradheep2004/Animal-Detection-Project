# Animal Detection with Custom Trained YOLOv8

![Python](https://img.shields.io/badge/Python-3.9-blue.svg?style=flat-square&logo=python)
![Ultralytics](https://img.shields.io/badge/Ultralytics-8.1.29-green.svg?style=flat-square)

## Overview

Welcome to the Animal Detection with Custom Trained YOLOv5 project! This application enables real-time animal detection using a custom-trained YOLOv5 model integrated with OpenCV. Whether you're monitoring wildlife or studying animal behavior, this tool provides accurate and efficient detection capabilities.

### Key Features

- Real-time animal detection using the webcam feed.
- Support for multiple animal species with customizable class labels.
- Integration with OpenCV for seamless execution and visualization.
- Efficient inference leveraging hardware acceleration platforms.

## Job Opportunity

**Role:** Computer Vision Engineer / YOLO Developer

**Job Description:**
This role focuses on improving and extending the animal detection pipeline using YOLOv8. The team member will work on dataset preparation, model training, inference optimization, and integration with the existing OpenCV-based application. The position is ideal for someone who enjoys developing practical computer vision solutions, debugging real-world detection workflows, and deploying models for monitoring animal behavior.

**Responsibilities:**

- Prepare and annotate training datasets for animal detection.
- Train, validate, and optimize YOLOv8 models for accuracy and speed.
- Integrate model inference into the application workflow.
- Evaluate detection performance and implement improvements.
- Support documentation, testing, and deployment of the project.

**Qualifications:**

- Strong Python programming skills.
- Experience with YOLO/Ultralytics, OpenCV, and deep learning.
- Familiarity with computer vision workflows and object detection.
- Ability to analyze model predictions and tune performance.
- Good communication and documentation habits.

## Installation

To run the Animal Detection with Custom Trained YOLOv5 project, follow these steps:

1. Clone this repository to your local machine.
2. Install Python 3.9 and create a virtual environment.
3. Install required dependencies: `pip install -r requirements.txt`.
4. Download the YOLOv8 model weights and place them in the specified directory.
5. Run the `main.py` script.

## Folder Structure

```
📂 animal_detection_yolov5/
├── 📁 data/
│   ├── 📁 train/
│   │   ├── 📁 images/
│   │   └── 📁 labels/
│   └── 📁 valid/
│       ├── 📁 images/
│       └── 📁 labels/
├── 📂 runs/
│   └── 📂 detect/
│       └── 📂 train/
│           └── 📂 weights/
│               └── 📄 best.pt
├── 📄 main.py
├── 📄 config.yaml
├── 📄 model.py
└── 📄 requirements.txt
```

## Usage

```bash
python main.py
```

## Screenshots

<div style="display: flex; justify-content: center; align-items: center;">
  <img src="https://raw.githubusercontent.com/Rajivjha003/Animal_Detection_YOLOV8/main/demo/Predict.jpg" alt="GIF" width="1234" height="214">
</div>

## Contributing

Contributions are welcome! If you have any ideas for improvements or new features, feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
