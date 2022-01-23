# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 08:48:22 2021

@author: DMZ-Admin

source article: https://www.sicara.ai/blog/object-detection-template-matching
source code: https://gist.github.com/jrovani/2de8c25a040dc3ea529a1b6324fb30be#gistcomment-3652497
"""

import cv2
import numpy as np

DEFAULT_TEMPLATE_MATCHING_THRESHOLD = 0.57 # 0.6-7 works well for EG2, 0.57-0.6 works fine for EG1
class Template:
     def __init__(self, image_path, label, color, matching_threshold=DEFAULT_TEMPLATE_MATCHING_THRESHOLD):
        self.image_path = image_path
        self.label = label
        self.color = color
        self.template = cv2.imread(image_path)
        self.template_height, self.template_width = self.template.shape[:2]
        self.matching_threshold = matching_threshold
image = cv2.imread("IMG_1243.JPG") 
templates = [
    Template(image_path="Temp.JPG", label="1", color=(0, 255, 255)),
    Template(image_path="emergency.JPG", label="2", color=(140, 120, 42)),
    Template(image_path="emergency_1243.JPG", label="3", color=(255, 0, 0)),
    Template(image_path="exitD.JPG", label="4", color=(255, 191, 255)),
    Template(image_path="exitD2.JPG", label="5", color=(255, 191, 255)),
    Template(image_path="exitD_1243.JPG", label="6", color=(0, 0, 255)),
    Template(image_path="exitU.JPG", label="7", color=(0, 0, 255)),
    Template(image_path="exitU2.JPG", label="8", color=(0, 0, 255)),
    Template(image_path="exitU_1243.JPG", label="9", color=(0, 255, 0)),
    Template(image_path="exitL.JPG", label="10", color=(0, 255, 0)),
    Template(image_path="exitR.JPG", label="11", color=(0, 255, 60)),
    Template(image_path="firstaid.JPG", label="12", color=(0, 0, 255)),
]

detections = []
for template in templates:
    template_matching = cv2.matchTemplate(
        template.template, image, cv2.TM_CCOEFF_NORMED
    )

    match_locations = np.where(template_matching >= template.matching_threshold)

    for (x, y) in zip(match_locations[1], match_locations[0]):
        match = {
            "TOP_LEFT_X": x,
            "TOP_LEFT_Y": y,
            "BOTTOM_RIGHT_X": x + template.template_width,
            "BOTTOM_RIGHT_Y": y + template.template_height,
            "MATCH_VALUE": template_matching[y, x],
            "LABEL": template.label,
            "COLOR": template.color
        }      
        detections.append(match)

def compute_iou(
    boxA, boxB
):
    xA = max(boxA["TOP_LEFT_X"], boxB["TOP_LEFT_X"])
    yA = max(boxA["TOP_LEFT_Y"], boxB["TOP_LEFT_Y"])
    xB = min(boxA["BOTTOM_RIGHT_X"], boxB["BOTTOM_RIGHT_X"])
    yB = min(boxA["BOTTOM_RIGHT_Y"], boxB["BOTTOM_RIGHT_Y"])
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    boxAArea = (boxA["BOTTOM_RIGHT_X"] - boxA["TOP_LEFT_X"] + 1)*(boxA["BOTTOM_RIGHT_Y"] - boxA["TOP_LEFT_Y"] + 1)
    boxBArea = (boxB["BOTTOM_RIGHT_X"] - boxB["TOP_LEFT_X"] + 1)*(boxB["BOTTOM_RIGHT_Y"] - boxB["TOP_LEFT_Y"] + 1)
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

def non_max_suppression(
    objects,
    non_max_suppression_threshold=0.5,
    score_key="MATCH_VALUE",
):
    sorted_objects = sorted(objects, key=lambda obj: obj[score_key], reverse=True)
    filtered_objects = []
    for object_ in sorted_objects:
        overlap_found = False
        for filtered_object in filtered_objects:
            iou = compute_iou(object_, filtered_object)
            if iou > non_max_suppression_threshold:
                overlap_found = True
                break
        if not overlap_found:
            filtered_objects.append(object_)
    return filtered_objects
NMS_THRESHOLD = 0.2
detections = non_max_suppression(detections, non_max_suppression_threshold=NMS_THRESHOLD) 
image_with_detections = image.copy()

for detection in detections:
    cv2.rectangle(
        image_with_detections,
        (detection["TOP_LEFT_X"], detection["TOP_LEFT_Y"]),
        (detection["BOTTOM_RIGHT_X"], detection["BOTTOM_RIGHT_Y"]),
        detection["COLOR"],
        2,
    )
    """
    cv2.putText(
        image_with_detections,
        f"{detection['LABEL']} - {detection['MATCH_VALUE']}",
        (detection["TOP_LEFT_X"] + 2, detection["TOP_LEFT_Y"] + 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        detection["COLOR"],
        1,
        cv2.LINE_AA,
    )
    """
cv2.imwrite('IMG_1243_detected.jpeg', image_with_detections)