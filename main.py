#!/usr/bin/env python
import io
import time

from doggydo import doggy
from doggydo.doggy import DoggyOrder
import requests
import cv2

CURRENT_URL_VM = "http://34.240.56.31:80/upload"

def main():
    # Init vars and load models here

    if not doggy.start():
        raise RuntimeError("Doggy did not start!")
    else:
        print("Doggy started.")

    new_detection = DoggyOrder.NONE
    URL_VM = CURRENT_URL_VM
    headers = {"accept": "application/json"}

    # Main event loop
    with doggy.video.camera as camera:
        doggy.video.setup()
        stream = io.BytesIO()
        camera.start()
        for _ in range(1000):
            camera.capture_file(stream, format="jpeg")
            frame = doggy.get_camera_frame(stream)
            if frame is not None:
                bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                cv2.imwrite("frame.jpg", bgr_frame)
                files = {"image": open("frame.jpg", "rb")}
                response = requests.post(
                    URL_VM, files=files, headers=headers, timeout=5
                )
                current_order = 1 if response.json()["message"] == "Go" else -1

                if current_order != DoggyOrder.NONE and doggy.ready():
                    doggy.do(current_order)
            else:
                print("I'll sleep to wait a little.")
                time.sleep(1)


if __name__ == "__main__":
    main()
