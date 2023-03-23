"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import os
from PIL import Image
import datetime
import cv2
import numpy as np

import torch
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return render_template("fail.html")

        img_bytes = file.read()
        im = Image.open(io.BytesIO(img_bytes))
        padded_img = np.array(im)
        # padded_img = [padded_img]
        old_image_height, old_image_width, channels = padded_img.shape
        # print(old_image_width)
        new_image_height = old_image_height
        new_image_width = old_image_width + 600
        color = (255,255,255)
        result = np.full((new_image_height,new_image_width, channels), color, dtype=np.uint8)
        x_center = (new_image_width - old_image_width) // 2
        y_center = (new_image_height - old_image_height) // 2

# copy img image into center of result image
        result[y_center:y_center+old_image_height, 
        x_center:x_center+old_image_width] = padded_img
        pil_image = Image.fromarray(result)
        results = model([result])

        results.render()  # updates results.imgs with boxes and labels
        now_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
        img_savename = f"static/{now_time}.png"
        Image.fromarray(results.ims[0]).save(img_savename)
        return redirect(img_savename)

    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    # model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # force_reload = recache latest code
    model = torch.hub.load('ultralytics/yolov5','custom', path='C:/Users/garvi/OneDrive/Desktop/YOLO Training/yolov5/run_120/weights/best.pt')
    model.eval()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat