# Intelligent Road Monitoring System

## Overview
An intelligent system that monitors mountainous roads (like Aqabat Dhalq) in real-time using cameras and sensors. The system detects accidents, rockslides, fog, and other hazards, displaying them instantly on an interactive dashboard for authorities.

## System Components

### 1. Car Crash Detection
Real-time accident detection using computer vision and machine learning algorithms.

**Repository:** [Car-Crash-Detection](https://github.com/hknl5/Car-Crash-Detection)

**Features:**
- Real-time video analysis
- Accident detection and classification
- Instant alert generation
- Integration with central monitoring system

### 2. Fog Detection System
Environmental hazard detection focusing on fog and visibility conditions.

**Repository:** [Fog-Detection-System](https://github.com/hknl5/Fog-Detection-System)

**Features:**
- Fog density measurement
- Visibility assessment
- Weather condition monitoring
- Real-time hazard alerts

## How to Run

### Prerequisites
- Python 3.8+
- OpenCV
- Required dependencies (see requirements.txt in each repo)

### Running Car Crash Detection
```bash
cd Car-Crash-Detection
pip install -r requirements.txt
python main.py
```

### Running Fog Detection System
```bash
cd Fog-Detection-System
pip install -r requirements.txt
python main.py
```

## Architecture
```
[Road Cameras] → [Detection Systems] → [Central Dashboard] → [Authorities]
```

## Target Use Case
- **Location:** Mountainous roads (Aqabat Dhalq and similar)
- **Hazards Detected:** Accidents, rockslides, fog, visibility issues
- **Users:** Traffic authorities, emergency services
- **Output:** Real-time interactive dashboard with instant alerts

## Key Benefits
- **Real-time monitoring** of dangerous road conditions
- **Instant alerts** for emergency response
- **Comprehensive coverage** of multiple hazard types
- **Centralized dashboard** for efficient monitoring

## Technology Stack
- Computer Vision (OpenCV)
- Machine Learning
- Real-time video processing
- Dashboard visualization
- Alert notification system

---
*Developed for hackathon - Intelligent road safety monitoring solution*
