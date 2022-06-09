'''
	Author: Carson Pribble
	File: movie_object.py
	Purpose: This is a class that will create object out of each movie scraped from Paragons movie times
'''
class Movie(object):

	def __init__(self, movie_name, movie_time, theater_num, sold_seats):
		self.movie_name = movie_name
		self.movie_time = movie_time
		self.theater_num = theater_num
		self.sold_seats = sold_seats

	# GETTERS
	def getMovieName(self):
		return self.movie_name
	def getMovieTime(self):
		return self.movie_time
	def getTheaterNum(self):
		return self.theater_num
	def getSoldSeats(self):
		return self.sold_seats
		
	# DUNDERS
	def __str__(self):
		return (str(self.movie_name) + "\n" + str(self.movie_time)
			+ "\n" + "Theater Number: " + (str(self.theater_num)) + "\n"
			"LuxBox Seats: " + str(self.sold_seats))

