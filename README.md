# Vehicle Detection using OpenCV

A simple, real-time vehicle detection system leveraging classic background subtraction in OpenCV. This project detects moving vehicles in a given video (or webcam feed) and draws bounding boxes around them.

---

## Features

- Background subtraction (MOG2) for moving-object segmentation
- Noise removal via morphological operations and thresholding
- Contour detection to find vehicle-shaped blobs
- Adjustable minimum contour area to filter out small artifacts
- Two display windows: one for annotated frames, one for the foreground mask

---

## Requirements

Tested on Ubuntu 20.04+ (or any Debian-based distro).

- Python 3.6+
- OpenCV (with GUI/video support)
- imutils (for easy resizing and contour handling)
- FFmpeg (for reliable video decoding)

---

## Installation

### Option A: System-wide (APT)

```bash
sudo apt update && \
  sudo apt install -y python3 python3-pip python3-opencv libopencv-dev ffmpeg
```

### Option B: Python Virtual Environment (pip)

```bash
# 1. Create & activate venv
python3 -m venv ~/vehdet-env
source ~/vehdet-env/bin/activate

# 2. Install dependencies
pip install --upgrade pip
pip install opencv-python imutils
# (Optional: pip install ultralytics  # for YOLO upgrade)
```

---

## Usage

1. **Download or provide a video file**:

   ```bash
   # Example: royalty-free traffic clip
   wget -O traffic.mp4 \
     https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/car-detection.mp4
   ```
2. **Save the python file**

   ```bash
   nano vehicle_detection.py
   ```
   
3. **Run the detector**:

   ```bash
   cd ~/vehicle-detector
   python3 vehicle_detection.py --video traffic.mp4
   ```

4. **Controls**:

   - Press **q** to quit.
   - Adjust the detection sensitivity with `--min-area` (default: 500).

---
## Output video
[![Watch the video](https://img.youtu.be.com/vi/jbaWU47-TRk.jpg)](https://youtu.be/jbaWU47-TRk)

## Script Options

| Flag             | Description                                          | Default |
| ---------------- | ---------------------------------------------------- | ------- |
| `-v, --video`    | Path to input video (omit for webcam)                | `None`  |
| `-m, --min-area` | Minimum contour area (in pixels) to detect a vehicle | `500`   |

---

## Troubleshooting

- **Could not open video source**:

  - Verify the file exists and path is correct (`ls -lh traffic.mp4`).
  - Ensure OpenCV can decode the format (`sudo apt install ffmpeg`).
  - Test with absolute path: `--video ~/traffic.mp4`.

- **Qt plugin "xcb" error**:

  ```bash
  sudo apt install -y libxcb-xinerama0 libxkbcommon-x11-0
  ```

- **Python import errors**:

  - Make sure you’re using the venv’s `python` if you opted for Option B.
  - Reinstall the PyPI wheel: `pip install --upgrade opencv-python`.

---

## Extending with Deep Learning

To improve accuracy and handle overlapping or stationary vehicles, swap out the background-subtraction block with a YOLO or MobileNet-SSD inference loop. The rest of the script (display, trails, counters) remains the same.

---

## License

This project is released under the MIT License. Feel free to use and modify as needed.
