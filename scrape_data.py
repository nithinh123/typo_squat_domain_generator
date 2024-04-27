"""
    Module for getting report of a domain of your choice
    from https://dnstwister.report and scrape the required 
    details.

"""
import re
import idna
import binascii
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DNSTWISTER_ENDPOINT = "https://dnstwister.report"
SUPPORTED_BROWSERS = ["chrome", "firefox", "edge"]


class ScrapeData:
    """
    A class to scrap data from dnsteister website

    ...

    Attributes
    ----------
    domain : str
        domain url that need to be searched for 
        Typosquatting related entries
    browser : str
        name of the browser that is supported.
        supported browsers are: 
        1) firefox 
        2) chrome
        3) edge

    Methods
    -------
    get_driver():
        get the driver for supported browser

    scrap_domain_data():
        scrap domain data of the domain that is passed
    """

    def __init__(self, domain: str, browser: str):
        self.domain = domain
        self.browser = browser

    def get_driver(self):
        """
            This method checks for the driver input and 
            returns the driver if it is supported

        Returns:
            Returns a status(boolean) and 
            driver details if browser is supported 
            or message if it is not supported
        """
        if self.browser in SUPPORTED_BROWSERS:
            if self.browser == "chrome":
                return True, webdriver.Chrome()
            elif self.browser == "edge":
                return True, webdriver.Edge()
            elif self.browser == "firefox":
                return True, webdriver.Firefox()
        return False, f"{self.browser} browser is not supported"

    def encode_domain_name(self) -> str:
        """
            This method returns encoded domain name for API usage
        
        """
        return binascii.hexlify(self.domain.encode()).decode()
    
    def scrape_domain_data(self) -> dict:
        """
            This method connects to browser and get domain
            related data from dnstwist website

        Returns:
            Returns a dictionary with status(boolean),
            a list of dictionary containing domain and ip,
            and message regarding the status

            Eg: 
                {"status": True,
                "data":[{'domain': 'www.google.com','ip': '172.217.16.228'},
                {'domain': 'login-google.com','ip': '199.231.164.178'}],
                "message": "Scraping completed successfully"}

            Eg:

                if browser not supported:

                {"status": False, "data":[],"message":"safari browser is not supported"}

                if some exception occurs:

                {"status": False, "data":[], "message":"Exception: <exception reason>"}
        """
        try:
            encoded_domain = self.encode_domain_name()
            url = f"{DNSTWISTER_ENDPOINT}/search?ed={encoded_domain}"
            status, driver = self.get_driver()
            if status:
                driver.get(url)
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.LINK_TEXT, "export csv")))
                scrape_data = driver.find_elements_by_xpath('//tr[@class="domain-row resolved"]')
                processed_data = []
                for item in enumerate(scrape_data):
                    data = re.sub(r'\([^)]*\)', '', item[1].text)
                    data = data.replace('\n', ' ')
                    data = data.split(" ")
                    data = [x for x in data if x]
                    puny_code = idna.encode(data[0]).decode()
                    processed_data.append(
                        {
                        "domain": data[0], 
                        "puny_code_domain": puny_code if puny_code != data[0] else "",
                        "ip": data[1]
                        }
                    )
                driver.quit()
                return {"status": True, "data": processed_data,
                        "message": "Scraping completed successfully"}
            return {"status": False, "data": [], "message": driver}
        except Exception as e:
            return {"status": False, "data": [],"message": f"Exception: {str(e)}"}
