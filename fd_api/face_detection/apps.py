from django.apps import AppConfig
import mediapipe as mp


class FaceDetectionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "face_detection"

    predictor = mp.solutions.face_detection.FaceDetection(
        model_selection=1,
        min_detection_confidence=.5
    )
