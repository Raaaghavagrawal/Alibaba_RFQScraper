# Alibaba RFQ Scraper

---

This project contains Python scripts to scrape Request for Quote (RFQ) data from Alibaba's sourcing platform.

## Features

- Scrapes RFQ data from multiple pages
- Extracts comprehensive information including RFQ ID, title, buyer details, dates, quantities, etc.
- Supports both Selenium (for JavaScript-heavy pages) and Requests (for static pages)
- Saves data to CSV format
- Includes anti-detection measures (random delays, user agents)
- Error handling and retry logic

## Files

1. `alibaba_rfq_scraper.py` - Main scraper using Selenium (recommended for JavaScript-heavy pages)
2. `alibaba_rfq_scraper_requests.py` - Alternative scraper using Requests and BeautifulSoup
3. `requirements.txt` - Python dependencies
4. `README.md` - This file

## Installation

1. Install Python 3.7 or higher
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. For the Selenium version, Chrome browser will be automatically downloaded via webdriver-manager

## Usage

### Option 1: Selenium Scraper (Recommended)

```bash
python alibaba_rfq_scraper.py
```

### Option 2: Requests Scraper

```bash
python alibaba_rfq_scraper_requests.py
```

## CSV Output Format

The scraped data will be saved to a CSV file with the following columns:

- **RFQ_ID**: Unique identifier for the RFQ
- **Title**: Title/name of the RFQ
- **Buyer_Country**: Country of the buyer (e.g., AE for UAE)
- **Buyer_Name**: Name of the buying company
- **Posted_Date**: Date when the RFQ was posted
- **Expiry_Date**: Expiry date of the RFQ
- **Category**: Product category or industry
- **Quantity**: Required quantity
- **Unit**: Unit of measurement
- **Description**: Detailed description of the requirement
- **Contact_Info**: Contact information
- **Status**: Current status of the RFQ
- **Keywords**: Associated keywords or tags

## Configuration

You can modify the following parameters in the scripts:

- `max_pages`: Maximum number of pages to scrape (default: 50)
- `base_url`: The target URL
- `params`: URL parameters for filtering

## Target URL

The scraper targets: `https://sourcing.alibaba.com/rfq/rfq_search_list.htm?spm=a2700.8073608.1998677541.1.82be65aaoUUItC&country=AE&recently=Y&tracelog=newest`

## Anti-Detection Features

- Random delays between requests (2-7 seconds)
- Random user agents
- Session management
- Error handling and retry logic
- Headless browser mode (Selenium)

## Troubleshooting

### Common Issues

1. **No data scraped**: The website structure might have changed. Check the console output for error messages.

2. **Chrome driver issues**: The Selenium version automatically downloads Chrome driver. If you encounter issues, ensure Chrome browser is installed.

3. **Rate limiting**: If you get blocked, increase the delay between requests or use a VPN.

4. **Empty results**: The website might require authentication or have anti-bot measures. Try the alternative scraper.

### Debug Mode

To see what's happening, you can modify the scripts to run in non-headless mode by commenting out the `--headless` option in the Chrome options.

## Output Files

The scraper generates CSV files with timestamps:
- `alibaba_rfq_data_YYYYMMDD_HHMMSS.csv` (Selenium version)
- `alibaba_rfq_data_requests_YYYYMMDD_HHMMSS.csv` (Requests version)

## Legal Notice

This scraper is for educational purposes only. Please ensure you comply with Alibaba's terms of service and robots.txt file. Use responsibly and respect rate limits.

## Requirements

- Python 3.7+
- Chrome browser (for Selenium version)
- Internet connection
- Sufficient disk space for CSV output

## Dependencies

- requests
- beautifulsoup4
- pandas
- selenium
- webdriver-manager
- lxml
- fake-useragent 

⚠️ **Disclaimer:**
This project is intended for educational use only. Please ensure that scraping any website using this tool is done in compliance with its Terms of Service and relevant laws. The author assumes no responsibility for misuse.