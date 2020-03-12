import pytesseract
import bs4 as bs
import cv2.cv2 as cv2
from PIL import Image
from pdf2image import convert_from_path
import difflib
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

PDF_file = "doc.pdf"

pages = convert_from_path(PDF_file, 500)

image_counter = 1
for page in pages:
    # PDF page n -> page_n.jpg
    filename = "page_" + str(image_counter) + ".jpg"

    # Save the image of the page in system
    page.save(filename, 'JPEG')

    # Increment the counter to update filename
    image_counter = image_counter + 1

# Variable to get count of total number of pages
filelimit = image_counter - 1

# Creating a text file to write the output
outfile = "out_text.html"
hocr = False

f = open(outfile, "ab")
# Iterate from 1 to total number of pages
for i in range(1, filelimit + 1):
    filename = "page_" + str(i) + ".jpg"
    hocr = pytesseract.image_to_pdf_or_hocr(filename, extension='hocr', config='--psm 12')
    f.write(hocr)

f.close()

def parse_hocr(search_terms=None, hocr_file=None, regex=None):
    """Parse the hocr file and find a reasonable bounding box for each of the strings
    in search_terms.  Return a dictionary with values as the bounding box to be used for
    extracting the appropriate text.

    inputs:
        search_terms = Tuple, A tuple of search terms to look for in the HOCR file.

    outputs:
        box_dict = Dictionary, A dictionary whose keys are the elements of search_terms and values
        are the bounding boxes where those terms are located in the document.
    """
    # Make sure the search terms provided are a tuple.
    if not isinstance(search_terms,list):
        raise ValueError('The search_terms parameter must be a list')

    # Make sure we got a HOCR file handle when called.
    if not hocr_file:
        raise ValueError('The parser must be provided with an HOCR file handle.')

    # Open the hocr file, read it into BeautifulSoup and extract all the ocr words.
    hocr = open(hocr_file,'r').read()
    soup = bs.BeautifulSoup(hocr,'html.parser')
    words = soup.find_all('span',class_='ocrx_word')

    result = dict()

    # Loop through all the words and look for our search terms.
    for word in words:

        w = word.get_text().lower()

        for s in search_terms:

            # If the word is in our search terms, find the bounding box
            if len(w) > 1 and difflib.SequenceMatcher(None, s, w).ratio() > .5:
                bbox = word['title'].split(';')
                print("######", bbox)
                bbox = bbox[0].split(' ')
                bbox = tuple([int(x) for x in bbox[1:]])

                # Update the result dictionary or raise an error if the search term is in there twice.
                if s not in result.keys():
                    result.update({s:bbox})

            else:
                pass

    return result

dimensions= parse_hocr(search_terms=["company"], hocr_file = outfile)["company"]

image = cv2.imread('page_1.jpg', 0)
thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

x, y, w, h = dimensions[0], dimensions[1], dimensions[2], dimensions[3]
ROI = thresh[y:y+h, x:x+w]
data = pytesseract.image_to_string(ROI, lang='eng', config='--psm 12')
print(data)