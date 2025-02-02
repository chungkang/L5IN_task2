import cv2
import random
import json
from shapely.geometry import Polygon

# modify file_name to test different images

MIN_AREA = 3000
BINARY_THRESHOLD = 135
APPROX_CONTOUR = 0.001

file_name = "module_test\\result\\4OG_full_color"
image_name = file_name + ".png"

img = cv2.imread(image_name)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold the image to create a binary image
# _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_OTSU)
_, thresh = cv2.threshold(gray, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)

mor_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (3, 3), iterations=3)

# hierachy: [Next, Previous, First_Child, Parent]
contours, hierarchy = cv2.findContours(mor_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_L1)
# mode RETR_LIST: retrieves all of the contours without establishing any hierarchical relationships
# mothod CHAIN_APPROX_TC89_L1: advanced contour approximation methods that use the Teh-Chin chain approximation algorithm

# Convert lines to GeoJSON format
line_features = []
polygon_features = []
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
            epsilon = APPROX_CONTOUR * cv2.arcLength(contours[i], True)
            approx = cv2.approxPolyDP(contours[i], epsilon, True)

            # Convert the contour to a Shapely LineString
            coordinates = approx.squeeze().tolist()  # Convert contour coordinates to list
            # Upside-down y-coordinates
            coordinates = [[x, img.shape[0] - y] for x, y in coordinates]
            # Convert the contour to a Shapely LineString
            # coordinates = contours[i].squeeze().tolist()  # Convert contour coordinates to list
            coordinates.append(coordinates[0]) # Close the polygon
            polygon_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coordinates]
                },
                "properties": {}  # add additional properties
            }
            polygon_features.append(polygon_feature)

            line_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates
                },
                "properties": {}  # add additional properties
            }
            line_features.append(line_feature)

            # for shapely
            line_string = Polygon(coordinates)
            line_strings.append(line_string)

cv2.imwrite(file_name + "_test0_bin.png", thresh)
cv2.imwrite(file_name + "_test0.png", img)

# Create GeoJSON object
geojson_line_obj = {
    "type": "FeatureCollection",
    "features": line_features
}
geojson_polygon_obj = {
    "type": "FeatureCollection",
    "features": polygon_features
}

# Save GeoJSON to a file
with open(file_name + "_line.geojson", "w") as f:
    json.dump(geojson_line_obj, f)
with open(file_name + "_polygon.geojson", "w") as f:
    json.dump(geojson_polygon_obj, f)
