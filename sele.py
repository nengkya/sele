import os
import pandas as pd
import csv

from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class Se:
	def components():
		options = webdriver.EdgeOptions()
		options.add_argument("start-maximized");
		options.add_argument("disable-infobars")
		options.add_argument("--disable-extensions")
		driver = webdriver.Edge(options=options)
		driver.get('https://www.customs.go.th/statistic_report.php?lang=en&')
		title = driver.title
		assert title == "Thai Customs"

		f = open("230430 230430 HS Codes.txt", "r")

		for hs_code in f:

			hs_code = f.readline()

			text_box = driver.find_element(by=By.NAME, value="tariff_code")

			text_box.send_keys(hs_code)

			text_box2 = driver.find_element(by=By.NAME, value="imex_type")

			text_box2.send_keys(Keys.ARROW_DOWN)

			WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form[1]/div[3]/div[1]/div[2]/div[1]/table[1]/tbody[1]/tr[7]/td[2]/button[1]"))).click()

			soup = BeautifulSoup(driver.page_source, features = "html.parser")

			df_pandas=pd.read_html(driver.page_source, attrs={'class':'table-bordered'},flavor='html5lib')

			rows = df_pandas[2].values.tolist()

			a_tab = SoupStrainer('li',{'class': 'active'})
			soup1 = BeautifulSoup(driver.page_source, features = "html.parser", parseOnlyThese = a_tab)
			a = soup1.find('a')

			filename = hs_code.strip() + ".csv"
				
			#writing to csv file 
			with open(filename, 'w') as csvfile: 
				#creating a csv writer object 
				csvwriter = csv.writer(csvfile) 

				csvwriter.writerow(list(df_pandas[2]))
					
				#writing the data rows
				for i in range(0, len(rows)):
					csvwriter.writerow(rows[i])

		f.close()
		driver.quit()

if __name__ == '__main__':
	os.system('tput reset')

	Se.components()
