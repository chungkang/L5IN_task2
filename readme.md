# L5IN task2: Vectorized Floor Plan generation from image of Emergency Evacuation Plan

Input source: images of Emergency Evacuation Plan
Expected Result: geospatial format (shp, geojson) of vectorized floor plan

# Main Logic
## 1. Take photo of Emergency Evacuation Plan
Better to have well projected, high resolution and low glare/reflected images

|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/af151ea8-a216-4d9d-b34b-45cb1af11b68)|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/ab47eec3-cce6-48bf-8426-6607a9c16dbe)|
|-|-|
|well projected|With reflection and projected from side view

## 2. Reproject (Rectify) image
If is not well projected, reproject(rectify) image
Compute Vanishing points using RANSAC and rectify the image

Reference: Image-Rectification of chsasank from github repository
https://github.com/chsasank/Image-Rectification
based on the paper: Chaudhury, Krishnendu, Stephen DiVerdi, and Sergey Ioffe. "Auto-rectification of user photos." 2014 IEEE International Conference on Image Processing (ICIP). IEEE, 2014.
https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/42532.pdf

|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/645795a5-37be-4b86-92b5-9e751eaf5a79)|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/9b49c96b-2154-4eba-8f34-d0d827f61b28)|
|-|-|
|Projected from side view|Reprojected/rectified image|

crop the part which is needed

## 3. Filter the image to reduce noise
Reduce noise from image with bilateral filter of OpenCV

|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/59590f39-a5ef-4bb3-bc4b-bdcc5c751614)|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/ebc90368-9c1d-4549-9fe6-c0571821a2d7)|
|-|-|
|Before filtering noise|After filtering noise|

Adjust following parameters for preserving the edges of an image while reducing noise
Diameter: The diameter of each pixel neighborhood used during filtering. It controls the size of the neighborhood. Larger values o result in stronger smoothing.
sigmaColor: The standard deviation of the color space. It controls how different colors are considered to be neighboring pixels. Larger values of sigmaColor result in more colors being included in the filtering process.
sigmaSpace: The standard deviation of the coordinate space. It controls the spatial extent of the filter. Larger values of sigmaSpace result in pixels farther apart in the spatial domain being considered as neighbors.

## 4. Remove symbols from image with Feature matching
Reduce symbols on emergency evacuation plan
Feature matching method of OpenCV
Feature matching steps:
Clustering: MEANSHIFT => divide image
Feature Extraction: SIFT => extract feature points from divided image
Feature Matching: FLANN => match feature points between image and symbol
Homography calculation: RANSAC => calculate offset, rotation, scale of symbol on image

Symbols should be cropped from each image

|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/be492029-a32e-4c76-8c96-e956ae1418db)|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/4411b11f-5b15-441f-8bc6-a9e5e5316675)|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/d221f2e4-0afe-408e-a4e8-6cbc796c5669)|
|-|-|-|
|Before removing symbols|After removing symbols|Cropped symbols from image|

Adjust following parameters for reducing symbols from the image
MIN_MATCH_COUNT: This parameter determines the minimum number of matches required for a template image to be considered a valid match. For perspective Transform, more than 4 points are needed.
MATCH_DISTANCE: This parameter is used in the Lowe's ratio test during feature matching. It controls the threshold for accepting matches based on their distance ratio.
NUMBER_OF_TEMPLATES: This parameter specifies the number of template images to be processed.
PAD: This parameter defines the padding value used when generating the destination points for perspective transformation.

Reference: https://stackoverflow.com/questions/42938149/opencv-feature-matching-multiple-objects?noredirect=1&lq=1

## 5. Stitch images
If it is not covering whole floor, stitch images to make single image to make single floor

Should be stitched one by one

|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/fe67683b-00c6-4d7d-a917-c47afc809e9c)|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/fed1ea65-53ac-46d7-98d0-47c4d46d3ded)|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/020109fb-f146-416a-ade6-0239246f365c)|
|-|-|-|
|3OG part1|3OG part2|3OG part 3|

|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/efb0bf38-b009-4dbc-86b0-6d37cffcab62)|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/112d9bd8-12aa-42e0-8df0-8b316f5268bc)|
|-|-|
|3OG part1 + part2|3OG full floor|

Reference: https://gist.github.com/tigercosmos/90a5664a3b698dc9a4c72bc0fcbd21f4

## 6. Extract contours of wall
MIN_AREA: This parameter defines the minimum contour area required for an object to be considered valid. Contours with an area smaller than this threshold will be filtered out.
BINARY_THRESHOLD: This parameter sets the threshold value for creating a binary image from the grayscale image. Pixels with intensity values below this threshold will be set to 0, and pixels above or equal to the threshold will be set to 255.
APPROX_CONTOUR: This parameter controls the level of approximation when converting contours using the cv2.approxPolyDP() function. It specifies the percentage of the contour perimeter that should be approximated.

Logic steps: Binarize -> extract contour -> straighten contour -> save as geojson

|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/26b66b0a-62af-4d9a-bf95-60f3e143760d)|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/8f4726c8-4241-4ffc-bebf-8fc02d1ee592)|
|Binarize|Extract contour|
|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/ae05a498-6cc6-4178-aff3-b984684e8475)|![image](https://github.com/chungkang/L5IN_task2/assets/36185863/feab00a4-038f-4641-8895-a9ba42de209f)|
|Straighten contour|Geojson format of contour|

## 7. Georeference with QGIS
With QGIS, vector file can be georeferenced with [Layer-Georeferencer] function.
Since QGIS version 3.26, QGIS provides vector georeferencer function also for vector format.
![image](https://github.com/chungkang/L5IN_task2/assets/36185863/1c35c51d-3c19-499b-9388-fd3e0a5c2566)
Georeferenced vector data on OpenStreetMap

Among transformation algorithms of QGIS, Thin Plate Spline (TPS) algorithm has been chosen, which provided better results.
https://docs.qgis.org/3.28/en/docs/user_manual/working_with_raster/georeferencer.html#id7

## 8. Detect doors
Possible solution 1: define door with size of area
https://stackoverflow.com/questions/55356251/how-to-detect-doors-and-windows-from-a-floor-plan-image

Possible solution 2: Detect the center of arc part
https://stackoverflow.com/questions/62804419/detecting-the-center-of-an-arc-by-using-open-cv
https://stackoverflow.com/questions/59099931/how-to-find-different-centers-of-various-arcs-in-a-almost-circular-hole-using-op

Possible solution 3: detect ovelapping area of hallway and room

## 9. Unsolved problems
Symbol removal is not perfectly performed
Glare/Reflection correction didn’t applied
Adjacent object along wall affects contour detection
