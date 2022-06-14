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
	for i in range(len(lyst)-1, -1, -1):
		f.write(lyst[i].getMovieName())
		f.write("\n")
		f.write(lyst[i].getMovieTime())
		f.write("\n")
		f.write("Theater Number: ")
		f.write(str(lyst[i].getTheaterNum()))
		f.write("\n")
		f.write("Lux Box Seats:")
		f.write(str(lyst[i].getSoldSeats()))
		f.write("\n")
		f.write("\n")

def getCaryLocation(driver):
	locations = driver.find_element(By.CLASS_NAME, "subNavContainer")
	locations.click()
	locations1 = driver.find_elements(By.ID, "theaterBox")
	parkside = locations1[5]
	return parkside

def getMovieDataLists(movie_box):
	list_of_lists = []
	for i in range(len(movie_box)):
		times_box = movie_box[i].find_elements(By.ID, "comment")
		for j in range(len(times_box)):
			seat_type = times_box[j].find_element(By.TAG_NAME, "div").text.split()
			first_word = seat_type[0]
			inner_list = []
			if first_word == "LUX":
				inner_list.append(i)
				inner_list.append(j)
				num_times = len(times_box[j].find_elements(By.CLASS_NAME, "view"))
				inner_list.append(num_times)
				list_of_lists.append(inner_list)
	return list_of_lists

def populateMovieObjList(list_of_lists, parkside_url):
	list_of_movies = []
	for movie in list_of_lists:
		for time in range(movie[2]):
			movie[2] -= 1
			try:
				movie_name, showing_time, theater_num, sold_seats = scrapeSeats(movie[0], movie[1], movie[2], parkside_url)
				movie_obj = Movie(movie_name, showing_time, theater_num, sold_seats)
				list_of_movies.append(movie_obj)
			except:
				pass
	return list_of_movies

def main():
	
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')

	# Current chromedriver version is v102 for Chrome version 102
	driver = webdriver.Chrome(".\chromedriver.exe", chrome_options=options)
	url = "https://www.paragontheaters.com/"
	driver.get(url)

	# Go to the Cary Parkside Location
	getCaryLocation(driver).click()

	parkside_url = driver.current_url
	print("Working URL:",parkside_url)

	# Find each showtime and create list
	movie_box = driver.find_elements(By.ID, "showtimes_movie")

	# Create list of movie data
	list_of_lists = getMovieDataLists(movie_box)

	driver.quit()

	# Create list of Movie objects
	list_of_movie_objs = populateMovieObjList(list_of_lists, parkside_url)

	# Print notice of success
	print("\nSuccess!\n")

	# Print movie data to console
	for i in list_of_movie_objs:
		print(i)
		print()

	# Write movie data to text file in order
	writeToFile(list_of_movie_objs)

if __name__ == "__main__":
	main()


