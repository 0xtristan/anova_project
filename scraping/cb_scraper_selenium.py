from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import time

def download_csv_large():
    # Download csv
    browser.find_element_by_xpath('//button[@aria-label="Export your results"]').click()
    time.sleep(1)
    browser.find_element_by_xpath('//button[@aria-label="Export to CSV"]').click()

    try:
        element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//mat-dialog-actions/div/button[@class="mat-button"]'))
        )
        element.click()
    except:
        print('Timeout waiting for download confirmation window')

def download_csv():
    # Download csv
    browser.find_element_by_xpath('//button[@aria-label="Export your results"]').click()
    time.sleep(1)
    browser.find_element_by_xpath('//button[@aria-label="Export to CSV"]').click()

dir_path = os.path.dirname(os.path.realpath(__file__))

# Fill in your details here to be posted to the login form.
payload = {
    'inUserName': 'jeffrey.paine@gmail.com',
    'inUserPass': 'modelSs5'
}

base_url = 'https://www.crunchbase.com'

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
  "download.default_directory": dir_path+"/cb_csv",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
browser = webdriver.Chrome(chrome_options=options)
# Log in to CB
browser.get(base_url+'/login')
browser.find_element_by_id('mat-input-1').send_keys(payload['inUserName'])
browser.find_element_by_id('mat-input-2').send_keys(payload['inUserPass']+'\n')
time.sleep(2)

# Scrape investors page
browser.get(base_url+'/search/principal.investors')

download_csv_large()

soup = BeautifulSoup(browser.page_source, 'html.parser')
investor_list = []
# Bit of a hack but idk how else to differentiate the title col from the location col
for investor_cell in [x for x in soup.find_all('a', role='link') if x['href'][1]=='o'][:10]:
    investor_info_url = base_url+investor_cell['href']
    investor_exits_url = base_url+'/search/organizations/field/organizations/num_exits/'+investor_info_url.split('/')[2]
    investor_title = investor_cell['title']
    investor_list.append(investor_title)
    #print('Now visiting: '+str(investor_title)+' at url: '+str(investor_exits_url))
    #browser.get(investor_exits_url)

# This accesses our pre-made search
browser.get('https://www.crunchbase.com/lists/investor-search/cafb51b3-9566-46c7-b29d-47ab9a2e62fc/organizations')

# Now to fill in the search bar for each investor
for investor_name in investor_list:
    search_bar = browser.find_element_by_xpath('//input[@placeholder="Accel, Marc Benioff"]')
    search_button = browser.find_element_by_xpath('//button[@aria-label="Search"]')
    search_bar.clear()
    search_bar.send_keys(investor_name)
    search_button.click()

    # Wait for search to load
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'grid-row'))
        )
    except:
        print('Timeout waiting for search to return results')
    download_csv()
    browser.implicitly_wait(3)
