import os
import sys

import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import pdftotext

from rich.progress import track
from rich.console import Console
from rich.text import Text
from rich.traceback import install

install()
console = Console()


class extractText():

    def __init__(self, file, method='text'):
        '''
        file : path to the pdf to be extracted
        method : "text" or "ocr"
        '''
        
        self.file = file              
        self.path_txt_ = 'temp/'

    def _pdf_to_jpg(self):
        '''
        Conversion from PDF to JPEG used in the OCR-approach
        '''

        console.print("[cyan]Preprocessing files ... :bear:")
        self.pages = convert_from_path(self.file) #conversion 
        self.image_counter = 1
        for page in track(self.pages, description=f"[cyan]Converting pages ..."):
            page_name = f"{self.path_}page_{str(self.image_counter)}.jpg"
            page.save(page_name, "JPEG")
            self.image_counter += 1

    def _extract_tess(self):
        '''
        Method to extract text from PDF via OCR-approach
        '''

        filelimit = self.image_counter
        for i in track(range(1, filelimit), description=f'[cyan]Extracting text from images ...'):
                filename = f"{self.path_}page_{str(i)}.jpg"
                # Recognize the text as string in image using pytesserct
                text_extract = str((pytesseract.image_to_string(Image.open(filename))))

                text_extract = text_extract.replace('-\n', '')  # Cleaning line-break/hyphen

                return text_extract

    def _pdf_to_text(self):
        '''
        Method to extract text from PDF via a "simple" approach
        '''

        with open(self.file, "rb") as f:
            pdf = pdftotext.PDF(f)
            self.text_extracted = " ".join([page for page in pdf])
            self.text_extracted =  " ".join(self.text_extracted.split())
            return self.text_extracted

    def extract(self):
        '''
        Try to extract text from Simple-approach. 
        If no text to select, use the OCR-approach
        '''

        try:
            return self._pdf_to_text()
        
        except:
            self._pdf_to_jpg()
            return self._extract_tess()

    def to_txt(self):
        '''
        '''

        outfile = "out_text.txt"
        with open(outfile, "w") as f:

            f.write(self.text_extracted)
            console.print("[cyan]Text file created ... :wolf:")

    def del_txt(self, path='temp/'):
        # removing files from temp/

        files = os.listdir(path)      
        for file in track(files, description="[cyan]Deleting images from temp/ ..."):
            os.remove(f'temp/{file}')

        console.print("Everything is all set for categorising your file! :thumbs_up:")
