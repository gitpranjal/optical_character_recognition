from PIL import Image
from pdf2image import convert_from_path
import re
import pytesseract
import cv2.cv2 as cv2
import numpy as np
import os

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
custom_oem_psm_config = r'--oem 3 --psm 6'

# column = Image.open('code.png')
# gray = column.convert('L')
# blackwhite = gray.point(lambda x: 0 if x < 200 else 255, '1')
# blackwhite.save("code_bw.jpg")

# Path of the pdf
PDF_file = "doc.pdf"
# Store all the pages of the PDF in a variable
pages = convert_from_path(PDF_file, 500)

# Counter to store images of each page of PDF to image
image_counter = 1

# Iterate through all the pages stored above
t = ""

for page in pages:
    # Declaring filename for each page of PDF as JPG
    # For each page, filename will be:
    # PDF page 1 -> page_1.jpg
    # PDF page 2 -> page_2.jpg
    # PDF page 3 -> page_3.jpg
    # ....
    # PDF page n -> page_n.jpg
    filename = "page_" + str(image_counter) + ".jpg"
    page.save(filename, 'JPEG')

    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    text = str(((pytesseract.image_to_string(img, config=custom_oem_psm_config))))
    t += text+"\n"

    os.remove(filename)

information_extracted = ["DATE", "ORDER NO", "COMPANY", "FROM", "STYLE NAME", "Style Number"]

print(t)
m = re.findall(r"(?<=Style Number).+", t)
print(m)
if m:
    print(m[0])



