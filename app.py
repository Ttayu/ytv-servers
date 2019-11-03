import io
import os
from urllib.request import urlopen

from flask import Flask, jsonify, request
from watson_developer_cloud import VisualRecognitionV3

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

IMAGE_DIR = f"{os.environ['HOST_NAME']}assets/images/resized"


class IBM:
    api_key = os.environ["IBM_API_KEY"]
    visual_recognition = VisualRecognitionV3("2019-11-02", iam_apikey=api_key)

    @classmethod
    def classify_fashion_sense(cls, images_file):
        result = cls._classify(images_file)
        return cls._get_max_class(result)

    @classmethod
    def _classify(cls, file_name):
        print(f"{IMAGE_DIR}/new_{file_name}")
        url = urlopen(f"{IMAGE_DIR}/new_{file_name}")
        file = io.BytesIO(url.read())
        result = cls.visual_recognition.classify(
            file, threshold="0.0", classifier_ids="DefaultCustomModel_1445172307"
        ).get_result()
        return result

    @classmethod
    def _get_max_class(cls, result):
        classifiers = result["images"][0]["classifiers"]
        fashion_classes = classifiers[0]["classes"]
        max_score = 0
        fashion_sense = None
        for element in fashion_classes:
            if max_score < element["score"]:
                max_score = element["score"]
                fashion_sense = element["class"]
        if fashion_sense is None:
            raise ValueError("not classified fashion sense.")
        return fashion_sense, max_score


@app.route("/", methods=["POST"])
def index():
    return request.data


def get_image(data):
    file_name = data["file_name"]
    fashion_sense, score = IBM.classify_fashion_sense(file_name)
    return {"id": data["id"], "class": fashion_sense, "score": score}


@app.route("/test_image", methods=["POST"])
def post_image():
    data = request.get_json()
    if not data:
        raise ValueError(f"data not found: {data}")
    return jsonify(get_image(data))


@app.route("/test_images", methods=["POST"])
def post_images():
    data = request.get_json()
    responses = []
    for datum in data:
        responses.append(get_image(datum))
    return jsonify(responses)


if __name__ == "__main__":
    app.debug = True
    app.run()
