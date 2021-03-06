from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from typing import Union

from exceptions.exceptions import UnsupportedLocation

def _get_web_elements(driver, location : str) -> list:
    
    if location not in ["england", "wales", "scotland", "northern-ireland"]:
        raise UnsupportedLocation(location)
        
    driver.get(f"https://www.scaleupinstitute.org.uk/scaleup-companies-{location}/")
    
    if location == "england":
        xpath = "//div[@class='col-6']//p"
    else :
        xpath = "//div[@class='col-lg-6']//p"
    
    web_elements= driver.find_elements_by_xpath(xpath)
        
    return web_elements


def _clean_locations(locations: Union[str, list]) -> list:
    
    if isinstance(locations, str):
        locations = [locations]
    
    locations = [x.strip().lower() for x in locations]
    
    return locations


def get_companies(locations : list = ["wales", "scotland", "northern-ireland", "england"], 
                  path_driver : Union[str,None] = None) -> list:
    
    locations = _clean_locations(locations)
    companies = []
    
    for location in locations:
        
        if not path_driver:
            driver = webdriver.Chrome(ChromeDriverManager().install())          
        else:
            driver = driver = webdriver.Chrome('path_driver')
        
        driver.implicitly_wait(10)
        web_elements = _get_web_elements(driver, location)
        output = [element.text.split('\n') for element in web_elements]
        output = [x for sublist in output for x in sublist]
        
        companies = companies + output
        driver.close()
    
        
    return companies








