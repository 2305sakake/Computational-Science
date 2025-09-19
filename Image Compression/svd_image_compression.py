import cv2
import numpy as np
import matplotlib.pyplot as plt

# Import image and convert to a gray scale image
color_img = cv2.imread("Images/sample_face.jpg")
gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

# Extract image shape and size
n, m = gray_img.shape
original_storage = n*m

# Calculate SVD of the image matrix
U, S, V = np.linalg.svd(gray_img, full_matrices=False)

# r values we wish to test
r_values = [25, 100, 250]

# Set up figure and plot images for corresponding r values
fig, axes = plt.subplots(2, 2, figsize=(9, 9))
fig.suptitle("SVD compressed image for different r values compared with original image")

for ax, r in zip(axes.flat, r_values):
    img_approx = U[:,:r] @ np.diag(S[:r]) @ V[:r,:]
    storage = r * (n + m + 1)
    storage_percent = storage*100/original_storage
    ax.imshow(img_approx, cmap="gray")
    ax.set_title(f"r = {r}, Storage = {storage_percent:.2f}%")
    ax.axis(False)

axes.flat[-1].imshow(gray_img, cmap="gray")
axes.flat[-1].set_title("Original Image")
axes.flat[-1].axis(False)

plt.tight_layout()
plt.show()
