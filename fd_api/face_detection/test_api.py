import requests
import cv2
import argparse
import pprint
import urllib.request
import numpy as np

url = "http://localhost:8000/model/"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--img_url",
    default="https://www.lakedistrict.gov.uk/__data/assets/image/0031/439564/hd-rangerwalk.jpg",
    type=str,
    help="Specify image url to test api"
)


def main(config):
    resp = urllib.request.urlopen(config.img_url)
    data = resp.read()
    image = np.asarray(bytearray(data), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    img_h, img_w = image.shape[:-1]

    payload = {"url": config.img_url}
    response = requests.post(url, data=payload).json()

    for (rel_x, rel_y, rel_w, rel_h) in response["detections"]:
        start_x = int(rel_x * img_w)
        start_y = int(rel_y * img_h)
        end_x = start_x + int(img_w * rel_w)
        end_y = start_y + int(img_h * rel_h)
        cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

    cv2.imshow("Test image:", image)
    cv2.waitKey(0)


if __name__ == "__main__":
    config = parser.parse_args()
    pprint.pprint(config)
    main(config)
