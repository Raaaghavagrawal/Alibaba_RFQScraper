import re
import pandas as pd
from datetime import datetime

def extract_rfq_data_from_html():
    try:
        with open('alibaba_page_source.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print("Reading HTML file...")
        
        data_start = html_content.find('window.PAGE_DATA["index"].data = [];')
        if data_start == -1:
            print("Could not find data section")
            return []
        
        pattern = r'window\.PAGE_DATA\["index"\]\.data\.push\(\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\s*\}\)'
        matches = re.findall(pattern, html_content, re.DOTALL)
        
        print(f"Found {len(matches)} RFQ records")
        
        rfq_data_list = []
        
        for i, match in enumerate(matches):
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
                    print(f"Extracted RFQ {i+1}: {rfq_data.get('Title', 'No title')[:50]}...")
                        
            except Exception as e:
                print(f"Error parsing RFQ data {i+1}: {e}")
                continue
        
        return rfq_data_list
        
    except Exception as e:
        print(f"Error reading HTML file: {e}")
        return []

def main():
    print("Extracting RFQ data from saved HTML file...")
    
    rfq_data_list = extract_rfq_data_from_html()
    
    if rfq_data_list:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"alibaba_rfq_data_extracted_{timestamp}.csv"
        
        df = pd.DataFrame(rfq_data_list)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\nExtraction completed successfully!")
        print(f"Total records extracted: {len(rfq_data_list)}")
        print(f"Data saved to: {filename}")
        
        print("\nFirst 5 records:")
        print(df.head().to_string())
        
        print(f"\nColumns extracted: {list(df.columns)}")
        
    else:
        print("No data was extracted.")

if __name__ == "__main__":
    main() 