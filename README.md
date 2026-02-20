# Behavioral Biometrics Authentication System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![dlib](https://img.shields.io/badge/dlib-19.x-orange.svg)](http://dlib.net/)

A real-time behavioral biometrics authentication system combining **facial recognition** and **blink detection** for continuous session access control. The system verifies user identity through facial features and monitors blink patterns throughout the session to ensure ongoing authentication.

![System Demonstration](demo.gif)
*Real-time face recognition and blink detection system*

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements a **multi-factor behavioral biometrics authentication system** that combines:

1. **Face Recognition** - Identifies and verifies the user's identity
2. **Blink Detection** - Monitors natural eye blink patterns as a behavioral biometric
3. **Continuous Authentication** - Maintains security throughout the entire session

The system uses computer vision techniques to analyze facial landmarks and eye aspect ratios (EAR) to detect blinks, providing a non-intrusive yet secure authentication mechanism.

## ✨ Features

### Current Implementation

- ✅ **Real-time Face Detection** using dlib's HOG-based detector
- ✅ **Facial Recognition** with 128-dimensional face embeddings
- ✅ **Blink Detection** using Eye Aspect Ratio (EAR) algorithm
- ✅ **Live Video Processing** with OpenCV
- ✅ **Visual Feedback** with bounding boxes and status indicators

### Planned Features

- 🔄 **Access Control System** - Grant/deny access based on combined authentication
- 🔄 **Session Monitoring** - Continuous verification throughout user session
- 🔄 **Behavioral Profiling** - Learn individual blink patterns
- 🔄 **Alert System** - Detect unauthorized access attempts
- 🔄 **Multi-user Support** - Database of authorized users
- 🔄 **Logging & Analytics** - Track authentication events and patterns

## 🔬 How It Works

### 1. Face Recognition

The system uses **dlib's face recognition model** to:
- Detect faces in real-time video stream
- Extract 68 facial landmarks
- Generate 128-dimensional face embeddings
- Compare embeddings with authorized user database
- Calculate similarity scores for authentication

### 2. Blink Detection Algorithm

Blink detection is based on the **Eye Aspect Ratio (EAR)** method:

#### Eye Aspect Ratio Formula

```
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
```

Where:
- `p1, p2, p3, p4, p5, p6` are the 6 facial landmarks around one eye
- `||·||` denotes Euclidean distance
- Vertical eye landmarks: p2, p3, p5, p6
- Horizontal eye landmarks: p1, p4

#### Detection Logic

1. **Calculate EAR** for both eyes
2. **Average the values** to get overall eye openness
3. **Threshold comparison**: EAR < 0.25 indicates closed eye
4. **Consecutive frames**: Blink detected when eyes closed for 2-3 consecutive frames
5. **Blink counter** tracks total blinks in session

