import cv2.cv2 as cv2
import numpy as np
import pytesseract
from PIL import Image
print ("Hello")
src_path = "E:\\optical_character_recognition\\hand_written.jpg"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


print (src_path)


# Read image with opencv
img = cv2.imread(src_path)

# Convert to gray
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply dilation and erosion to remove some noise
kernel = np.ones((1, 1), np.uint8)
img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)

# Write image after removed noise
cv2.imwrite(src_path + "removed_noise.png", img)

#  Apply threshold to get image with only black and white
#img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

# Write the image after apply opencv to do some ...
cv2.imwrite(src_path + "thres.png", img)

# Recognize text with tesseract for python
result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))


# Remove template file
#os.remove(temp)


import pytesseract, re
f = src_path + "thres.png"
custom_oem_psm_config = r'--oem 3 --psm 6'
t = pytesseract.image_to_string(Image.open(f), config=custom_oem_psm_config)
print(t+"\n")
m = re.findall(r"(?<=ORDER).+", t)
print(m)
if m:
    print(m[0])