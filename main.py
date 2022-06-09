'''
	Author: Carson Pribble
	File: main.py
	Purpose: This is the main file for the paragon luxbox seatscraper. It will call the
		scrapeSeats method for each time for each movie that has luxbox seating available.
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from movie_object import Movie
from seat_check import scrapeSeats

# add method to write to file
def writeToFile(lyst):
	f = open('lux_box_seats.txt', 'w')
	for i in lyst:
		f.writelines(i)
	
	
def main():
	list_of_movies = []

	# Current chromedriver version is v102 for Chrome version 102
	driver = webdriver.Chrome(".\chromedriver.exe")
	url = "https://www.paragontheaters.com/"
	driver.get(url)

	# go to the Cary Parkside Location
	locations = driver.find_element(By.CLASS_NAME, "subNavContainer")
	locations.click()
	locations1 = driver.find_elements(By.ID, "theaterBox")
	parkside = locations1[5]
	parkside.click()

	parkside_url = driver.current_url
	print(parkside_url)

	movies_obj_list = driver.find_elements(By.ID, "showtimes_movie")

	list_of_lists = []

	for i in range(len(movies_obj_list)):
		sections_obj_list = movies_obj_list[i].find_elements(By.ID, "comment")
		for j in range(len(sections_obj_list)):
			seat_type = sections_obj_list[j].find_element(By.TAG_NAME, "div").text.split()
			first_word = seat_type[0]
			last_word = seat_type[-1]
			inner_list = []
			if first_word == "LUX":
				inner_list.append(i)
				inner_list.append(j)
				#list_of_lists.append(inner_list)
				#for h in range(len())
				num_times = len(sections_obj_list[j].find_elements(By.CLASS_NAME, "view"))
				inner_list.append(num_times)
				list_of_lists.append(inner_list)

	driver.quit()


	# POSSIBLE FIX BUT CREATED AN ERROR. MUST RUN scapeSeats on each time not just the first time in each section of each movie -_-
	for movie in list_of_lists:
		for time in range(movie[2]):
			movie[2] -= 1
			try:
				movie_name, showing_time, theater_num, sold_seats = scrapeSeats(movie[0], movie[1], movie[2], parkside_url)
				movie_obj = Movie(movie_name, showing_time, theater_num, sold_seats)
				list_of_movies.append(movie_obj)
			except:
				pass

	for i in list_of_movies:
		print(i)
		print()

if __name__ == "__main__":
	main()


