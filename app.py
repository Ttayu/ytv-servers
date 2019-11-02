import os
from pathlib import Path

from flask import Flask, json, jsonify, make_response, redirect, request
from watson_developer_cloud import VisualRecognitionV3

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


class IBM:
    api_key = os.environ["IBM_API_KEY"]
    visual_recognition = VisualRecognitionV3("2019-11-02", iam_apikey=api_key)

    @classmethod
    def classify_best_cool(cls, images_file):
        result = cls.classify(images_file)
        return cls.get_score_of_best_cool(result)

    @classmethod
    def classify(cls, images_file):
        with open(images_file, "rb") as f:
            result = cls.visual_recognition.classify(
                f, threshold="0.0", classifier_ids="DefaultCustomModel_1445172307"
            ).get_result()
        return result

    @classmethod
    def get_score_of_best_cool(cls, result):
        classifiers = result["images"][0]["classifiers"]
        fashion_classes = classifiers[0]["classes"]
        score = None
        for element in fashion_classes:
            if element["class"] == "class4":
                score = element["score"]
        if score is None:
            raise ValueError("not included class4")
        return score


@app.route("/", methods=["POST"])
def index():
    return request.data


def get_image(data):
    image_path = Path(data["image_path"])
    if not Path(image_path).exists():
        raise FileNotFoundError(f"file not found: {image_path}")
        # return redirect("/error")
    score = IBM.classify_best_cool(image_path)
    return {"id": data["id"], "score": score}


@app.route("/test_image", methods=["POST"])
def post_image():
    data = request.get_json()
    if not data:
        raise ValueError(f"data not found: {data}")
        # return redirect("/error")
    return jsonify(get_image(data))


@app.route("/test_images", methods=["POST"])
def post_images():
    data = request.get_json()
    print(data)
    responses = []
    for datum in data:
        responses.append(get_image(datum))
    return jsonify(responses)


@app.route("/error")
def error():
    return "error"


if __name__ == "__main__":
    app.debug = True
    app.run()
