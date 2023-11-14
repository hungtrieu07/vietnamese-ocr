from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm

# Create a new instance of the Chrome web driver
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "/home/hungtrieu07/Downloads/vietnamese-ocr/downloaded_pdf"}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=chrome_options)

# Open a new tab
driver.execute_script("window.open('', '_blank');")
driver.switch_to.window(driver.window_handles[1])

# Navigate to the page with the list of documents
driver.get(
    "https://www.thudo.gov.vn/documentlist.aspx?lvb=a6da96dd-8e49-1b4b-b641-00bff73c688a")

page_count = 811    # Số tự set bằng tay

# Initialize tqdm for tracking page progress
page_progress_bar = tqdm(total=page_count, desc='Processing Page', unit='page')

# Loop through each page
for page in range(1, page_count + 1):
    # Find all the elements with class "vanbanitem_sovanban" on the current page
    elements = driver.find_elements(By.CLASS_NAME, "vanbanitem_sovanban")

    element_progress_bar = tqdm(
        total=len(element), desc='Processing Elements', unit='element')

    # Loop through each element on the current page
    for i in range(len(elements)):
        # Re-find the elements before interacting with them
        elements = driver.find_elements(By.CLASS_NAME, "vanbanitem_sovanban")

        if i >= len(elements):
            break  # Break out of the loop if all elements have been processed

        element = elements[i]

        # Click the element to access the document page
        element.click()
        driver.implicitly_wait(5)  # Adjust the timing if needed

        # Capture the current URL before clicking
        original_url = driver.current_url

        # Check if the URL has changed (indicating redirection to the homepage)
        if driver.current_url == original_url:
            # If the URL is the same, navigate back to the original URL
            driver.get(original_url)

            js_code = "javascript:__doPostBack('dnn$ctr685$View$rptFileAttach$ctl00$lbtDownLoadAttach','');"
            driver.execute_script(js_code)
            # Find the PDF download link inside the <li> tag
            driver.execute_script("window.history.go(-1)")

        element_progress_bar.update(1)

    element_progress_bar.close()

    if page < page_count:
        # Find the ">" link and click it
        next_page_link = driver.find_element(
            By.XPATH, "//a[contains(text(), '>')]")
        next_page_link.click()

        # Wait for the page to load (you can adjust the timing if needed)
        driver.implicitly_wait(5)

    # Re-find the elements for the next page
    elements = driver.find_elements(By.CLASS_NAME, "vanbanitem_sovanban")

    page_progress_bar.update(1)

page_progress_bar.close()

# Close the tab with the document page
driver.close()

# Switch back to the original tab (main page)
driver.switch_to.window(driver.window_handles[0])

# Close the main tab
driver.quit()
