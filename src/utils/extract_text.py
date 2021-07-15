import os
import sys

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

from rich.progress import track
from rich.console import Console
from rich.text import Text
from rich.traceback import install

install()
console = Console()

# Store all the pages of the PDF in a variable
text = Text("Preprocessing pages ...")
text.stylize("bold green")
console.print(text)


def extract_text(file):
    pages = convert_from_path(file)

    image_counter = 1

    for page in track(pages, description=f"[cyan]Converting pages ..."):
        page_name = "temp/page_" + str(image_counter) + ".jpg"
        page.save(page_name, "JPEG")
        image_counter += 1

    # Variable to get count of total number of pages
    filelimit = image_counter - 1

    # Creating a text file to write the output
    outfile = "out_text.txt"
    with open(outfile, "w") as f:
        print("Empty output file created")

    # Open the file in append mode so that
    # All contents of all images are added to the same file
    with open(outfile, "a") as f:
        # Iterate from 1 to total number of pages
        for i in track(range(1, filelimit + 1), description=f'[cyan]Extracting text from image ...'):
            filename = "temp/page_" + str(i) + ".jpg"
            # Recognize the text as string in image using pytesserct
            text_extract = str((pytesseract.image_to_string(Image.open(filename))))

            text_extract = text_extract.replace('-\n', '')  # Cleaning line-break/hyphen

            # Finally, write the processed text to the file.
            f.write(text_extract)

    files = os.listdir("temp/")

    # deleting files from temp/
    for file in track(files, description="[cyan]Deleting images from temp/ ..."):
        os.remove(f'temp/{file}')

    console.print("Everything is all set for categorising your file! :thumbs_up:")
