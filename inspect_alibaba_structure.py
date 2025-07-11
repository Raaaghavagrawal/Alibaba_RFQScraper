import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

def inspect_alibaba_structure():
    url = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?spm=a2700.8073608.1998677541.1.82be65aaoUUItC&country=AE&recently=Y&tracelog=newest"
    
    session = requests.Session()
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    session.headers.update(headers)
    
    try:
        print(f"Fetching URL: {url}")
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        with open('alibaba_page_source.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("HTML source saved to alibaba_page_source.html")
        
        print("\n=== Analyzing page structure ===")
        
        potential_selectors = [
            'div[class*="rfq"]',
            'div[class*="item"]', 
            'div[class*="list"]',
            'div[class*="card"]',
            'div[class*="row"]',
            'li[class*="rfq"]',
            'li[class*="item"]',
            'tr[class*="rfq"]',
            'tr[class*="item"]'
        ]
        
        for selector in potential_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"\nFound {len(elements)} elements with selector: {selector}")
                for i, elem in enumerate(elements[:3]):
                    print(f"  Element {i+1}:")
                    print(f"    Classes: {elem.get('class', [])}")
                    print(f"    ID: {elem.get('id', 'None')}")
                    print(f"    Text preview: {elem.get_text()[:100]}...")
                    print()
        
        data_elements = soup.find_all(attrs={"data-rfq-id": True})
        if data_elements:
            print(f"Found {len(data_elements)} elements with data-rfq-id")
        
        rfq_id_elements = soup.find_all(id=lambda x: x and 'rfq' in x.lower())
        if rfq_id_elements:
            print(f"Found {len(rfq_id_elements)} elements with ID containing 'rfq'")
        
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables")
        
        lists = soup.find_all(['ul', 'ol'])
        print(f"Found {len(lists)} lists (ul/ol)")
        
        rfq_text_elements = soup.find_all(string=lambda text: text and ('RFQ' in text.upper() or 'Request' in text))
        print(f"Found {len(rfq_text_elements)} text elements containing 'RFQ' or 'Request'")
        
        forms = soup.find_all('form')
        print(f"Found {len(forms)} forms")
        
        print("\n=== Looking for specific text patterns ===")
        page_text = soup.get_text()
        
        if 'RFQ' in page_text.upper():
            print("Page contains 'RFQ' text")
        if 'Request' in page_text:
            print("Page contains 'Request' text")
        if 'Quote' in page_text:
            print("Page contains 'Quote' text")
        if 'Buyer' in page_text:
            print("Page contains 'Buyer' text")
        if 'Supplier' in page_text:
            print("Page contains 'Supplier' text")
        
        if 'login' in page_text.lower() or 'sign in' in page_text.lower():
            print("WARNING: Page might require authentication")
        
        if 'captcha' in page_text.lower():
            print("WARNING: Page might have CAPTCHA protection")
        
        with open('alibaba_page_text.txt', 'w', encoding='utf-8') as f:
            f.write(page_text[:5000])
        print("Page text sample saved to alibaba_page_text.txt")
        
        return soup
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    inspect_alibaba_structure() 