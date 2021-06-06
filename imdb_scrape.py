''' Scraping IMDB for LGBT tagged content'''

from bs4 import BeautifulSoup
import requests
import numpy as np
import re
import pandas as pd
from time import sleep
from random import randint
from tabulate import tabulate




titles = []
years = []
mpaa_ratings =[]
fan_stars = []
genres =[]
creators =[]        #Actors and directors
imdb_reference = [] #IMDb reference number



pages = np.arange(1, 35, 1)

for page in pages:
    page_i = requests.get("https://www.imdb.com/search/keyword/?keywords=lgbt&ref_=kw_ref_key&sort=moviemeter,asc&mode=detail&page=" + str(page))
    soup = BeautifulSoup(page_i.text, 'lxml')

    data = soup.findAll('div', attrs = {'class' : "lister-item mode-detail"})

    #This gives running script so we can see the program working and check its status.
    print('Sleeping')
    sleep(randint(2,10))
    print('Running' + str(page))

    for listing in data:
        title = listing.h3.a.text
        year = listing.h3.find('span', class_ = 'lister-item-year text-muted unbold').text.replace('(', '').replace(')', '').replace('I ', '').replace('I', '').split('–')
        titles.append(title)
        years.append(year[0])
        
        
        mpaa_rating = listing.p.find('span', class_ = "certificate").text if listing.p.find('span', class_ = "certificate") else '-'
        mpaa_ratings.append(mpaa_rating)
            
    
        genre = listing.p.find('span', class_ = "genre").text.replace('\n', '').replace(' ', '') if listing.p.find('span', class_ = "genre") else '-'
        genre = genre.split(',')    
        genres.append(genre)
        
            
        stars = float(listing.find('div', class_ = "inline-block ratings-imdb-rating").text.replace('\n', '')) if listing.find('div', 
        class_ = "inline-block ratings-imdb-rating") else '-'
        fan_stars.append(stars)
        
        people = []
        if listing.find_all("a", attrs = { 'href' : re.compile("/name/.")}):
            people_tags = listing.find_all("a", attrs = { 'href' : re.compile("/name/.")})
            for person in people_tags:
                people.append(person.text)
            
        else:
            people.append('-')
        creators.append(people)
        
        
        id = str(listing.h3.find("a")) if listing.h3.find("a") else '-'*26
        imdb_reference.append(id[16:25])

# This checks for equal field size
"""    
print(len(titles))
print(len(years))
print(len(mpaa_ratings))
print(len(fan_stars))
print(len(genres))
print(len(creators))
print(len(imdb_reference))
"""

# Pandas dataframe
movies = pd.DataFrame({
    'movie': titles,
    'years' : years,
    'mpaa_ratings' : mpaa_ratings,
    'fan_stars' : fan_stars,
    'genres' : genres,
    'creators' : creators,
    'imdb_reference' : imdb_reference
})

#I dont want the output to be regenerated every time I change other parts
"""
movies.to_csv('output.csv')
"""


# Possible other outputs? Need to see how pandas does with CSV files
print(tabulate(movies, headers='keys', tablefmt='psql'))
