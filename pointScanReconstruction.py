import numpy as np
import matplotlib.pyplot as plt
import cv2

# === Load the data ===
data = np.load(
    "/Users/aayanmaheshwari/Desktop/random/compPhotos/scan_data64.npz"
)  # <-- Replace with your file
print(data.files)


N = 128

a = data["output"]
print(a)

width = len(a[0])
for i in range(5):
    a[i] = [np.min(a)] * width

# # === Reshape to 64x64 ===

fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# === Display the image ===
axs[0].imshow(a, cmap="gray")  # Use 'gray' or remove cmap for default
axs[0].axis("off")


img_norm = a - np.min(a)  # Subtract min
img_norm = img_norm / np.max(img_norm)  # Divide by max
img_uint8 = (img_norm * 255).astype(np.uint8)  # Scale and convert to uint8

# Gaussian Blur
img_uint8 = cv2.GaussianBlur(img_uint8, (3, 3), 0)
axs[1].imshow(img_uint8, cmap="gray")
axs[1].axis("off")
# axs[1].set_title('After Gaussian Blur')


# cv2.imwrite('/Users/jon/Documents/PROJECTS/15_dualPhotography/results/cat_NLS.png', img_uint8)

plt.tight_layout()
plt.show()
