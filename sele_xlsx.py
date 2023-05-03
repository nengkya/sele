import os
import fnmatch

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class Se:
	def __init__(self, hs_code):
		self.hs_code = hs_code

	def components(self):
		options = webdriver.EdgeOptions()
		options.add_argument("start-maximized");
		options.add_argument("disable-infobars")
		options.add_argument("--disable-extensions")
		driver = webdriver.Edge(options=options)
		driver.get('https://www.customs.go.th/statistic_report.php?lang=en&')
		title = driver.title
		assert title == "Thai Customs"

		driver.implicitly_wait(1)

		#create action chain object
		action = ActionChains(driver)

		text_box = driver.find_element(by=By.NAME, value="tariff_code")
		text_box.send_keys(self.hs_code)

		driver.implicitly_wait(1)

		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form[1]/div[3]/div[1]/div[2]/div[1]/table[1]/tbody[1]/tr[7]/td[2]/button[3]"))).click()
		action.pause(5)
		#perform the operation
		action.perform()

		for file in os.listdir('.'):
			if fnmatch.fnmatch(file, 'Statistic*.txt'):
				print(file)

		driver.quit()

if __name__ == '__main__':
	os.system('tput reset')

	f = open("230430 230430 HS Codes.txt", "r")

	for hs_code in f:

		hs_code = f.readline()

		Se(hs_code).components()

	f.close()
