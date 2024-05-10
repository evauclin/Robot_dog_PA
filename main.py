#!/usr/bin/env python
import io
import time

from typing import Any, List, Optional
from doggydo import doggy
from doggydo.doggy import DoggyOrder
import requests


def clamp_detections(detections: List[DoggyOrder], limit: int = 5) -> List[DoggyOrder]:
    """Clamp the number of detections to not exceed limit"""
    while len(detections) > limit:
        detections.pop(0)
    return detections


def get_order_given(last_detections: List[DoggyOrder]) -> DoggyOrder:
    """Returns the order to give as regard of all the detections given"""
    for order in DoggyOrder:
        if all(order == detection for detection in last_detections):
            return order
    return DoggyOrder.NONE




def main():
    # Init vars and load models here
    last_detections = []


    if not doggy.start():
        raise RuntimeError("Doggy did not start!")
    else:
        print("Doggy started.")

    new_detection = DoggyOrder.NONE
    url_vm = "http://18.201.12.192:80/upload"
    headers = {"accept": "application/json"}

    # Main event loop
    with doggy.video.camera as camera:
        doggy.video.setup()
        stream = io.BytesIO()
        for _ in camera.capture_file(stream, 'jpeg'):
            frame = doggy.get_camera_frame(stream)
            if frame is not None:
                print(frame)
                files = {'image':frame}
                response = requests.post(url_vm, files=files, headers=headers)
                name = response.json()["name"]
                distance = response.json()["distance"]
                current_order = 1 if response.json()["message"] == "Go" else -1
                print(new_detection)
                print(current_order)

                if current_order != DoggyOrder.NONE and doggy.ready():
                    last_detections = []
                    doggy.do(current_order)
            else:
                print("I'll sleep to wait a little.")
                time.sleep(1)


if __name__ == "__main__":
    main()
