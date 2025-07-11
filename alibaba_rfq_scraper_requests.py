import requests
import pandas as pd
import time
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import re
from datetime import datetime
import urllib.parse

class AlibabaRFQScraperRequests:
    def __init__(self):
        self.base_url = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm"
        self.params = {
            'spm': 'a2700.8073608.1998677541.1.82be65aaoUUItC',
            'country': 'AE',
            'recently': 'Y',
            'tracelog': 'newest'
        }
        self.data = []
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(headers)
        
    def get_page_url(self, page=1):
        params = self.params.copy()
        if page > 1:
            params['page'] = page
        return f"{self.base_url}?{urllib.parse.urlencode(params)}"
    
    def extract_rfq_data(self, rfq_element):
        try:
            rfq_data = {
                'RFQ_ID': '',
                'Title': '',
                'Buyer_Country': '',
                'Buyer_Name': '',
                'Posted_Date': '',
                'Expiry_Date': '',
                'Category': '',
                'Quantity': '',
                'Unit': '',
                'Description': '',
                'Contact_Info': '',
                'Status': '',
                'Keywords': ''
            }
        
            rfq_id_attr = rfq_element.get('data-rfq-id') or rfq_element.get('id')
            if rfq_id_attr:
                rfq_data['RFQ_ID'] = rfq_id_attr
            
            title_selectors = ['.rfq-title', '.title', 'h3', 'h4', 'a[href*="rfq"]']
            for selector in title_selectors:
                title_elem = rfq_element.select_one(selector)
                if title_elem:
                    rfq_data['Title'] = title_elem.get_text(strip=True)
                    break
            
            buyer_selectors = ['.buyer-info', '.buyer', '.company', '.supplier']
            for selector in buyer_selectors:
                buyer_elem = rfq_element.select_one(selector)
                if buyer_elem:
                    buyer_text = buyer_elem.get_text(strip=True)
                    country_match = re.search(r'([A-Z]{2})$', buyer_text)
                    if country_match:
                        rfq_data['Buyer_Country'] = country_match.group(1)
                        rfq_data['Buyer_Name'] = buyer_text.replace(country_match.group(1), '').strip()
                    else:
                        rfq_data['Buyer_Name'] = buyer_text
                    break
            
            date_selectors = ['.date', '.time', '.posted-date', '.expiry-date']
            date_elements = []
            for selector in date_selectors:
                date_elements.extend(rfq_element.select(selector))
            
            if len(date_elements) >= 1:
                rfq_data['Posted_Date'] = date_elements[0].get_text(strip=True)
            if len(date_elements) >= 2:
                rfq_data['Expiry_Date'] = date_elements[1].get_text(strip=True)
            
            category_selectors = ['.category', '.cat', '.industry', '.product-category']
            for selector in category_selectors:
                cat_elem = rfq_element.select_one(selector)
                if cat_elem:
                    rfq_data['Category'] = cat_elem.get_text(strip=True)
                    break
            
            quantity_selectors = ['.quantity', '.qty', '.amount', '.volume']
            for selector in quantity_selectors:
                qty_elem = rfq_element.select_one(selector)
                if qty_elem:
                    quantity_text = qty_elem.get_text(strip=True)
                    qty_match = re.search(r'(\d+(?:\.\d+)?)\s*([a-zA-Z]+)', quantity_text)
                    if qty_match:
                        rfq_data['Quantity'] = qty_match.group(1)
                        rfq_data['Unit'] = qty_match.group(2)
                    else:
                        rfq_data['Quantity'] = quantity_text
                    break
            
            desc_selectors = ['.description', '.desc', '.details', '.content']
            for selector in desc_selectors:
                desc_elem = rfq_element.select_one(selector)
                if desc_elem:
                    rfq_data['Description'] = desc_elem.get_text(strip=True)
                    break
            
            contact_selectors = ['.contact', '.contact-info', '.contact-details']
            for selector in contact_selectors:
                contact_elem = rfq_element.select_one(selector)
                if contact_elem:
                    rfq_data['Contact_Info'] = contact_elem.get_text(strip=True)
                    break
            
            status_selectors = ['.status', '.state', '.condition']
            for selector in status_selectors:
                status_elem = rfq_element.select_one(selector)
                if status_elem:
                    rfq_data['Status'] = status_elem.get_text(strip=True)
                    break
            
            keyword_selectors = ['.keyword', '.tag', '.label']
            keywords = []
            for selector in keyword_selectors:
                keyword_elements = rfq_element.select(selector)
                keywords.extend([elem.get_text(strip=True) for elem in keyword_elements])
            
            if keywords:
                rfq_data['Keywords'] = ', '.join(keywords)
            
            return rfq_data
            
        except Exception as e:
            print(f"Error extracting RFQ data: {e}")
            return None
    
    def scrape_page(self, page=1):
        url = self.get_page_url(page)
        print(f"Scraping page {page}: {url}")
        
        try:
            time.sleep(random.uniform(2, 5))
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            rfq_selectors = [
                '.rfq-item',
                '.rfq-list-item',
                '.list-item',
                '.item',
                '[data-rfq-id]',
                '.rfq-card',
                '.card',
                '.rfq-entry',
                '.rfq-row'
            ]
            
            rfq_elements = []
            for selector in rfq_selectors:
                elements = soup.select(selector)
                if elements:
                    rfq_elements = elements
                    print(f"Found {len(elements)} RFQ elements using selector: {selector}")
                    break
            
            if not rfq_elements:
                print("No RFQ elements found on this page")
                potential_elements = soup.select('div, li, tr')
                print(f"Found {len(potential_elements)} potential elements to analyze")
                return False
            
            page_data = []
            for rfq_element in rfq_elements:
                rfq_data = self.extract_rfq_data(rfq_element)
                if rfq_data:
                    page_data.append(rfq_data)
            
            self.data.extend(page_data)
            print(f"Extracted {len(page_data)} RFQ records from page {page}")
            
            return len(page_data) > 0
            
        except requests.exceptions.RequestException as e:
            print(f"Request error scraping page {page}: {e}")
            return False
        except Exception as e:
            print(f"Error scraping page {page}: {e}")
            return False
    
    def scrape_all_pages(self, max_pages=50):
        page = 1
        consecutive_empty_pages = 0
        
        while page <= max_pages and consecutive_empty_pages < 3:
            success = self.scrape_page(page)
            
            if success:
                consecutive_empty_pages = 0
            else:
                consecutive_empty_pages += 1
            
            page += 1
            
            time.sleep(random.uniform(3, 7))
        
        print(f"Scraping completed. Total pages scraped: {page-1}")
        print(f"Total RFQ records collected: {len(self.data)}")
    
    def save_to_csv(self, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"alibaba_rfq_data_requests_{timestamp}.csv"
        
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Data saved to {filename}")
        return filename

def main():
    scraper = AlibabaRFQScraperRequests()
    
    try:
        print("Starting Alibaba RFQ scraper (requests version)...")
        scraper.scrape_all_pages(max_pages=50)
        
        if scraper.data:
            filename = scraper.save_to_csv()
            print(f"\nScraping completed successfully!")
            print(f"Total records scraped: {len(scraper.data)}")
            print(f"Data saved to: {filename}")
            
            print("\nFirst 5 records:")
            df = pd.DataFrame(scraper.data)
            print(df.head().to_string())
        else:
            print("No data was scraped. Please check the website structure or try again later.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 