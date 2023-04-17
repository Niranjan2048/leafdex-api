import flask
from flask import request, jsonify, Response
import json
import base64
import requests
from time import sleep


API_KEY = "SvVQtc0lDhpQRYqEEXqo4DfnL1FZrkdA6Vpyf7GGXmwFVhMrno"    # Ask for your API key: https://web.plant.id/api-access-request/


def encode_file(file_name):
    with open(file_name, "rb") as file:
        return base64.b64encode(file.read()).decode("ascii")


def identify_plant(file_names):
    params = {
        "images": [encode_file(img) for img in file_names],
        }

    headers = {
        "Content-Type": "application/json",
        "Api-Key": API_KEY,
        }

    response = requests.post("https://api.plant.id/v2/enqueue_identification",
                             json=params,
                             headers=headers).json()

    return get_result(response["id"])


def get_result(identification_id):
    params = {
        "plant_language": "en",
        "plant_details": ["common_names",
                          "edible_parts",
                          "gbif_id",
                          "name_authority",
                          "propagation_methods",
                          "synonyms",
                          "taxonomy",
                          "url",
                          "wiki_description",
                          "wiki_image",
                          ],
        }

    headers = {
        "Content-Type": "application/json",
        "Api-Key": API_KEY,
        }

    endpoint = "https://api.plant.id/v2/get_identification_result/"

    while True:
        print("Waiting for suggestions...")
        sleep(5)
        response = requests.post(endpoint + str(identification_id),
                                 json=params,
                                 headers=headers).json()
        if response["suggestions"] is not None:
            return response

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/v1/leaf', methods=['POST'])
def get_leaf():
    if request.method == 'POST':
        data = request.get_json()
        img = data['img']
        img.save("img.jpg")
    res = identify_plant([img])
    
    return res["suggestions"][0]["plant_details"]["common_names"]
if __name__ == "__main__":
    app.run(host='0.0.0.0')

