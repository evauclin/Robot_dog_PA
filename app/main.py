from Face_rec import images_process, easy_face_reco

from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import cv2 as cv
import uuid
from logger import log
from distance_toolbox import (
    object_detector,
    focal_length_finder,
    distance_finder,
    KNOWN_DISTANCE,
    PERSON_WIDTH,
)


# reading the reference image from dir
ref_person = cv.imread("ReferenceImages/test.jpg")
log.info("Reference image loaded successfully")


person_data = object_detector(ref_person)
person_width_in_rf = person_data[0][1]
log.info("Person width in reference image: {}".format(person_width_in_rf))


# finding focal length
focal_person = focal_length_finder(KNOWN_DISTANCE, PERSON_WIDTH, person_width_in_rf)
log.info("Focal length found: {}".format(focal_person))


app = FastAPI()

# Configure a directory to save the uploaded images
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

known_face_names, known_face_encodings = images_process("images")
log.info("Images source loaded successfully")


@app.get("/")
async def home():
    return {"message": "Welcome to the home page"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    if not image:
        raise HTTPException(status_code=400, detail="No image uploaded")

    if not allowed_file(image.filename):
        print(image.filename)
        raise HTTPException(status_code=400, detail="Only PNG images allowed")

    try:
        image.filename = f"{uuid.uuid4()}.jpeg"
        content = await image.read()
        with open(UPLOAD_FOLDER / image.filename, "wb") as f:
            f.write(content)
            image_convert = cv.imread(f"{UPLOAD_FOLDER}/{image.filename}")
            try:
                data = object_detector(image_convert)
                if data[0][0] == "person":
                    distance = distance_finder(focal_person, PERSON_WIDTH, data[0][1])
                    name = easy_face_reco(
                        image_convert, known_face_encodings, known_face_names
                    )
                    if distance > 400 and (name != None or name != "Unknown"):
                        log.info(f"Person detected at {distance} cm with name {name}")
                        return {
                            "name": name,
                            "distance": distance,
                            "message": "Go",
                        }

                else:
                    log.info("No person detected or person is too close")
                    return {
                        "name": None,
                        "distance": None,
                        "message": None,
                    }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")
