# epl

## Purpose

This project was designed as a means to determine the best value
for footballers in the English Premier League, for the purposes of the Fantasy
League. While the most important feaure is the points scored, the limited
budget makes the cost of each player that much more important. The value will
be based on most pertinent factors.

## Tools Used

Here is a list of technologies utilized in this project
* Flask
* Python
* HTML
* CSS
* Pandas
* Numpy
* Scikit Learn Linear Regression
* Dataframe Image

## Overview of workflow

* Data is updated (currently, this is manual)
* Flask app is run
* The flask app runs four scripts which are imported as functions
* Each script imports 2 csvs, cleans the data, groups data by player name, and exports a png and csv
    for use on HTML and future purposes


## Functions created

Since the four scripts are identical, with the exception of the position, I
created function that could be imported and used by all four scripts. Here are the function:


### Cleaning of the Dataframe

First, for the cleanDataFrame() function, I created a variable to be the most
recent gameweek using max. Next, I had to clean the ***_Cost_*** columns and
remove the pound sign. I created a Location column to designate the game as
being either Home or Away. The following item was to create a cost dataframe,
saving the most recent cost of the player according to the most recent
Gameweek, to join with the grouped dataframe later on. I then used groupby to
get the averages of the points for the last four games, known as form, for
each player. I then dropped the Gameweek, Opposition, Net Transfers, Selected
by, and ICT Index columns since they were not of any use in the regression
analysis.

### Clone Dataframes

For the cloneDfs() function, I simply created two filtered tables based on
location being either Home or Away. These two tables are used to find the
difference between home and away performance.

###



## Linear Regression Analysis

