""" CS 109A tutorial on Panda Processing"""

import pandas as pd


f = open("./output.csv")

column_names = f.readline().strip().split(",")[1:]
cleaned_column_names = [name for name in column_names]
cleaned_column_names.insert(0, "ID")

#print(cleaned_column_names)

dataset = []

#Iterates through each line in the csv file
for line in f:
    print(type(line))
    attributes = line.split(",")

    #Constructs a new dictionary for each line, and 
    # appends this dictionary to the 'dataset';
    # thus, the data set is a list of dictionaries (1 dictionary per movie/tv show)
    
    #Why zip() ?
    dataset.append(dict(zip(cleaned_column_names, attributes)))

print(dataset)