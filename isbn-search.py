import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()

with open('output.txt', 'r') as file:
    lines = file.read().splitlines()

for line in lines:
    #print(line)
    #time.sleep(5)
    driver.get(f"https://sclib.svkk.sk/sck01/Search/Results?lookfor={line}")
    WebDriverWait(driver, 10)
    if (driver.find_element(By.CLASS_NAME, "search-stats").text == "No Results!"):
        #print(f"Nebolo možné nájsť: {line}")
        with open('book_data.txt', 'a') as file:
            file.write(f"Nebolo možné násjť: {line}; ; ; ; {line}" + "\n")
        #driver.close()
    else:
        value = driver.find_element(By.CSS_SELECTOR, '.hiddenId').get_attribute('value')
        #print(value)
        driver.get(f"https://sclib.svkk.sk/sck01/Record/{value}")
        WebDriverWait(driver, 10)

        bookName = driver.find_element(By.CSS_SELECTOR, 'h3[property="name"]').text
        
        author_elements = driver.find_elements(By.CSS_SELECTOR, '.author-data')
        author_data = [element.text for element in author_elements]
        joined_author_data = ', '.join(author_data)

        published_element = driver.find_element(By.XPATH, '//tr[th[contains(text(), "Published:")]]/td')

        # Extract the text content of the element
        published_text = published_element.text

        # Split the text into date and publisher name
        # Assuming the format is "Publisher Name, Year"
        split_text = published_text.split(',')
        date_published = split_text[-1].strip() # Extract the year
        publisher_name = ', '.join(split_text[:-1]).strip() # Extract the publisher name

        #print(bookName, joined_author_data, date_published, publisher_name)
        #driver.close()
        
        data_line = f"{bookName}; {joined_author_data}; {date_published}; {publisher_name}; {line}"

        # Write the data line to a text file
        with open('book_data.txt', 'a') as file:
            file.write(data_line + "\n")
driver.close()
# Data loading into excel : https://www.indeed.com/career-advice/career-development/how-to-import-text-file-into-excel