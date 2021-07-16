import src.utils.extract_text as extract

pdf = './dataset/testpdf.pdf'

extract = extract.extractText(pdf)

extract._pdf_to_jpg()
extract._extract_tess()
extract.to_txt()

