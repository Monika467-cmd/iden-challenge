import json
import codecs
from playwright.sync_api import sync_playwright

def fix_quotes_and_decode(text):
    # Decode any escaped Unicode characters
    text = codecs.decode(text, 'unicode_escape')
    
    # Manually replace incorrect encoding characters
    text = text.replace('â', '“').replace('â', '”')  # Fix quotes
    text = text.replace('â', '‘').replace('â', '’')  # Fix apostrophes
    
    return text

def scrape_products():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch browser in headless mode
        page = browser.new_page()
        page.goto("https://quotes.toscrape.com/")  # URL of the quotes website

        # Wait for the quotes to load (adjust selector as needed)
        page.wait_for_selector('.quote')

        # Extract product information
        products = []
        quotes = page.query_selector_all('.quote')
        
        for quote in quotes:
            text = quote.query_selector('.text').inner_text()
            author = quote.query_selector('.author').inner_text()
            tags = quote.query_selector('.tags').inner_text().replace("Tags: ", "")  # Remove "Tags: "
            
            # Fix quotes and decode text
            text = fix_quotes_and_decode(text)

            products.append({
                'quote': text,
                'author': author,
                'tags': tags
            })

        # Save data to JSON file
        with open('products_data.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)

        print("Products have been saved successfully!")

# Run the function
scrape_products()
