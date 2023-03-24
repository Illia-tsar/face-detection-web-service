import cv2
import urllib.request
import numpy as np
from django.http import JsonResponse
from .apps import FaceDetectionConfig
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def detect(request):
    data = {"success": False}

    if request.method == "POST":
        url = request.POST.get("url", None)

        if url is None:
            data["error"] = "No URL provided."
            return JsonResponse(data)

        image = load_image(url)
        image = image[:, :, ::-1]
        img_h, img_w = image.shape[:-1]

        face_detection_results = FaceDetectionConfig.predictor.process(image)

        rects = []
        for face in face_detection_results.detections:
            face_data = face.location_data.relative_bounding_box
            rel_x, rel_y, rel_w, rel_h, = face_data.xmin, face_data.ymin, face_data.width, face_data.height
            abs_x, abs_y, abs_w, abs_h = int(rel_x * img_w), int(rel_y * img_h), int(rel_w * img_w), int(rel_h * img_h)
            rects.append((abs_x, abs_y, abs_w, abs_h))

        data.update({
            "detections": rects,
            "success": True
        })

    return JsonResponse(data)


def load_image(url):
    resp = urllib.request.urlopen(url)
    data = resp.read()
    image = np.asarray(bytearray(data), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image
