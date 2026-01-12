# NonMouse - Hand Gesture Mouse Control

Control your computer mouse using hand gestures through your webcam. No physical mouse needed!

## Features

- **Cursor Control**: Point with index finger to move cursor
- **Left Click**: Pinch thumb and index finger together
- **Right Click**: Hold pinch for 1.5 seconds without moving
- **Scroll**: Lower index finger below hand level
- **Copy**: Make a fist (all fingers down)
- **Paste**: Peace sign (index and middle finger up)

## Installation

1. Install Python 3.9+
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python -m nonmouse
```

1. Select your camera device (usually 0)
2. Choose placement mode (Normal recommended)
3. Adjust sensitivity (30 is default)
4. Show your hand to the camera
5. Use gestures to control your mouse

## Gestures Guide

| Gesture | Action | Description |
|---------|--------|-------------|
| 👉 Point | Move Cursor | Point with index finger |
| 🤏 Pinch | Left Click | Touch thumb to index finger |
| 🤏➡️ Hold Pinch | Right Click | Hold pinch for 1.5s without moving |
| 👇 Lower Finger | Scroll | Lower index finger below hand |
| ✊ Fist | Copy | Close all fingers (Ctrl+C) |
| ✌️ Peace | Paste | Index and middle finger up (Ctrl+V) |

## System Requirements

- Python 3.9+
- Webcam
- Windows/macOS/Linux
- Good lighting for hand detection

## Dependencies

- OpenCV
- MediaPipe
- NumPy
- pynput
- tkinter

## Troubleshooting

- **Hand not detected**: Ensure good lighting and clear hand visibility
- **Cursor too sensitive**: Lower sensitivity in setup dialog
- **Gestures not working**: Check finger count display in bottom left
- **Camera not working**: Try different camera device numbers (0, 1, 2, 3)

## License

MIT License - See LICENSE file for details