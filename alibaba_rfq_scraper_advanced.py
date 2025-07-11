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

class AlibabaRFQScraperAdvanced:
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
    
    def extract_js_data(self, html_content):
        try:
            pattern = r'window\.PAGE_DATA\["index"\]\.data\.push\(({[^}]+})\)'
            matches = re.findall(pattern, html_content, re.DOTALL)
            
            if not matches:
                pattern = r'window\.PAGE_DATA\["index"\]\.data\s*=\s*(\[[^\]]+\])'
                match = re.search(pattern, html_content, re.DOTALL)
                if match:
                    pass
            
            rfq_data_list = []
            
            for match in matches:
                try:
                    js_obj_str = match.strip()
                    
                    js_obj_str = js_obj_str.replace('\\x20', ' ')
                    js_obj_str = js_obj_str.replace('\\x2d', '-')
                    js_obj_str = js_obj_str.replace('\\x2f', '/')
                    js_obj_str = js_obj_str.replace('\\x3d', '=')
                    js_obj_str = js_obj_str.replace('\\x26', '&')
                    js_obj_str = js_obj_str.replace('\\x27', "'")
                    js_obj_str = js_obj_str.replace('\\x3a', ':')
                    js_obj_str = js_obj_str.replace('\\x2c', ',')
                    
                    rfq_data = {}
                    
                    id_match = re.search(r'id:\s*"([^"]+)"', js_obj_str)
                    if id_match:
                        rfq_data['RFQ_ID'] = id_match.group(1)
                    
                    subject_match = re.search(r'subject:\s*"([^"]+)"', js_obj_str)
                    if subject_match:
                        rfq_data['Title'] = subject_match.group(1)
                    
                    buyer_match = re.search(r'buyerName:\s*\'([^\']+)\'', js_obj_str)
                    if buyer_match:
                        rfq_data['Buyer_Name'] = buyer_match.group(1)
                    
                    country_match = re.search(r'country:\s*"([^"]+)"', js_obj_str)
                    if country_match:
                        rfq_data['Buyer_Country'] = country_match.group(1)
                    
                    country_simple_match = re.search(r'countrySimple:\s*"([^"]+)"', js_obj_str)
                    if country_simple_match:
                        rfq_data['Buyer_Country_Code'] = country_simple_match.group(1)
                    
                    quantity_match = re.search(r'quantity:\s*\'([^\']+)\'', js_obj_str)
                    if quantity_match:
                        rfq_data['Quantity'] = quantity_match.group(1)
                    
                    quantity_unit_match = re.search(r'quantityUnit:\s*"([^"]+)"', js_obj_str)
                    if quantity_unit_match:
                        rfq_data['Unit'] = quantity_unit_match.group(1)
                    
                    desc_match = re.search(r'description:\s*"([^"]+)"', js_obj_str)
                    if desc_match:
                        rfq_data['Description'] = desc_match.group(1)
                    
                    open_time_match = re.search(r'openTimeStr:\s*"([^"]+)"', js_obj_str)
                    if open_time_match:
                        rfq_data['Posted_Date'] = open_time_match.group(1)
                    
                    exp_time_match = re.search(r'expirationTime:\s*"([^"]+)"', js_obj_str)
                    if exp_time_match and exp_time_match.group(1):
                        rfq_data['Expiry_Date'] = exp_time_match.group(1)
                    
                    url_match = re.search(r'url:\s*"([^"]+)"', js_obj_str)
                    if url_match:
                        rfq_data['Detail_URL'] = url_match.group(1)
                    
                    tags_match = re.search(r'tags:\s*(\[[^\]]+\])', js_obj_str)
                    if tags_match:
                        tags_str = tags_match.group(1)
                        tag_names = re.findall(r'"tagName":"([^"]+)"', tags_str)
                        rfq_data['Keywords'] = ', '.join(tag_names)
                    
                    rfq_level_match = re.search(r'rfqLevel:\s*"([^"]+)"', js_obj_str)
                    if rfq_level_match:
                        rfq_data['Status'] = rfq_level_match.group(1)
                    
                    quote_extra_match = re.search(r'quoteExtraCount:\s*parseInt\("([^"]+)"', js_obj_str)
                    if quote_extra_match:
                        rfq_data['Quote_Count'] = quote_extra_match.group(1)
                    
                    rfq_extra_match = re.search(r'rfqExtraCount:\s*parseInt\("([^"]+)"', js_obj_str)
                    if rfq_extra_match:
                        rfq_data['RFQ_Count'] = rfq_extra_match.group(1)
                    
                    rfq_data.setdefault('Category', '')
                    rfq_data.setdefault('Contact_Info', '')
                    
                    if rfq_data:
                        rfq_data_list.append(rfq_data)
                        
                except Exception as e:
                    print(f"Error parsing RFQ data: {e}")
                    continue
            
            return rfq_data_list
            
        except Exception as e:
            print(f"Error extracting JS data: {e}")
            return []
    
    def scrape_page(self, page=1):
        url = self.get_page_url(page)
        print(f"Scraping page {page}: {url}")
        
        try:
            time.sleep(random.uniform(2, 5))
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            rfq_data_list = self.extract_js_data(response.text)
            
            if rfq_data_list:
                self.data.extend(rfq_data_list)
                print(f"Extracted {len(rfq_data_list)} RFQ records from page {page}")
                return True
            else:
                print(f"No RFQ data found on page {page}")
                return False
            
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
    scraper = AlibabaRFQScraperAdvanced()
    
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