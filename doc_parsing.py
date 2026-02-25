import os
from bs4 import BeautifulSoup
import fitz
from PIL import Image
import io
import pytesseract

# Mapping of HTML file names to their respective class names for text extraction
html_file_classes_map = {'Motorcycle_Night_Riding_by_Road_Guardians.html': 'infinite-content-container infinite-container',
                    'Cornering_101.html': 'post hentry uncustomized-post-template',
                    'Tips_for_Cornering.html': 'blog__article',
                    'Navigating_Blind_Turns.html': 'entry-content'}

def list_documentation_files() -> list[str]:
    file_paths = []
    for root, _, files in os.walk('documentation'):
        for filename in files:
            full_path = os.path.join(root, filename)
            file_paths.append(full_path)
    return file_paths


def parse_html(file_path: str) -> str:
    file_name = file_path.split('\\')[-1]
    if file_name not in html_file_classes_map:
        print(f'File {file_name} not found in HTML mapping.')
        return None

    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    class_name = html_file_classes_map[file_name]
    text = soup.find(class_=class_name).get_text(strip=True)
    return text


def parse_pdf(file_path: str) -> str:
    with fitz.open(file_path) as pdf_document:
        text_content = []
        for page in pdf_document:
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))
            text_content.append(pytesseract.image_to_string(img))
    return '\n'.join(text_content)


def parse_documentation() -> list[str]:
    documentation = []
    for file_path in list_documentation_files():
        if file_path.endswith('.html'):
            text = parse_html(file_path)
            documentation.append(text)
        elif file_path.endswith('.pdf'):
            text = parse_pdf(file_path)
            documentation.append(text)
        else:
            print(f'Unsupported file type for {file_path}')
            continue
    return documentation