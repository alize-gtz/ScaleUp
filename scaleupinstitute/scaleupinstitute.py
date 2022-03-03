from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome(ChromeDriverManager().install())

def _get_web_elements(locations : list = ["england", "wales", "scotland", "northern-ireland"]) -> list:
    web_elements = []
    for  location in locations:
        driver.get(f"https://www.scaleupinstitute.org.uk/scaleup-companies-{location}/")
        xpath = "//div[@id='visible_scaleups_response']//p[@class = 'mb-2']"
        web_elements.append(driver.find_elements_by_xpath(xpath))
        
        driver.quit()
        WebDriverWait(driver, timeout=3)
        
    return web_elements

def get_companies(locations : list = ["england", "wales", "scotland", "northern-ireland"]) -> list:
    web_elements = _get_web_elements(locations)
    return [element.text for element in web_elements]