See the [Eye Aspect Ratio Diagram](#ear-diagram) below for visual explanation.

### 3. Authentication Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    START VIDEO STREAM                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               DETECT FACE IN FRAME                           │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌──────────────────┐          ┌──────────────────────┐
│  Face Recognition│          │  Blink Detection     │
│  - Extract embed │          │  - Calculate EAR     │
│  - Compare DB    │          │  - Track blinks      │
│  - Verify ID     │          │  - Count patterns    │
└────────┬─────────┘          └──────────┬───────────┘
         │                               │
         └───────────────┬───────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│          BOTH AUTHENTICATED? → GRANT ACCESS                  │
│          MONITOR CONTINUOUSLY DURING SESSION                 │
└─────────────────────────────────────────────────────────────┘
```

## 🛠 Technologies Used

### Core Libraries

- **Python 3.8+** - Programming language
- **OpenCV 4.x** - Computer vision and video processing
- **dlib** - Face detection and facial landmark recognition
- **NumPy** - Numerical computations for EAR calculations
- **face_recognition** - High-level face recognition API built on dlib

### Algorithms

- **Histogram of Oriented Gradients (HOG)** - Face detection
- **68-point facial landmark detection** - Facial feature extraction
- **ResNet-based face embeddings** - Face recognition (128-D vectors)
- **Eye Aspect Ratio (EAR)** - Blink detection
- **Euclidean distance** - Similarity measurement

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Webcam or camera device
- (Optional) CUDA-capable GPU for faster processing

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/behavioral-biometrics-auth.git
cd behavioral-biometrics-auth
```

### Step 2: Create virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

**Note**: Installing dlib on Windows may require CMake and Visual Studio. See [dlib installation guide](http://dlib.net/compile.html) for details.

### Step 4: Download pre-trained models

The system uses dlib's pre-trained models:
- `shape_predictor_68_face_landmarks.dat`
- `dlib_face_recognition_resnet_model_v1.dat`

Download from [dlib model files](http://dlib.net/files/) and place in the project root or `models/` directory.

## 🚀 Usage

### Basic Face Recognition and Blink Detection

```bash
python blink.py
```

This will:
1. Start your webcam
2. Detect your face in real-time
3. Display blink count and EAR values
4. Show live video feed with annotations

### Controls

- **Press 'q'** - Quit the application
- **Press 's'** - Save current frame
- **Press 'r'** - Reset blink counter

### Register New User (Coming Soon)

```bash
python register_user.py --name "Your Name" --images 20
```

### Run with Access Control (Planned)

```bash
python main.py --mode continuous --timeout 300
```

## 📁 Project Structure

```
behavioral-biometrics-auth/
│
├── models/                              # Pre-trained model files
│   ├── shape_predictor_68_face_landmarks.dat
│   └── dlib_face_recognition_resnet_model_v1.dat
│
├── data/                                # User data (excluded from git)
│   ├── faces/                           # Authorized user face images
│   └── embeddings.pkl                   # Stored face embeddings
│
├── src/                                 # Source code
│   ├── face_recognition.py              # Face recognition module
│   ├── blink_detection.py               # Blink detection module
│   └── utils.py                         # Utility functions
│
├── notebooks/                           # Jupyter notebooks for testing
│   └── algorithm_testing.ipynb
│
├── logs/                                # Authentication logs
│   └── auth_log.txt
│
├── blink.py                             # Main blink detection script
├── blinkdetect.py                       # Alternative implementation
├── requirements.txt                     # Python dependencies
├── .gitignore                           # Git ignore rules
├── README.md                            # This file
└── LICENSE                              # MIT License
```

## 🔮 Future Enhancements

### Phase 1: Access Control System (In Progress)

- [ ] Implement access grant/deny logic based on combined authentication
- [ ] Add user registration system
- [ ] Create database of authorized users
- [ ] Develop session management

### Phase 2: Continuous Authentication

- [ ] Monitor user throughout entire session
- [ ] Detect suspicious behavioral changes
- [ ] Implement re-authentication triggers
- [ ] Add timeout mechanisms

### Phase 3: Advanced Behavioral Analysis

- [ ] Profile individual blink patterns
- [ ] Detect fatigue through blink rate analysis
- [ ] Anti-spoofing measures (liveness detection)
- [ ] Machine learning for anomaly detection

### Phase 4: System Integration

- [ ] REST API for external system integration
- [ ] Web dashboard for monitoring
- [ ] Mobile app support
- [ ] Multi-camera support

## 📊 Eye Aspect Ratio (EAR) Diagram

*(See generated diagram image in repository)*

The Eye Aspect Ratio is calculated using 6 facial landmarks around each eye:
- Points p1 and p4 define the horizontal eye span
- Points p2, p3, p5, p6 define the vertical eye spans
- When eyes are open: EAR ≈ 0.3
- When eyes are closed: EAR < 0.25
- Blink is detected when EAR drops below threshold for consecutive frames

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

Run specific test:
```bash
pytest tests/test_blink_detection.py -v
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- [dlib](http://dlib.net/) - Facial landmark detection
- [OpenCV](https://opencv.org/) - Computer vision library
- [face_recognition](https://github.com/ageitgey/face_recognition) - Simplified face recognition API
- Research paper: "Real-Time Eye Blink Detection using Facial Landmarks" by Soukupová and Čech (2016)

## 📧 Contact

For questions or feedback, please open an issue or contact [your.email@example.com](mailto:your.email@example.com)

---

⭐ **If you find this project useful, please consider giving it a star!** ⭐
