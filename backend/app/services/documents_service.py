import fitz
import pytesseract

from PIL import Image
from io import BytesIO

# Tesseract OCR executable
import pytesseract
import os

if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a normal digital PDF.
    """

    document = fitz.open(
        stream=file_bytes,
        filetype="pdf"
    )

    extracted_text = ""

    for page in document:
        extracted_text += page.get_text()

    document.close()

    return extracted_text.strip()


def extract_text_from_image(file_bytes: bytes) -> str:
    """
    Extract text from image using Tesseract OCR.
    """

    image = Image.open(
        BytesIO(file_bytes)
    )

    text = pytesseract.image_to_string(image)

    return text.strip()


def extract_text(
    file_bytes: bytes,
    filename: str
) -> str:

    extension = filename.lower().split(".")[-1]

    if extension == "pdf":
        text = extract_text_from_pdf(file_bytes)

        return text

    elif extension in [
        "jpg",
        "jpeg",
        "png"
    ]:

        text = extract_text_from_image(file_bytes)

        return text

    else:

        raise ValueError(
            "Unsupported file format"
        )