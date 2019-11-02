from flask import json

from app import app


def test_image():
    body = {"id": 0, "image_path": "./test.jpg", "date": "2019-09-12", "user_id": 0}
    response = app.test_client().post(
        "/test_image", data=json.dumps(body), content_type="application/json"
    )

    data = json.loads(response.get_data(as_text=True))
    print(data)

    assert response.status_code == 200
    assert data["id"] == 0
    assert data["score"] == 0.748


def test_images():
    body = [
        {"id": 0, "image_path": "./test.jpg", "date": "2019-09-12", "user_id": 0},
        {"id": 1, "image_path": "./test.jpg", "date": "2019-07-12", "user_id": 1},
        {"id": 2, "image_path": "./test.jpg", "date": "2019-06-12", "user_id": 2},
        {"id": 3, "image_path": "./test.jpg", "date": "2019-09-22", "user_id": 3},
    ]
    response = app.test_client().post(
        "/test_images", data=json.dumps(body), content_type="application/json"
    )

    data = json.loads(response.get_data(as_text=True))
    print(data)

    assert response.status_code == 200
    assert len(data) == len(body)
