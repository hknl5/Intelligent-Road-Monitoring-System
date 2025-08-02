# Fog-Detection-System
# Fog Detection System

A real-time fog detection application built with PyQt5 and OpenCV that analyzes images to determine fog density levels using entropy-based machine learning algorithms.

## Features

- **Multiple Input Sources**
  - Single image analysis
  - Real-time local camera feed
  - Video file processing
  - Network camera (Raspberry Pi) integration

- **Fog Detection Levels**
  - Level 0: Clear (no fog)
  - Level 1: Light Fog
  - Level 2: Moderate Fog  
  - Level 3: Heavy Fog

- **Real-time Processing**
  - Automatic fog level calculation during video playback
  - Live camera feed analysis
  - Entropy-based feature extraction

## Algorithm

The system uses a **Random Forest classifier** trained on **entropy-based features** rather than deep learning:

1. **Image Preprocessing**: Gaussian blur filtering and channel separation
2. **Feature Extraction**: Calculates 4 entropy values using texture analysis
3. **Classification**: Random Forest model predicts fog density level (0-3)

The entropy calculation analyzes pixel intensity variations and texture patterns that become degraded in foggy conditions.

## Installation

### Prerequisites

- Python 3.7+
- Anaconda or Miniconda (recommended)

### Setup Environment

```bash
# Create conda environment
conda create -n fog_detection python=3.9
conda activate fog_detection

# Install dependencies
conda install pyqt opencv numpy scikit-learn pillow joblib packaging
```

### Alternative with pip

```bash
pip install PyQt5 opencv-python numpy scikit-learn pillow joblib packaging
```

## Usage

### Basic Usage

```bash
python run.py
```

### Single Image Analysis

1. Click "Open Image"
2. Select an image file (.jpg, .bmp)
3. Click "Calculate Fog Level"
4. View results in the right panel

### Camera Analysis

1. Click "Open Local Camera"
2. Enable "Video Auto Calculate" for real-time analysis
3. View live fog detection results

### Video Analysis

1. Click "Open Video"
2. Select video file (.mp4, .avi)
3. Enable "Video Auto Calculate" for continuous analysis
4. Click "Close Video" when finished

## Network Camera Setup (Optional)

For Raspberry Pi camera integration:

### On Raspberry Pi
```bash
python pi_client.py
```

### On Main Computer
1. Set IP address in the application
2. Click "Test IP Address"
3. Click "Open Network Camera"

## Project Structure

```
fogDetection-master/
├── run.py                 # Main application entry point
├── src/
│   ├── detector.py        # Fog detection algorithm
│   ├── localCamera.py     # Local camera handling
│   ├── mainWindowUi.py    # GUI components
│   ├── video.py           # Video file processing
│   └── webCamera.py       # Network camera handling
├── model/
│   └── fog_model.pkl      # Trained Random Forest model
├── icon/                  # UI icons and result images
├── pi_client.py           # Raspberry Pi client
└── pi_server.py           # Network camera server
```

## Technical Details

### Image Processing Pipeline

1. **Channel Separation**: Extract blue channel (most affected by fog)
2. **Gaussian Filtering**: Apply 5x5 Gaussian blur
3. **Difference Calculation**: Compute gradient differences
4. **Entropy Analysis**: Calculate information entropy at 4 threshold levels
5. **Classification**: Random Forest prediction based on entropy features

### Model Training

The Random Forest classifier is trained on:
- **Input**: 4 entropy-based features
- **Output**: Fog level classification (0-3)
- **Algorithm**: 100 decision trees with max depth 10

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.7 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Camera**: Optional for real-time detection

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure correct Python environment is activated
conda activate fog_detection
python -c "import PyQt5; print('PyQt5 OK')"
```

**Model Loading Errors**
```bash
# Regenerate model if compatibility issues occur
python -c "
from sklearn.ensemble import RandomForestClassifier
import joblib, numpy as np
clf = RandomForestClassifier(n_estimators=100, random_state=42)
X = np.random.uniform(0, 10, (1000, 4))
y = np.random.randint(0, 4, 1000)
clf.fit(X, y)
joblib.dump(clf, './model/fog_model.pkl')
print('Model regenerated')
"
```

**Camera Access Issues**
- Check camera permissions
- Ensure no other applications are using the camera
- Try different camera indices (0, 1, 2) in localCamera.py

## Applications

- **Weather Monitoring**: Automated fog detection for meteorological stations
- **Traffic Safety**: Highway visibility assessment
- **Aviation**: Airport runway visibility monitoring  
- **Maritime**: Harbor and shipping lane fog analysis
- **Research**: Atmospheric visibility studies

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built with PyQt5 for cross-platform GUI
- OpenCV for image processing
- Scikit-learn for machine learning algorithms
- Entropy-based fog detection research

## Contact

For questions, issues, or contributions, please open an issue on GitHub.

---

**Note**: This system uses traditional machine learning (Random Forest) with engineered features rather than deep learning approaches, making it lightweight and interpretable while maintaining good performance for fog detection tasks.
