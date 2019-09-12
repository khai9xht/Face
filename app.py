# TODO: test the API, both search and append database
# TODO: combine with front-end to produce a simple version

import os, glob, sys
import time

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin

import numpy as np
import pandas as pd

from backend.core.descriptors.insightface import InsightFaceDetector, InsightFaceFilter, InsightFaceDescriptor
from backend.core.searchers.knn_classifier import KNNClassifier
from backend import config, utils, database

app = Flask(__name__, static_url_path="")
cors = CORS(app, resources=config.CORS_RESOURCES)

@app.route("/add", methods=["POST"])
def add():
    content = request.get_json()
    image = utils.base64_to_image(content["data"])
    email = content["email"]

    bboxes, points_list = detector.detect(image)
    faces = filter.filter(image, bboxes, points_list)
    embeddings = descriptor.process(faces)

    areas = bboxes[:, 2:-1] - bboxes[:, :2]
    areas = areas[:, 0] * areas[:, 1]
    largest_bbox = np.argmax(areas)
    
    data = np.append([email], embeddings[largest_bbox])
    database_manager.append_database(data)
    classifier.init_data(database_manager.get_database())
    return jsonify({"result": True})

@app.route("/search", methods=["POST"])
def search():
    content = request.get_json()
    image = utils.base64_to_image(content["data"])
    
    bboxes, points_list = detector.detect(image)
    faces = filter.filter(image, bboxes, points_list)
    embeddings = descriptor.process(faces)
    face_ids, scores = classifier.predict(embeddings)

    # visualize
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # h, w, _ = image.shape
    # for point in content["landMarks"]:
    #     x, y = int(point["newX"]*w), int(point["newY"]*h)
    #     cv2.circle(image, (x, y), 3, (255, 0, 0))
    # cv2.imwrite("image.jpg", image)

    return jsonify({"id": face_ids[0, 0], "score": scores[0]})

@app.route("/reset", methods=["POST"])
def reset():
    database_manager.empty_database()
    classifier.init_data(database_manager.get_database())
    return jsonify({"result": True})

@app.route("/", methods=["GET"])
def main():
    try:
        return send_file("static/views/webcamFaceDetection.html")
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    database_manager = database.DatabaseManager(config.DATABASE_PATH)
    detector = InsightFaceDetector()
    filter = InsightFaceFilter()
    descriptor = InsightFaceDescriptor()
    classifier = KNNClassifier()

    classifier.init_data(database_manager.get_database())
    app.run(host="0.0.0.0", port=8888, threaded=False)
