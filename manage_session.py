from playwright.sync_api import sync_playwright

def scrape_quotes(page):
    page.goto("https://quotes.toscrape.com/")
    
    quotes = page.query_selector_all(".quote")  # Find all quotes on the page
    for quote in quotes:
        text = quote.query_selector(".text").inner_text()
        author = quote.query_selector(".author").inner_text()
        print(f"Quote: {text}\nAuthor: {author}\n")
    
    # Handle pagination (if necessary)
    next_button = page.query_selector('li.next > a')
    if next_button:
        next_button.click()
        scrape_quotes(page)  # Recursive call for the next page

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        scrape_quotes(page)
        browser.close()

if __name__ == "__main__":
    main()
