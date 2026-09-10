from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image
import os
import shutil

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "temp_files")

os.makedirs(UPLOAD_DIR, exist_ok=True)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/")
async def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


# --------------------------------------------------
# MEDIA CONVERTER
# --------------------------------------------------

@app.post("/upload")
async def convert_media(
    file: UploadFile = File(...),
    ratio: str = Form("9_16")
):

    print(f"Received file: {file.filename}")
    print(f"Content type: {file.content_type}")
    print(f"Selected ratio: {ratio}")

    # Get extension
    _, file_ext = os.path.splitext(file.filename)
    file_ext = file_ext.lower()

    # Supported ratios
    ratio_map = {
        "9_16": 9 / 16,
        "1_1": 1 / 1,
        "4_5": 4 / 5
    }

    if ratio not in ratio_map:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid aspect ratio selected."}
        )

    target_ratio = ratio_map[ratio]

    # --------------------------------------------------
    # SAVE INPUT FILE
    # --------------------------------------------------

    input_path = os.path.join(
        UPLOAD_DIR,
        "input" + file_ext
    )

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # --------------------------------------------------
    # IMAGE PROCESSING
    # --------------------------------------------------

    image_types = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/avif",
        "image/gif",
        "image/bmp",
        "image/tiff"
    ]

    if file.content_type in image_types:

        try:

            print("Processing IMAGE...")

            img = Image.open(input_path)

            # Fully load image
            img.load()

            print("Original size:", img.size)
            print("Image mode:", img.mode)

            # Convert to RGB
            if img.mode != "RGB":
                img = img.convert("RGB")

            width, height = img.size

            current_ratio = width / height

            # --------------------------------------------------
            # CROP
            # --------------------------------------------------

            if current_ratio > target_ratio:

                # Image is too wide
                new_width = int(height * target_ratio)

                left = (width - new_width) // 2

                cropped = img.crop(
                    (
                        left,
                        0,
                        left + new_width,
                        height
                    )
                )

            else:

                # Image is too tall
                new_height = int(width / target_ratio)

                top = (height - new_height) // 2

                cropped = img.crop(
                    (
                        0,
                        top,
                        width,
                        top + new_height
                    )
                )

            # Make sure final image is RGB
            cropped = cropped.convert("RGB")

            # --------------------------------------------------
            # SAVE JPEG
            # --------------------------------------------------

            output_path = os.path.join(
                UPLOAD_DIR,
                "converted_image.jpg"
            )

            cropped.save(
                output_path,
                "JPEG",
                quality=95
            )

            print("Image conversion successful.")
            print("Output:", output_path)
            print("Output size:", cropped.size)

            return FileResponse(
                output_path,
                media_type="image/jpeg",
                filename="converted_image.jpg"
            )

        except Exception as e:

            print("IMAGE ERROR:", str(e))

            return JSONResponse(
                status_code=500,
                content={
                    "error": f"Image processing failed: {str(e)}"
                }
            )

    # --------------------------------------------------
    # VIDEO PROCESSING
    # --------------------------------------------------

    video_types = [
        "video/mp4",
        "video/quicktime",
        "video/webm",
        "video/x-msvideo",
        "video/x-matroska"
    ]

    if file.content_type in video_types:

        try:

            print("Processing VIDEO...")

            from moviepy import VideoFileClip

            clip = VideoFileClip(input_path)

            width, height = clip.size

            current_ratio = width / height

            # --------------------------------------------------
            # CROP VIDEO
            # --------------------------------------------------

            if current_ratio > target_ratio:

                new_width = int(height * target_ratio)

                left = (width - new_width) // 2

                cropped_clip = clip.cropped(
                    x1=left,
                    y1=0,
                    x2=left + new_width,
                    y2=height
                )

            else:

                new_height = int(width / target_ratio)

                top = (height - new_height) // 2

                cropped_clip = clip.cropped(
                    x1=0,
                    y1=top,
                    x2=width,
                    y2=top + new_height
                )

            output_path = os.path.join(
                UPLOAD_DIR,
                "converted_video.mp4"
            )

            cropped_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac"
            )

            clip.close()
            cropped_clip.close()

            print("Video conversion successful.")

            return FileResponse(
                output_path,
                media_type="video/mp4",
                filename="converted_video.mp4"
            )

        except Exception as e:

            print("VIDEO ERROR:", str(e))

            return JSONResponse(
                status_code=500,
                content={
                    "error": f"Video processing failed: {str(e)}"
                }
            )

    # --------------------------------------------------
    # UNKNOWN FORMAT
    # --------------------------------------------------

    print("Unsupported file type:", file.content_type)

    return JSONResponse(
        status_code=400,
        content={
            "error": (
                f"Unsupported file type: "
                f"{file.content_type or file_ext}"
            )
        }
    )


# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )