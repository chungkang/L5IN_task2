# https://www.sicara.ai/blog/object-detection-template-matching
# https://gist.github.com/jrovani/2de8c25a040dc3ea529a1b6324fb30be#gistcomment-3652497

import cv2
import numpy as np

DEFAULT_TEMPLATE_MATCHING_THRESHOLD = 0.65
file_name = "module_test\\result\\image2-2_crop_bin"
image_name = file_name + ".png"

class Template:
     def __init__(self, image_path, label, color, matching_threshold=DEFAULT_TEMPLATE_MATCHING_THRESHOLD):
        self.image_path = image_path
        self.label = label
        self.color = color
        self.template = cv2.imread(image_path)
        self.template_height, self.template_width = self.template.shape[:2]
        self.matching_threshold = matching_threshold

image = cv2.imread(image_name)

templates = [
    Template(image_path = file_name + '_template1.png', label="1", color=(0, 255, 255)),
    Template(image_path = file_name + '_template2.png', label="2", color=(140, 120, 42)),
    # Template(image_path = file_name + '_template3.png', label="3", color=(0, 200, 50)),
    # Template(image_path = file_name + '_template4.png', label="4", color=(140, 250, 0)),
    # Template(image_path = file_name + '_template5.png', label="5", color=(140, 0, 100)),
    # Template(image_path = file_name + '_template6.png', label="6", color=(255, 191, 255)),
]

# save detected templates
detections = []

# Define a range of rotation angles
angles = np.arange(0,360,5)
scales = np.arange(0.7, 1.3, 0.05)

# for mirrored template
flip_yn = [0,1]

for template in templates:
    for flip in flip_yn:
        if flip == 1:
            template.template = cv2.flip(template.template, 1)

        # Loop over all rotation angles
        for angle in angles:
            # Loop over all scales
            for scale in scales:
                # Get image size
                h, w = template.template.shape[:2]
                # Calculate rotation matrix
                M = cv2.getRotationMatrix2D((w/2, h/2), angle, scale)
                # Apply rotation and scaling to image
                img_rotated_scaled = cv2.warpAffine(template.template, M, (w, h))

                # template_matching = cv2.matchTemplate(template_hsv, image, cv2.TM_CCORR_NORMED)
                template_matching = cv2.matchTemplate(img_rotated_scaled, image, cv2.TM_CCOEFF_NORMED)
                match_locations = np.where(template_matching >= template.matching_threshold)
                for (x, y) in zip(match_locations[1], match_locations[0]):
                    match = {
                        "TOP_LEFT_X": x,
                        "TOP_LEFT_Y": y,
                        "CENTER_X": int(x + template.template_width/2),
                        "CENTER_Y": int(y + template.template_height/2),
                        "BOTTOM_RIGHT_X": x + template.template_width,
                        "BOTTOM_RIGHT_Y": y + template.template_height,
                        "MATCH_VALUE": template_matching[y, x],
                        "LABEL": template.label,
                        "COLOR": template.color,
                        "HEIGHT": h,
                        "WIDTH": w,
                        "ANGLE": int(angle),
                        "SCALE": scale,
                    }      
                    detections.append(match)

def compute_iou(boxA, boxB):
    xA = max(boxA["TOP_LEFT_X"], boxB["TOP_LEFT_X"])
    yA = max(boxA["TOP_LEFT_Y"], boxB["TOP_LEFT_Y"])
    xB = min(boxA["BOTTOM_RIGHT_X"], boxB["BOTTOM_RIGHT_X"])
    yB = min(boxA["BOTTOM_RIGHT_Y"], boxB["BOTTOM_RIGHT_Y"])
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    boxAArea = (boxA["BOTTOM_RIGHT_X"] - boxA["TOP_LEFT_X"] + 1)*(boxA["BOTTOM_RIGHT_Y"] - boxA["TOP_LEFT_Y"] + 1)
    boxBArea = (boxB["BOTTOM_RIGHT_X"] - boxB["TOP_LEFT_X"] + 1)*(boxB["BOTTOM_RIGHT_Y"] - boxB["TOP_LEFT_Y"] + 1)
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

def non_max_suppression(objects, threshold=0.5, score_key="MATCH_VALUE"):
    # Sort objects in descending order by score
    objects = sorted(objects, key=lambda obj: obj[score_key], reverse=True)
    # Initialize an empty list to hold filtered objects
    filtered_objects = []
    # Iterate over each object
    for obj in objects:
        # Check if there is any overlap with previously filtered objects
        overlap = any(compute_iou(obj, filtered_obj) > threshold for filtered_obj in filtered_objects)
        # If there is no overlap, add the object to the list of filtered objects
        if not overlap:
            filtered_objects.append(obj)
    # Return the filtered objects
    return filtered_objects    

NMS_THRESHOLD = 0.2
detections = non_max_suppression(detections, threshold=NMS_THRESHOLD) 
image_with_detections_box = image.copy()
image_with_detections = image.copy()

for detection in detections:
    # Define the rectangle parameters
    center = (detection["CENTER_X"], detection["CENTER_Y"])
    # size = (detection["HEIGHT"], detection["WIDTH"])
    size = (detection["HEIGHT"]+15, detection["WIDTH"]+15)
    angle = detection["ANGLE"]

    # Calculate the rectangle vertices
    rect = cv2.boxPoints((center, size, angle))
    rect = np.int0(rect)
    color = detection["COLOR"]
    # Draw the rectangle on the image
    cv2.drawContours(image_with_detections_box, [rect], 0, color, 3)
    # fill rectangle with white color
    cv2.fillConvexPoly(image_with_detections, rect, (255, 255, 255))

cv2.imwrite( file_name + "_result_box.png", image_with_detections_box)
cv2.imwrite( file_name + "_result.png", image_with_detections)
