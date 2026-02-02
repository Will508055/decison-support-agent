from bs4 import BeautifulSoup

def parse_night_riding_html() -> str:
    file_path = 'documentation/Motorcycle_Night_Riding_by_Road_Guardians.html'

    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.find(class_='infinite-content-container infinite-container').get_text(strip=True)
    return text
