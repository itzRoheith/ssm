import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import subprocess

URL = "https://ssmetrust.in/SSM63/Parent_portal/parent_publish/circularboostrs.aspx?admno=1979&pwd=Sanjeev&year=2024-25"

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Start the timer
start_time = time.time()

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(URL)

    # 🚀 Wait up to 10 seconds for at least one PDF link to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href$='.pdf']"))
        )
    except:
        print("Timeout: No PDF links found within 10 seconds.")
        driver.quit()
        exit(0)

    # 🚀 Extract PDF Links Faster
    pdf_links = [elem.get_attribute("href") for elem in driver.find_elements(By.CSS_SELECTOR, "a[href$='.pdf']")]

    driver.quit()

    if pdf_links:
        print("Extracted PDF Links:", pdf_links)
        with open("pdf_links.txt", "w") as f:
            f.writelines(link + "\n" for link in pdf_links)

        subprocess.run(["gitcommit.cmd"], check=True)
    else:
        print("No PDF links found.")
        exit(0)

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    try:
        driver.service.process.kill()
    except NameError:
        pass

# Stop the timer and print execution time
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Code finished in {elapsed_time:.2f} seconds")
