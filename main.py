'''
Author: Carson Pribble
File: main.py
Purpose: This is the main file for the paragon luxbox seatscraper. It will call the
	scrapeSeats method for each time for each movie that has luxbox seating available.
	Contains methods to print and write each Movies objects string as well as methods
	to print and write the data needed by Paragon Theaters to predict volume.
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from movie_object import Movie
from seat_check import scrapeSeats

# Writes to file the list of movie objects string
def writeToFileAsList(lyst):
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

# Writes to file the formatted data for Paragon
def writeToFileFormatted(list_of_movie_objs):
	f = open('lux_box_seats.txt', 'w')
	movie_names = []
	list_of_times_of_movie = []
	list_of_sold_seats = []
	for i in range(len(list_of_movie_objs)):
		movie_name = list_of_movie_objs[i].getMovieName()
		if movie_name not in movie_names:
			movie_names.append(movie_name)
	for i in range(len(movie_names)):
		times_of_movie = []
		sold_seats = []
		for movie in list_of_movie_objs:
			if str(movie.getMovieName()) == str(movie_names[i]):
				times_of_movie.append(movie.getMovieTime())
				sold_seats.append(movie.getSoldSeats())
		list_of_times_of_movie.append(times_of_movie)
		list_of_sold_seats.append(sold_seats)
	for i in range(len(movie_names)):
		f.write(movie_names[i])
		f.write("\n")
		for j in range(len(list_of_times_of_movie[i])):
			f.write("{} - {}".format(list_of_times_of_movie[i][j], list_of_sold_seats[i][j]))
			f.write("\n")
		f.write("\n")	

# Uses webdriver to find the html button for the Cary Parkside location
def getCaryLocation(driver):
	locations = driver.find_element(By.CLASS_NAME, "subNavContainer")
	locations.click()
	locations1 = driver.find_elements(By.ID, "theaterBox")
	parkside = locations1[5]
	return parkside

# Returns a lists of lists, each list contains the indexes for: movie, box of times and time.
def getMovieDataLists(movie_box):
	list_of_lists = []
	for i in range(len(movie_box)):
		times_box = movie_box[i].find_elements(By.ID, "comment")
		for j in range(len(times_box)):
			seat_type = times_box[j].find_element(By.TAG_NAME, "div").text.split()

			# TESTING FOR LUX PRESENT NOT LUX FIRST WORD - SLOWER
			#first_word = seat_type[0]
			inner_list = []
			#if first_word == "LUX":

			if "LUX" in seat_type:
				inner_list.append(i)
				inner_list.append(j)
				num_times = len(times_box[j].find_elements(By.CLASS_NAME, "view"))
				inner_list.append(num_times)
				list_of_lists.append(inner_list)
	return list_of_lists

# Uses the list of indexes to scrape movie from each time in each section of each movie
def populateMovieObjList(list_of_lists, parkside_url):
	list_of_movies = []
	for movie in list_of_lists:
		for time in range(movie[2]):
			movie[2] -= 1
			try:
				movie_name, showing_time, theater_num, sold_seats = scrapeSeats(movie[0], movie[1], movie[2], parkside_url)
				movie_obj = Movie(movie_name, showing_time, theater_num, sold_seats)
				list_of_movies.append(movie_obj)
				print("Movie Added")
			except:
				print("Unable To Get Movie Data")
	return list_of_movies

# Prints the movie object string to console
def printAsList(list_of_movie_objs):
	for i in list_of_movie_objs:
		print(i)
		print()

# Prints the formatted movie time + number of seats sold for that time under each movie name
def printInFormat(list_of_movie_objs):
	movie_names = []
	list_of_times_of_movie = []
	list_of_sold_seats = []
	for i in range(len(list_of_movie_objs)):
		movie_name = list_of_movie_objs[i].getMovieName()
		if movie_name not in movie_names:
			movie_names.append(movie_name)
	for i in range(len(movie_names)):
		times_of_movie = []
		sold_seats = []
		for movie in list_of_movie_objs:
			if str(movie.getMovieName()) == str(movie_names[i]):
				times_of_movie.append(movie.getMovieTime())
				sold_seats.append(movie.getSoldSeats())
		list_of_times_of_movie.append(times_of_movie)
		list_of_sold_seats.append(sold_seats)

	for i in range(len(movie_names)):
		print()
		print(movie_names[i])
		for j in range(len(list_of_times_of_movie[i])):
			print("{} - {}".format(list_of_times_of_movie[i][j], list_of_sold_seats[i][j]))

		
def getMovies():
	
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

	return list_of_movie_objs

def main():

	movies = getMovies()

	# Print movie data to console
	#printAsList(list_of_movie_objs)

	# Write movie data to text file in order
	#writeToFileAsList(list_of_movie_objs)

	# Print movie data formatted for blackboard record
	printInFormat(movies)

	# Write movie data to text file formatted
	writeToFileFormatted(movies)


if __name__ == "__main__":
	main()