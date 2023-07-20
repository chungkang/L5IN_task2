# L5IN Task 2: Vectorized Floor Plan Generation from Emergency Evacuation Plan Images

Input source: Images of Emergency Evacuation Plans
Expected Result: Geospatial format (shp, geojson) of vectorized floor plans

## Main Logic

### 1. Capture Photo of Emergency Evacuation Plan
It is preferable to use well-projected, high-resolution, and low-glare/reflected images.

|![Well Projected](https://github.com/chungkang/L5IN_task2/assets/36185863/af151ea8-a216-4d9d-b34b-45cb1af11b68)|![Reflection and Side View](https://github.com/chungkang/L5IN_task2/assets/36185863/ab47eec3-cce6-48bf-8426-6607a9c16dbe)|
|-|-|
|Well Projected Image|Image with Reflection and Side View|

### 2. Reproject (Rectify) Image
If the image is not well projected, reproject (rectify) it.
Compute Vanishing points using RANSAC and rectify the image.

Reference: [chsasank's Image-Rectification](https://github.com/chsasank/Image-Rectification) based on the paper: "Auto-rectification of user photos" by Chaudhury, Krishnendu, Stephen DiVerdi, and Sergey Ioffe.

|![Projected from Side View](https://github.com/chungkang/L5IN_task2/assets/36185863/645795a5-37be-4b86-92b5-9e751eaf5a79)|![Reprojected/Rectified Image](https://github.com/chungkang/L5IN_task2/assets/36185863/9b49c96b-2154-4eba-8f34-d0d827f61b28)|
|-|-|
|Projected from Side View|Reprojected/Rectified Image|

Crop the necessary part of the image.

### 3. Filter the Image to Reduce Noise
Reduce noise from the image with the bilateral filter of OpenCV.

|![Before Filtering Noise](https://github.com/chungkang/L5IN_task2/assets/36185863/59590f39-a5ef-4bb3-bc4b-bdcc5c751614)|![After Filtering Noise](https://github.com/chungkang/L5IN_task2/assets/36185863/ebc90368-9c1d-4549-9fe6-c0571821a2d7)|
|-|-|
|Before Filtering Noise|After Filtering Noise|

Adjust the following parameters to preserve the edges of the image while reducing noise:
- Diameter: The diameter of each pixel neighborhood used during filtering. Larger values result in stronger smoothing.
- SigmaColor: The standard deviation of the color space. Larger values include more colors in the filtering process.
- SigmaSpace: The standard deviation of the coordinate space. Larger values include pixels farther apart in the spatial domain as neighbors.

### 4. Remove Symbols from the Image with Feature Matching
Reduce symbols on the emergency evacuation plan using the feature matching method of OpenCV.

Feature Matching Steps:
- Clustering: MEANSHIFT => Divide the image.
- Feature Extraction: SIFT => Extract feature points from the divided image.
- Feature Matching: FLANN => Match feature points between the image and symbols.
- Homography Calculation: RANSAC => Calculate offset, rotation, and scale of the symbol on the image.

Symbols should be cropped from each image.

|![Before Removing Symbols](https://github.com/chungkang/L5IN_task2/assets/36185863/be492029-a32e-4c76-8c96-e956ae1418db)|![After Removing Symbols](https://github.com/chungkang/L5IN_task2/assets/36185863/4411b11f-5b15-441f-8bc6-a9e5e5316675)|![Cropped Symbols from Image](https://github.com/chungkang/L5IN_task2/assets/36185863/d221f2e4-0afe-408e-a4e8-6cbc796c5669)|
|-|-|-|
|Before Removing Symbols|After Removing Symbols|Cropped Symbols from Image|

Adjust the following parameters for reducing symbols from the image:
- MIN_MATCH_COUNT: The minimum number of matches required for a template image to be considered valid.
- MATCH_DISTANCE: The threshold for accepting matches based on their distance ratio in the Lowe's ratio test.
- NUMBER_OF_TEMPLATES: The number of template images to be processed.
- PAD: The padding value used when generating the destination points for perspective transformation.

### 5. Stitch Images
If the image does not cover the whole floor, stitch images to create a single floor image.

Images should be stitched one by one.

|![3OG Part 1](https://github.com/chungkang/L5IN_task2/assets/36185863/fe67683b-00c6-4d7d-a917-c47afc809e9c)|![3OG Part 2](https://github.com/chungkang/L5IN_task2/assets/36185863/fed1ea65-53ac-46d7-98d0-47c4d46d3ded)|![3OG Part 3](https://github.com/chungkang/L5IN_task2/assets/36185863/020109fb-f146-416a-ade6-0239246f365c)|
|-|-|-|
|3OG Part 1|3OG Part 2|3OG

 Part 3|

|![3OG Part 1 + Part 2](https://github.com/chungkang/L5IN_task2/assets/36185863/efb0bf38-b009-4dbc-86b0-6d37cffcab62)|![3OG Full Floor](https://github.com/chungkang/L5IN_task2/assets/36185863/112d9bd8-12aa-42e0-8df0-8b316f5268bc)|
|-|-|
|3OG Part 1 + Part 2|3OG Full Floor|

### 6. Extract Contours of Walls
Adjust the following parameters:
- MIN_AREA: The minimum contour area required for an object to be considered valid.
- BINARY_THRESHOLD: The threshold value for creating a binary image from the grayscale image.
- APPROX_CONTOUR: The percentage of the contour perimeter that should be approximated.

Logic Steps: Binarize -> Extract Contour -> Straighten Contour -> Save as GeoJSON

|![Binarize](https://github.com/chungkang/L5IN_task2/assets/36185863/26b66b0a-62af-4d9a-bf95-60f3e143760d)|![Extract Contour](https://github.com/chungkang/L5IN_task2/assets/36185863/8f4726c8-4241-4ffc-bebf-8fc02d1ee592)|
|-|-|
|Binarize|Extract Contour|

|![Straighten Contour](https://github.com/chungkang/L5IN_task2/assets/36185863/ae05a498-6cc6-4178-aff3-b984684e8475)|![GeoJSON Format of Contour](https://github.com/chungkang/L5IN_task2/assets/36185863/feab00a4-038f-4641-8895-a9ba42de209f)|
|-|-|
|Straighten Contour|GeoJSON Format of Contour|

### 7. Georeference with QGIS
Vector files can be georeferenced with the [Layer-Georeferencer] function in QGIS. Since QGIS version 3.26, QGIS provides vector georeferencer function for vector format.

![Georeferenced Vector Data on OpenStreetMap](https://github.com/chungkang/L5IN_task2/assets/36185863/1c35c51d-3c19-499b-9388-fd3e0a5c2566)

Among the transformation algorithms of QGIS, the Thin Plate Spline (TPS) algorithm has been chosen for better results.

### 8. Detect Doors
Possible solutions for door detection:
1. Define door with a size of area.
2. Detect the center of the arc part.
3. Detect overlapping areas of hallway and room.

### 9. Unsolved Problems
- Symbol removal is not perfectly performed.
- Glare/Reflection correction hasn't been applied.
- Adjacent objects along the wall affect contour detection.
