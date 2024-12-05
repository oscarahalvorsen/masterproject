import requests
from bs4 import BeautifulSoup
from books import books
import json
import time

def extract_article_from_url(url):
    """
    Henter vers fra en gitt URL og concatenater tekst for vers med samme ID.
    """
    response = requests.get(url, timeout=10)  # Timeout på 10 sekunder
    response.encoding = 'utf-8'
    
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return None
    
    html_text = response.text
    soup = BeautifulSoup(html_text, "html.parser") 
    
    article = soup.find("article", class_="relative max-w-2xl mx-4 md:mx-auto lg:mx-auto xl:mx-auto font-serif text-base md:text-lg lg:text-xl highlight-targets-in-text")
    
    if not article:
        print(f"No article found in {url}")
        return None

    verse_elements = article.find_all("span", id=True)

    verses = {}
    
    for verse in verse_elements:
        verse_id = verse.get("id")
        verse_text = verse.get_text(strip=True)
        
        # Concatenate text for duplicate verse IDs
        if verse_id in verses:
            verses[verse_id] += f" {verse_text}"
        else:
            verses[verse_id] = verse_text
    
    # Konverter dict til en liste med ønsket format
    formatted_verses = [{"verse": vid, "text": vtext} for vid, vtext in verses.items()]
    return formatted_verses

def extract_chapter_pair(book_abbr, chapter):
    """
    Henter vers fra både bokmål og nynorsk for en gitt bok og kapittel.
    """
    chapter_key = f"{book_abbr}.{chapter}"
    
    # Bokmål URL
    url_nb = f"https://bibel.no/nettbibelen/les/nb-2024/{book_abbr}/{chapter_key}"
    print(f"Processing {url_nb}")
    verses_nb = extract_article_from_url(url_nb)

    # Nynorsk URL
    url_nn = f"https://bibel.no/nettbibelen/les/nn-2024/{book_abbr}/{chapter_key}"
    print(f"Processing {url_nn}")
    verses_nn = extract_article_from_url(url_nn)

    # Hvis data mangler, hopp over dette kapittelet
    if not verses_nb or not verses_nn:
        print(f"Skipping {chapter_key} due to missing data.")
        return []

    # Kombiner bokmål og nynorsk vers
    paired_verses = []
    for verse_nb, verse_nn in zip(verses_nb, verses_nn):
        # Forsikre deg om at versene matcher på ID
        if verse_nb["verse"] == verse_nn["verse"]:
            paired_verses.append({"nb": verse_nb["text"], "nn": verse_nn["text"]})
        else:
            print(f"Verse ID mismatch in {chapter_key}: {verse_nb['verse']} != {verse_nn['verse']}")
    
    return paired_verses

def extract_all_books():
    """
    Henter alle bøker og kapittelpar for bokmål og nynorsk.
    """
    flat_verses = []
    
    for book in books:
        book_abbr = book["abbr"]
        
        for chapter in range(1, book["chapters"] + 1):
            paired_verses = extract_chapter_pair(book_abbr, chapter)
            flat_verses.extend(paired_verses)
            time.sleep(3)
        
    return flat_verses

def write_data_to_file(data, filename):
    """
    Skriver data til en JSONL-fil.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for item in data:
            json_line = json.dumps(item, ensure_ascii=False)
            f.write(json_line + '\n')

# Start datainnhenting
all_verses = extract_all_books()
write_data_to_file(all_verses, "datacollecting/NBS/NBS2023.jsonl")

print("Data successfully written to NBS2023.jsonl")
