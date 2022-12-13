import rectanglecropper.crop as rc

cropper = rc.RectangleImageCrop()
cropper.open(image_path='images/image1.png')
cropper.crop()
cropper.save(saved_path='cropimages', filename='image1', saved_format='jpeg')