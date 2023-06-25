import cv2
import numpy as np
import json
from shapely.geometry import LineString

file_name = "module_test\\result\\20230608_110853_bilateral"
image_name = file_name + ".png"

# Load the image
img = cv2.imread(image_name)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Thresholding
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Edge detection
edges = cv2.Canny(thresh, 50, 150, apertureSize=3)

# Hough Line Transform
lines = cv2.HoughLinesP(edges, rho=1, theta=1*np.pi/180, threshold=100, minLineLength=40, maxLineGap=10)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw lines on the original image
# Convert lines to GeoJSON format
features = []

# Convert lines to Shapely LineString instances
line_strings = []
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # for geojson
    coordinates = [[float(x1), float(y1)], [float(x2), float(y2)]]  # Convert coordinates to list
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": coordinates
        },
        "properties": {}  # You can add additional properties if needed
    }
    features.append(feature)
    
    # for shapely
    line_string = LineString(coordinates)
    line_strings.append(line_string)

# Draw contours on the original image
cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

# Convert contours to GeoJSON format
for contour in contours:
    coordinates = contour.squeeze().tolist()  # Convert contour coordinates to list
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": coordinates
        },
        "properties": {}  # You can add additional properties if needed
    }
    features.append(feature)

cv2.imwrite(file_name + "_contour.png", img)

# Create GeoJSON object
geojson_obj = {
    "type": "FeatureCollection",
    "features": features
}

# Save GeoJSON to a file
with open(file_name + "_contour.geojson", "w") as f:
    json.dump(geojson_obj, f)
