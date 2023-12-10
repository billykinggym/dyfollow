from typing import Optional, List

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium import webdriver

class BrowserWrapper:
	def __init__(self):
		self.driver:WebDriver= self.init_driver()
		self.driver.implicitly_wait(10)

	def init_driver(self) -> WebDriver :
		options = Options()
		# options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36')
		options.add_argument(
			'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
		return webdriver.Chrome(options)

	def get(self,url):
		self.driver.get(url)

	def find_element(self, by=By.ID, value: Optional[str] = None) -> WebElement:
		return self.driver.find_element(by,value)

	def find_elements(self, by=By.ID, value: Optional[str] = None) -> List[WebElement]:
		return self.driver.find_elements(by,value)

# driver.set_window_size(400, 811)