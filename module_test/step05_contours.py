import cv2
import numpy as np
import random
import json
from shapely.geometry import LineString, Polygon

MIN_AREA = 3000
BINARY_THRESHOLD = 140

file_name = "module_test\\result\\3OG_stitch_before\\3OG_full"
image_name = file_name + ".png"

img = cv2.imread(image_name)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold the image to create a binary image
# _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_OTSU)
_, thresh = cv2.threshold(gray, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)

mor_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (3, 3), iterations=3)

# hierachy: [Next, Previous, First_Child, Parent]
contours, hierarchy = cv2.findContours(mor_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

# Convert lines to GeoJSON format
features = []
# Convert lines to Shapely LineString instances
line_strings = []

# Iterate over the contours and filter out inner contours
for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    if area > MIN_AREA:
        # Check if the contour has no parent (outer most contour)
        if hierarchy[0, i, 3] == -1:
            cv2.drawContours(img, [contours[i]], -1, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), 3)
            
            # Approximate the contour
            epsilon = 0.003 * cv2.arcLength(contours[i], True)
            approx = cv2.approxPolyDP(contours[i], epsilon, True)

            # Convert the contour to a Shapely LineString
            coordinates = approx.squeeze().tolist()  # Convert contour coordinates to list
            # Upside-down y-coordinates
            coordinates = [[x, img.shape[0] - y] for x, y in coordinates]
            # Convert the contour to a Shapely LineString
            # coordinates = contours[i].squeeze().tolist()  # Convert contour coordinates to list
            coordinates.append(coordinates[0]) # Close the polygon
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates
                },
                "properties": {}  # add additional properties
            }
            features.append(feature)

            # for shapely
            line_string = Polygon(coordinates)
            line_strings.append(line_string)

# cv2.imwrite(file_name + "_test0_bin.png", thresh)
cv2.imwrite(file_name + "_test0.png", img)

# Create GeoJSON object
geojson_obj = {
    "type": "FeatureCollection",
    "features": features
}

# Save GeoJSON to a file
with open(file_name + "_contour.geojson", "w") as f:
    json.dump(geojson_obj, f)