from frr import FastReflectionRemoval

# numpy array with values between 0 and 1 of shape (H, W, C)
img = "20220112_162250_warped.png"
# instantiate the algoroithm class
alg = FastReflectionRemoval(h = 0.11)
# run the algorithm and get result of shape (H, W, C)
dereflected_img = alg.remove_reflection(img)