from __future__ import annotations

import base64
from functools import lru_cache

import numpy as np
from fastapi import HTTPException, status

from app.schemas.vision import (
    DishRecognitionResponse,
    VisionCandidate,
    VisionFeatures,
)

try:
    import cv2
except ImportError:  # pragma: no cover - exercised through runtime guard
    cv2 = None


class DishRecognizer:
    def recognize(self, image_base64: str) -> DishRecognitionResponse:
        image = self._decode_image(image_base64)
        features = self._extract_features(image)
        candidates = self._score_candidates(features)
        top_match = candidates[0]
        return DishRecognitionResponse(
            label=top_match.label,
            confidence=top_match.confidence,
            candidates=candidates,
            features=features,
        )

    def _decode_image(self, image_base64: str) -> np.ndarray:
        if cv2 is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OpenCV is not installed. Install project dependencies to enable dish recognition.",
            )

        try:
            payload = image_base64.split(",", 1)[-1]
            image_bytes = base64.b64decode(payload, validate=True)
        except (ValueError, TypeError) as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid base64 image payload.",
            ) from exc

        buffer = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        if image is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unable to decode image data.",
            )
        return image

    def _extract_features(self, image: np.ndarray) -> VisionFeatures:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        brightness = float(gray.mean() / 255.0)

        edges = cv2.Canny(gray, 80, 160)
        edge_density = float(np.count_nonzero(edges) / edges.size)

        green_mask = cv2.inRange(hsv, (35, 40, 40), (95, 255, 255))
        green_ratio = float(np.count_nonzero(green_mask) / green_mask.size)

        warm_mask_1 = cv2.inRange(hsv, (0, 40, 40), (25, 255, 255))
        warm_mask_2 = cv2.inRange(hsv, (160, 40, 40), (179, 255, 255))
        warm_ratio = float(
            (np.count_nonzero(warm_mask_1) + np.count_nonzero(warm_mask_2))
            / (warm_mask_1.size + warm_mask_2.size)
            * 2
        )

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, threshold = cv2.threshold(
            blurred,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )
        contours, _ = cv2.findContours(
            threshold,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )
        circularity = 0.0
        if contours:
            largest = max(contours, key=cv2.contourArea)
            perimeter = cv2.arcLength(largest, True)
            area = cv2.contourArea(largest)
            if perimeter > 0:
                circularity = float(4 * np.pi * area / (perimeter * perimeter))

        return VisionFeatures(
            brightness=round(brightness, 4),
            edge_density=round(edge_density, 4),
            circularity=round(circularity, 4),
            green_ratio=round(green_ratio, 4),
            warm_ratio=round(min(warm_ratio, 1.0), 4),
        )

    def _score_candidates(self, features: VisionFeatures) -> list[VisionCandidate]:
        scores = {
            "salad": self._clamp(
                0.2
                + 0.7 * features.green_ratio
                + 0.15 * features.edge_density
                - 0.15 * features.warm_ratio
            ),
            "soup": self._clamp(
                0.25
                + 0.55 * features.circularity
                + 0.35 * features.warm_ratio
                - 0.15 * features.edge_density
            ),
            "pizza": self._clamp(
                0.2
                + 0.45 * features.circularity
                + 0.45 * features.warm_ratio
                + 0.1 * features.edge_density
            ),
            "steak": self._clamp(
                0.15
                + 0.55 * features.warm_ratio
                + 0.2 * features.edge_density
                - 0.1 * features.green_ratio
            ),
            "dessert": self._clamp(
                0.1
                + 0.35 * features.brightness
                + 0.3 * features.circularity
                + 0.2 * features.warm_ratio
            ),
        }

        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:3]
        return [
            VisionCandidate(label=label, confidence=round(confidence, 4))
            for label, confidence in ranked
        ]

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(value, 1.0))


@lru_cache
def get_dish_recognizer() -> DishRecognizer:
    return DishRecognizer()
