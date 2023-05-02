import os
from selenium import webdriver
from selenium.webdriver.common.by import By

#for input text in html form
from selenium.webdriver.common.keys import Keys

#click
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#extract form submit result
from bs4 import BeautifulSoup, SoupStrainer

import pandas as pd
import csv


def test_eight_components():
	options = webdriver.EdgeOptions()
	options.add_argument("start-maximized");
	options.add_argument("disable-infobars")
	options.add_argument("--disable-extensions")

	driver = webdriver.Edge(options=options)

	driver.get('https://www.customs.go.th/statistic_report.php?lang=en&')

	title = driver.title
	assert title == "Thai Customs"

	text_box = driver.find_element(by=By.NAME, value="tariff_code")

	hs_code = "39011012000"

	text_box.send_keys(hs_code)

	WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form[1]/div[3]/div[1]/div[2]/div[1]/table[1]/tbody[1]/tr[7]/td[2]/button[1]"))).click()

	soup = BeautifulSoup(driver.page_source, features = "html.parser")

	df_pandas=pd.read_html(driver.page_source, attrs={'class':'table-bordered'},flavor='html5lib')

	newdf = df_pandas.copy()

	df_pandas.applymap('{:,.0f}'.format)

	print(list(df_pandas[2]))

	####################
	#data of csv file
	for table in range(1, len(df_pandas)):
		rows = df_pandas[table].values.tolist()

		#name of csv file
		a_tab = SoupStrainer('li',{'class': 'active'})

		soup1 = BeautifulSoup(driver.page_source, features = "html.parser", parseOnlyThese = a_tab)

		a = soup1.find('a')

		filename = str(a.string) + " table " + str(table) + ".csv"
			
		#writing to csv file 
		with open(filename, 'w') as csvfile: 
			#creating a csv writer object 
			csvwriter = csv.writer(csvfile) 

			if table == 2:
				csvwriter.writerow(list(df_pandas[table]))
				
			#writing the data rows
			for i in range(0, len(rows)):
				csvwriter.writerow(rows[i])

		df=pd.read_csv('filename.csv', thousands=',')
	##############






	driver.quit()


if __name__ == '__main__':
	os.system('tput reset')

	test_eight_components()
