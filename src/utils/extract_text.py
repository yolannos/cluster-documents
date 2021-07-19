import os

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


class ExtractText():

    def __init__(self, file, method='text'):
        '''
        file : path to the pdf to be extracted
        method : "text" or "ocr"
        '''       
        self.file = file              
        self.path_txt_ = 'temp/'
        self.method = method
        self._threshold_size = 2000 # minimum length expected for a pdf (arbitrary, based on the smallest document found)

    def _pdf_to_jpg(self):
        '''
        Conversion from PDF to JPEG used in the OCR-approach
        '''
        console.print("[cyan]Preprocessing file ...")
        self.pages = convert_from_path(self.file) #conversion 
        self.image_counter = 1
        for page in track(self.pages, description=f"[cyan]Converting pages ..."):
            page_name = f"{self.path_txt_}page_{str(self.image_counter)}.jpg"
            page.save(page_name, "JPEG")
            self.image_counter += 1

    def _extract_tess(self):
        '''
        Method to extract text from PDF via OCR-approach
        '''
        filelimit = self.image_counter
        text_extract = ''
        for i in track(range(1, filelimit), description=f'[cyan]Extracting text from images ...'):
                filename = f"{self.path_txt_}page_{str(i)}.jpg"
                # Recognize the text as string in image using pytesserct
                text = str((pytesseract.image_to_string(Image.open(filename))))
                text = text.replace('-\n', '')  # Cleaning line-break/hyphen

                text_extract += ' ' + text

        self._del_txt()
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
        Use of the extraction method specified in the instanciation of the class
        '''
        try:
            return getattr(self, self.method)()
        except AttributeError:
            raise NotImplementedError(f"Class `{self.__class__.__name__}` does not implement `{self.method}`")     

    def text(self):
        '''
        Use of the Simple-Approach to extract the text
        if the length of the text is too small (according to the threshold)
            -> use of the OCR method
        reason: pdf can contains static images and not text
        '''
        try:
            text = self._pdf_to_text()
            if len(text) >= self._threshold_size:
                return text
            else:
                print(f'\nIt seems that the file contains images instead of text. Applying OCR-Approach for file {os.path.basename(self.file)} ...')
                return self.ocr()

        except Exception as e:
            print(f'There was the following error: {e}')
    
    def ocr(self):
        try:
            self._pdf_to_jpg()
            return self._extract_tess()
        except Exception as e:
            print(f'There was the following error: {e}')

    def to_txt(self):
        '''
        export the text extracted to a text file
        '''
        outfile = "out_text.txt"
        with open(outfile, "w") as f:

            f.write(self.text_extracted)
            console.print("[cyan]Text file created ... :wolf:")

    def _del_txt(self):
        # removing files from temp/
        path = self.path_txt_
        files = os.listdir(path)      
        for file in track(files, description="[cyan]Deleting images from temp/ ..."):
            os.remove(f'temp/{file}')

