'''
	Author: Carson Pribble
	File: main.py
	Purpose: Scrape each movie at paragontheaters website at the Parkside location for the number of 'LuxBox' 
		seats that are sold when the program is run. This automates a task that takes an employee
		around 20 minutes to complete every hour and is very useful for busy weekend days.
		Requires selenium webdriver to be in PATH 
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import requests
import time

# This function performs one scrape on one showtime. This function should be used in an iteration over each movies showtimes
def scrapeSeats(movie, section, movie_time, url):
	'''
	Must change path to the correct location of chromedriver.exe if using code pulled from github. Current version
		being used is v102 for Chrome version 102
	driver = webdriver.Chrome("D:\Code_Practice\python_modules\selenium_v101\chromedriver.exe")
	'''
	
	driver = webdriver.Chrome(".\chromedriver.exe")

	purl = url
	driver.get(purl)

	# Gets all movies, the theater showtimes are children of showtimes_movie called 'comment'
	showtimes = driver.find_elements(By.ID, "showtimes_movie")

	movie = int(movie)
	sec = int(section)
	movie_time = int(movie_time)

	theater_type = showtimes[movie].find_elements(By.ID, "comment")

	times = theater_type[sec].find_elements(By.CLASS_NAME, "view")
	
	times[movie_time].click()

	# Changes drivers control to the newly opened window
	WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
	child = driver.window_handles[1]
	driver.switch_to.window(child)
	time.sleep(1)

	# Gets movie title (per each time though)
	movie_name = driver.find_element(By.CLASS_NAME, "movie-title").text


	# Gets time of the showing
	showing_time = driver.find_element(By.CLASS_NAME, "session-time").text.split()[-1]

	# Gets auditorium number for lux_seat section being 2 or 3
	theater_num = driver.find_element(By.CLASS_NAME, "cinema-screen-name").text.split()[-1]

	if str(theater_num) == '1' or theater_num == '11':
		section_id = 2
	else:
		section_id = 3

	# Adds a ticket and clicks the next button
	sections = driver.find_elements(By.CLASS_NAME, "item ")
	section = sections[0]
	btn = section.find_element(By.CLASS_NAME, "plus")
	btn.click()
	next_btn = driver.find_element(By.ID, "ibtnOrderTickets")
	next_btn.click()
	time.sleep(1)

	page_source = driver.page_source
	soup = bs(page_source, 'html.parser')

	lux_section = soup.find(id=section_id)
	rows = lux_section.find_all("tr")

	sold_seats = 0

	for row in rows:
		tds = row.find_all("td")
		for td in tds:
			if len(td.text.strip()) > 0:
				seat_value = td.find("img")["data-type"]
				if seat_value.strip() == "Sold":
					sold_seats += 1
	
	# Cancels the order to not trick the website into thinking there is an open order to reserve the seat
	cancel_btn = driver.find_element(By.CLASS_NAME, "clear")
	cancel_btn.click()

	time.sleep(1)

	driver.quit()
	return movie_name, showing_time, theater_num, sold_seats

