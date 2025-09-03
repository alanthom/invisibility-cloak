# Invisibility Cloak using OpenCV

This program creates an invisibility cloak effect using OpenCV in Python. It works by replacing pixels of a specific color (e.g., red cloak) in the video with the background, making the cloak appear invisible.

## Setup Instructions

1. **Create a virtual environment**
   - On Windows PowerShell, run:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

2. **Install dependencies**
   - With the virtual environment activated, run:
     ```powershell
     pip install opencv-python numpy
     ```

3. **Prepare your video**
   - Place your input video in the workspace folder and name it `input.mp4`.
   - The first few seconds of the video should show only the background (no cloak or person).
   - Wear a bright red cloak for best results.

4. **Run the program**
   - Execute the script:
     ```powershell
     python cloak.py
     ```
   - The output video will be saved as `output.mp4`.

## How it works
- The script captures the background from the first few frames.
- It detects the red color in each frame and replaces those pixels with the background.
- The result is an "invisible" cloak effect.

## Customization
- You can adjust the color range in `cloak.py` to use a different cloak color.

---

**Author:** alanthom