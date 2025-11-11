import PyPDF2

def extract_text_from_pdf(pdf_path: str) -> str:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def save_pdf_file(file, destination: str) -> None:
    with open(destination, 'wb') as f:
        f.write(file.read())