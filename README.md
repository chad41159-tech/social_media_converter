# Social Media Converter

A simple web-based media converter that allows users to crop images and videos into popular social media aspect ratios.

## Features

- Upload images and videos
- Drag and drop file upload
- Convert media to different aspect ratios
- Supports:
  - 9:16 — TikTok / YouTube Shorts / Instagram Reels
  - 1:1 — Instagram Square Post
  - 4:5 — Instagram Vertical Feed
- Image conversion to JPEG
- Video cropping
- Simple and responsive web interface

## Technologies Used

- Python
- FastAPI
- Pillow
- MoviePy
- HTML
- CSS
- JavaScript

## Project Structure

```text
social_media_converter/
├── .gitignore
├── index.html
├── README.md
├── requirements.txt
├── server_local.py
└── temp_files/
    └── .gitkeep
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Go into the project folder:

```bash
cd social_media_converter
```

Create a virtual environment:

```bash
python -m venv .venv
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:

```bash
python server_local.py
```

Then open:

```text
http://127.0.0.1:8000
```

## Supported Aspect Ratios

| Ratio | Platform / Use |
|---|---|
| 9:16 | TikTok, YouTube Shorts, Instagram Reels |
| 1:1 | Instagram Square Post |
| 4:5 | Instagram Vertical Feed |

## Note

The `.venv` folder and generated files inside `temp_files` are excluded from Git using `.gitignore`.
