import pytesseract
from pdf2image import convert_from_path
import glob
from rich.traceback import install
install()

pdf = "dataset/testpdf.pdf"

# images = convert_from_path(pdf)

# i = 1
# for image in images:
#     image_name = "dataset/Page_" + str(i) + ".jpg"  
#     image.save(image_name, "JPEG")
#     i = i+1