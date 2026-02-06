from bs4 import BeautifulSoup

def parse_html_documents() -> list[str]:
    file_classes_map = {'Motorcycle_Night_Riding_by_Road_Guardians.html': 'infinite-content-container infinite-container',
                        'Cornering_101.html': 'post hentry uncustomized-post-template',
                        'Tips_for_Cornering.html': 'blog__article__content rte',
                        'Navigating_Blind_Turns.html': 'entry-content'}
    
    parsed_texts = []

    for key, value in file_classes_map.items():
        path = f'documentation/{key}'
        with open(path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.find(class_=value).get_text(strip=True)
        parsed_texts.append(text)

    return parsed_texts