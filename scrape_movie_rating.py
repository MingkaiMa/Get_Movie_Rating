#!/usr/bin/python3

##Written by Mingkai Ma  mingkai.ma1@student.unsw.edu.au
##python script to get movie rating based on IMDb and Rotten Tomotoes, from user input

import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import fileinput
import os
import sys


sys.stdout.write("Input the movie name that you want to know the rating: \n\n")
sys.stdout.flush()
movie_list = []
for line in fileinput.input():
    movie_list.append(line.strip('\n'))

rating_details_imdb = {}
rating_details_rotten_romatoes = {}
sys.stdout.write("Please wait, trying to get data.\n")
sys.stdout.flush()
for movie in movie_list:
    movie_reserve_name = movie
    movie = re.sub(r'\s', '', movie)
    movie = movie.lower()
    search_url_imdb = 'http://www.google.com.au/search?q=' + movie + 'imdb'
    search_url_rotten_romatoes = 'http://www.google.com.au/search?q=' + movie + 'rottentomatoes'
    page = requests.get(search_url_imdb)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all('a')
    for l in links:
        m = re.findall(r'http://www\.imdb\.com/title/.*?/', l.get('href'))
        if m:
            break

    imdb_response = urlopen(m[0])
    soup2 = BeautifulSoup(imdb_response.read(), 'html.parser')
    spans = soup2.find_all('span', attrs={'class': "rating"})
    rating = spans[0]
    rating = re.sub(r'<.*?>', '', str(rating))
    rating = rating.split('/')[0]
    rating_details_imdb[movie_reserve_name] = rating

    page_rotten = requests.get(search_url_rotten_romatoes)    
    soup_rotten = BeautifulSoup(page_rotten.content, 'html.parser')
    links_rotten = soup_rotten.find_all('a')
    for l in links_rotten:
        n = re.findall(r'https://www\.rottentomatoes\.com/m/.*?/', l.get('href'))
        if n:
            break

    rotten_response = urlopen(n[0])
    soup2_rotten = BeautifulSoup(rotten_response.read(), 'html.parser')
    scripts = soup2_rotten.find_all('script', {"type" : "application/ld+json"})
    rating = re.findall(r'"AggregateRating","ratingValue":.*?,', str(scripts[0]))
    rating = re.findall(r'[0-9]+', rating[0])
    rating_details_rotten_romatoes[movie_reserve_name] = rating[0]
    
    
        
    

longest_movie_name_length = 0
for movie in rating_details_imdb:
    if(len(movie) > longest_movie_name_length):
        longest_movie_name_length = len(movie)

sys.stdout.write('=========================\n')
sys.stdout.write("Movie rating details: \n")
print('{:{}} : {}\n'.format('Movie', longest_movie_name_length, 'Rating based on IMDB'))
rating_details_imdb = sorted(rating_details_imdb.items(), key=lambda x:float(x[1]), reverse=True)
for movie in rating_details_imdb:
    print('{:{}} : {}'.format(movie[0], longest_movie_name_length, movie[1]))


sys.stdout.write('\n=========================\n')
print('{:{}} : {}\n'.format('Movie', longest_movie_name_length, 'Rating based on Rotten Tomatoes'))
rating_details_rotten_romatoes = sorted(rating_details_rotten_romatoes.items(), key=lambda x:float(x[1]), reverse=True)
for movie in rating_details_rotten_romatoes:
    print('{:{}} : {}%'.format(movie[0], longest_movie_name_length, movie[1]))







    
