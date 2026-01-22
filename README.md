🖐️ NoMouse – Control Your Computer Using Hand Gestures

A computer vision–based virtual mouse system that allows users to control the mouse cursor using hand gestures captured through a webcam. This project eliminates the need for a physical mouse by leveraging Python, OpenCV, and MediaPipe.

📌 Project Overview

NoMouse tracks hand landmarks in real time and maps specific hand gestures to mouse actions such as:

Cursor movement

Left click

Right click

Scrolling

Drag and drop

This project is useful for:

Touch-free computer interaction

Accessibility solutions

Human–Computer Interaction (HCI) research

Learning computer vision and gesture recognition

🚀 Features

✔ Real-time hand detection
✔ Smooth mouse cursor movement
✔ Left & right mouse click using gestures
✔ Scroll up & down using hand motion
✔ Drag and drop functionality
✔ Platform-independent (Windows / Linux / macOS)

🛠️ Technologies Used

Python 3

OpenCV – image processing

MediaPipe – hand landmark detection

NumPy – numerical operations

PyAutoGUI / Pynput – mouse & keyboard control

📂 Project Structure
NoMouse/
│
├── main.py                 # Main application file
├── hand_tracking.py        # Hand detection & landmark tracking
├── mouse_controller.py     # Mouse control logic
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── assets/                 # Images / demo screenshots

🧑‍💻 Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/NoMouse.git
cd NoMouse

2️⃣ Create a Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt


requirements.txt

opencv-python
mediapipe
numpy
pyautogui
pynput

▶️ How to Run
python main.py


📷 Make sure your webcam is connected and working.

✋ Gesture Controls
Gesture	Action
Index finger up	Move mouse
Index + Thumb close	Left click
Middle + Thumb close	Right click
Two fingers up	Scroll
Fist	Drag
Open palm	Release drag

(Gestures can be customized in the code)

⚙️ How It Works

Webcam captures live video frames

MediaPipe detects 21 hand landmarks

Finger positions are analyzed

Gestures are recognized based on distances and angles

Mouse actions are executed using PyAutoGUI / Pynput

📸 Demo

Add screenshots or a GIF here to showcase the working project.

assets/demo.gif

⚠️ Limitations

Requires good lighting conditions

Performance depends on webcam quality

Background clutter may affect accuracy

Slight delay on low-end systems

🔮 Future Enhancements

Multi-hand support

Gesture customization UI

AI-based gesture learning

Mobile camera support

Voice + gesture hybrid control

📚 Learning Outcomes

Computer Vision fundamentals

Hand landmark detection

Gesture recognition logic

Human-Computer Interaction (HCI) concepts

Real-time system development

👤 Author

Abdus Salam
Android Developer • Python Enthusiast • UI Explorer
