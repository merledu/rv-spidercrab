from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import shutil
import os
import sys
import subprocess


def Book_Resource(query) -> list:
	try:
		# Set up the WebDriver (make sure you have the appropriate WebDriver executable in your PATH)
		driver = webdriver.Chrome()  # You can use other drivers like Firefox or Edge	
		# Define the search query	
		# Open Google and perform the search
		driver.get("https://www.google.com")
		search_box = driver.find_element("name", "q")  # Using find_element with name selector
		search_box.send_keys(query)
		search_box.send_keys(Keys.RETURN)	
		# Wait for search results to load
		time.sleep(2)	
		# Extract and print search results
		pdfList = []
		search_results = driver.find_elements("css selector", ".tF2Cxc")
		
		while True:
			for result in search_results:
				if str(result.find_element("css selector", "a").get_attribute("href")).endswith(".pdf"):
					link = result.find_element("css selector", "a").get_attribute("href")
					if str(link) not in pdfList:
						pdfList.append(str(link))
			try:
				driver.find_element("id","pnnext").click()
				time.sleep(2)
				search_results = driver.find_elements("css selector",".tF2Cxc")

			except:
				break
	except WebDriverException:
		print("\033[0;31mInternet Service is not available")

		

	# Close the browser window
	driver.quit()
	file = open("BooksLinks.txt","w").close()
	file = open("BooksLinks.txt","a")
	for link in pdfList:
		file.write(link+"\n")

def Research_Paper_Resource(query):
	try:
		ResearchList = []
		# Set up the WebDriver (make sure you have the appropriate WebDriver executable in your PATH)
		driver = webdriver.Chrome()  # You can use other drivers like Firefox or Edge	
		# Define the search query	
		# Open Google and perform the search
		driver.get("https://scholar.google.com/")
		search_box = driver.find_element("name", "q")  # Using find_element with name selector
		search_box.send_keys(query)
		search_box.send_keys(Keys.RETURN)	
		# Wait for search results to load
		time.sleep(4)
		# Extract search results
		search_results = driver.find_elements("css selector",".gs_r.gs_or.gs_scl")
		time.sleep(2)
		while True:
			for result in search_results:
				if str(result.find_element("css selector", "a").get_attribute("href")).endswith(".pdf") or \
					"pdf" in str(result.find_element("css selector", "a").get_attribute("href")):
					link = result.find_element("css selector", "a").get_attribute("href")
				
					if str(link) not in ResearchList:
						ResearchList.append(str(link))

			try:
				next_button = driver.find_element('xpath','//*[@id="gs_n"]/center/table/tbody/tr/td[12]/a')
				next_button.click()
				time.sleep(4)
				search_results = driver.find_elements("css selector",".gs_r.gs_or.gs_scl")
				time.sleep(2)
    		
			except:
				break

	except WebDriverException:
		print("\033[0;31mInternet Service is not available")
	
	# Close the browsing window
	driver.quit()
	file = open("ResearchLinks.txt","w").close()
	file = open("ResearchLinks.txt","a")
	for link in ResearchList:
		file.write(link+"\n")

		

def Download_books(links_file_path:list):
	shell_command = f'file="{links_file_path}"; while read -r line; do wget "$line"; done < "$file"'
	subprocess.run(shell_command, shell=True)


Book_Resource("Free RISC-V Books pdf")
#Research_Paper_Resource("Risc-v Research Papers")
#if "-d" in sys.argv:
#	Download_books(pdflist)
