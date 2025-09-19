import cv2
import numpy as np
import matplotlib.pyplot as plt
import pywt

# Import image and convert to a gray scale image
color_img = cv2.imread("Images/sample_face.jpg")
gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

# Perform multi-level wavelet decomposition
wavelet = "bior4.4"
level = 4
coeffs = pywt.wavedec2(gray_img, wavelet, level=level)

# Flatten arrays from wavelet decomposition into one array and take absolute value
arrs = [coeffs[0].flatten()] 
arr, coeff_slices = pywt.coeffs_to_array(coeffs)
abs_coeffs = np.abs(arr.flatten())

# Fractions of highest coefficients we want to keep
fractions = [0.005, 0.05, 0.1]

# Set up plot
fig, axes = plt.subplots(2, 2, figsize=(9, 9))
fig.suptitle("Wavelet compressed image for different fractions of coefficients kept compared with original image")

for ax, fraction in zip(axes.flat, fractions):
    # Determine threshold
    k = int(fraction * len(abs_coeffs))
    threshold = np.partition(abs_coeffs, -k)[-k]

    # Apply threshold to coefficients and reconstruct coefficient list
    cA = pywt.threshold(coeffs[0], threshold, mode="hard")
    new_coeffs = [cA]
    for detail_level in coeffs[1:]:
        new_level = tuple(pywt.threshold(array, threshold, mode="hard") for array in detail_level)
        new_coeffs.append(new_level)

    # Reconstruct image and plot
    compressed_img = pywt.waverec2(new_coeffs, wavelet)
    ax.imshow(compressed_img, cmap="gray")
    ax.set_title(f"{fraction*100:.1f}% of coefficients kept")
    ax.axis(False)

# Plot Original Image
axes.flat[-1].imshow(gray_img, cmap="gray")
axes.flat[-1].set_title("Original Image")
axes.flat[-1].axis(False)

plt.tight_layout()
plt.show()
