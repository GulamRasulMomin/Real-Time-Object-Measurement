# Real-Time Object Measurement

A computer-vision app that detects an A4 sheet in a photo, rectifies its perspective, and estimates the width and height of quadrilateral objects on the sheet in centimetres. The main interface is a Streamlit web app.

## How it works

The A4 sheet is used as a known-size reference (210 × 297 mm). The app finds its four-corner contour, corrects the image perspective, then detects four-corner object contours and displays their estimated dimensions. It also shows the original and processed images and provides a PNG download of the result.

## Tech stack

- **Python** — application language.
- **Streamlit** — web interface, image upload, measurement display, and download.
- **OpenCV** — image processing, contour detection, perspective correction, and annotations.
- **NumPy** — image array handling and numerical operations.
- **Pillow** — image loading and format conversion.
- **Pandas** — tabular display of measurements.

## Requirements

- Python
- Dependencies listed in [`requirements.txt`](requirements.txt)

## Setup

From the project directory, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell prevents environment activation, use the equivalent activation command for your shell or run the environment's Python directly.

## Run the app

```powershell
streamlit run app.py
```

Open the local URL printed by Streamlit, upload a JPG, JPEG, or PNG photo, and review the detected objects and measurements. If no A4 sheet is detected, try a clear, well-lit photo with the entire sheet visible.

## Tips for better measurements

- Place objects flat on the A4 sheet and avoid overlapping them.
- Include all four sheet corners in the image.
- Keep the camera as parallel to the sheet as possible and use even lighting.
- Measurements depend on contour detection and the detected A4 outline, so treat them as estimates.

## Project files

- `app.py` — Streamlit interface and measurement workflow.
- `utlis.py` — contour detection, perspective correction, point ordering, and distance helpers.
- `ObjectMeasurement.py` — standalone OpenCV-window version; uses `3.jpg` by default. Its input and webcam settings are configured near the top of the file.
- `requirements.txt` — Python package dependencies.
