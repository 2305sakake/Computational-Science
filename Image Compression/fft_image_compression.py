import cv2
import numpy as np
import matplotlib.pyplot as plt

# Import image and convert to a gray scale image
color_img = cv2.imread("Images/sample_face.jpg")
gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

# Perform 2D FFT and get a flattened magnitude version of FFT
F = np.fft.fft2(gray_img)
F_mag = np.abs(F)
F_flatten = F_mag.flatten()

# Fractions of highest Fourier coefficients we want to keep
fractions = [0.005, 0.05, 0.25]

# Set up plot
fig, axes = plt.subplots(2, 2, figsize=(9, 9))
fig.suptitle("FFT compressed image for different fractions of coefficients kept compared with original image")

for ax, fraction in zip(axes.flat, fractions):
    # Determine threshold
    k = int(fraction * len(F_flatten))
    threshold = np.partition(F_flatten, -k)[-k]

    # Use mask to only keep values higher than threshold and inverse FFT back to recover image
    mask = F_mag >= threshold
    compressed_F = F * mask

    # Reconstruct image and plot
    compressed_img = np.fft.ifft2(compressed_F).real
    ax.imshow(compressed_img, cmap="gray")
    ax.set_title(f"{fraction*100}% of coefficients kept")
    ax.axis(False)

# Plot original image
axes.flat[-1].imshow(gray_img, cmap="gray")
axes.flat[-1].set_title("Original Image")
axes.flat[-1].axis(False)

plt.tight_layout()
plt.show()
