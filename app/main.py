import fileinput
from Face_rec import images_process, easy_face_reco

from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import cv2 as cv
import uuid
from pydantic import BaseModel

KNOWN_DISTANCE = 30  # inch
PERSON_WIDTH = 16  # inch

# Object detector constant
CONFIDENCE_THRESHOLD = 0.4
NMS_THRESHOLD = 0.3

# colors for object detected
COLORS = [(255, 0, 0), (255, 0, 255), (0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
# defining fonts
FONTS = cv.FONT_HERSHEY_COMPLEX

# getting class names from classes.txt file
class_names = []
with open("classes.txt", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]
#  setttng up opencv net
yoloNet = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')

yoloNet.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
yoloNet.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

model = cv.dnn_DetectionModel(yoloNet)
model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)


# object detector funciton /method
def object_detector(image):
    classes, scores, boxes = model.detect(image, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    # creating empty list to add objects data
    data_list = []
    for (classid, score, box) in zip(classes, scores, boxes):
        # define color of each, object based on its class id
        color = COLORS[int(classid) % len(COLORS)]

        label = "%s : %f" % (class_names[classid], score)

        # draw rectangle on and label on object
        cv.rectangle(image, box, color, 2)
        cv.putText(image, label, (box[0], box[1] - 14), FONTS, 0.5, color, 2)

        # getting the data
        # 1: class name  2: object width in pixels, 3: position where have to draw text(distance)
        if classid == 0:  # person class id
            data_list.append([class_names[classid], box[2], (box[0], box[1] - 2)])
        # if you want inclulde more classes then you have to simply add more [elif] statements here
        # returning list containing the object data.
    return data_list


def focal_length_finder(measured_distance, real_width, width_in_rf):
    focal_length = (width_in_rf * measured_distance) / real_width

    return focal_length


# distance finder function
def distance_finder(focal_length, real_object_width, width_in_frmae):
    distance = (real_object_width * focal_length) / width_in_frmae
    return distance


# reading the reference image from dir
ref_person = cv.imread("ReferenceImages/test.jpg")
# ref_mobile = cv.imread('ReferenceImages/image4.png')

# mobile_data = object_detector(ref_mobile)
# mobile_width_in_rf = mobile_data[1][1]

person_data = object_detector(ref_person)
person_width_in_rf = person_data[0][1]
print(person_width_in_rf)

print(f"Person width in pixels : {person_width_in_rf}")

# finding focal length
focal_person = focal_length_finder(KNOWN_DISTANCE, PERSON_WIDTH, person_width_in_rf)


app = FastAPI()

# Configure a directory to save the uploaded images
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

args = "/images"
known_face_names,known_face_encodings = images_process(args)

@app.get('/')
async def home():
    return {"message": "Welcome to the home page"}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post('/upload')
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
            data = object_detector(image_convert)
            if data[0][0] == 'person':
                distance = distance_finder(focal_person, PERSON_WIDTH, data[0][1])
                name = easy_face_reco(image_convert, known_face_encodings, known_face_names)
                if distance > 1 and (name != None or name != "Unknown"):
                    return {"message": "Go"}
                else:
                    return {"message": "Stop"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")
