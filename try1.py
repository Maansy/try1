from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

driver = webdriver.Chrome('/home/abdulrahman/Downloads/chromedriver-linux64/chromedriver')

try:
    def scrape_page(soup):
        title_non = soup.find_all('ul', {'class': 'listing'})[0].find_all('li')
        for title in title_non:
            article = title.find('div', {'class': 'text'}).find('a')
            if article:
                article_text = article.text.strip()
                print(article_text)
                article_link = 'https://www.shorouknews.com' + article.get('href')
                print(article_link)

    base_url = "https://www.shorouknews.com/art"
    driver.get(base_url)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    print("Page 1:")
    scrape_page(soup)

    for page_number in range(2, 6):

        page_number_to_click = str(page_number)
        button_xpath = f"//a[text()='{page_number_to_click}']"
        button_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, button_xpath)))

        # Scroll the button into view
        actions = ActionChains(driver)
        actions.move_to_element(button_element).perform()

        button_element.click() # Click the button

        # Wait until ul changes
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='listing']")))

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        print(f"Page {page_number}:")
        scrape_page(soup)

finally:
    # Close the driver when done or if an exception occurs
    driver.quit()
