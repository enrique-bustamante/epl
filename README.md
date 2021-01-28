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
* The flask app runs opening up to a webpage with two buttons
* The first button creates a copy of the current rankings to use as the last week's ranking value for the tables
* The second button runs the four scripts which are imported as functions
* Each script imports 2 csvs, cleans the data, groups data by player name, calculates a z-score for ranking, and exports a png and csv
    for use on HTML and future purposes


## Functions created

Since the four scripts are identical, with the exception of the position, functions were created that could be imported and used by all four scripts. Here are the functions:


### Cleaning of the Dataframe

First, for the cleanDataFrame() function, a variable was created to be the most
recent gameweek using the max value for each player. Next,the ***_Cost_*** columns were cleaned and
the British pound sign was removed. A Location column was created to designate the game as
being either Home or Away. The following item was to create a cost dataframe,
saving the most recent cost of the player according to the most recent
Gameweek, to join with the grouped dataframe later on. Groupby was then used to
get the averages of the points for the last four games, known as form, for
each player. The Gameweek, Opposition, Net Transfers, Selected
by, and ICT Index columns were then dropped since they were not of any use in the regression
analysis. This function returns the cleaned dataframe, the players and their cost in a dataframe, and the form of the players as a dataframe.

### Clone Dataframes

For the cloneDfs() function, I simply created two filtered tables based on
location being either Home or Away. These two tables are used to find the
difference between home and away performance.

### Category per Cost

For the categoryPerCost() function, I pass through a dataframe and a list of columns that I control for cost. This function runs a for loop through the list and divides those specific columns by the cost of the player, to control for price. The output is a dataframe, with the specified columns divided by cost.

### Linear Regression Analysis

The linearRegressionAnalysis() function takes the dataframe and separates it into features and labels, fits the data, then makes a prediction. The coefficient array is then multiplied across the features and summed to achieve the value. The prediction is also added to the dataframe that is output.

### Home Away Spread

The homeAwayDifference functions take the two dataframes, home and away, and creates a new dataframe with the new values.

### Home or Away

For the homeOrAway() function, I added this within the cleanDataFrame() function to determine if the location was a home or away game.

### Z-score

The mean and standard deviation were calculated for Value, Form, and Projection values (explained in Scripts section). To calculate the z-score, the mean was subtracted for the player specific value, then divided by the standard deviation. The z-score for Value and Projection were multiplied by 2, then all three z-scores were added together.

## Scripts




## Limitations

One limitation of this model is that if the site is refreshed, it will run the calculations again and the current rankings and last week rankings will be the same. I am thinking of adding an Update button and only run the script by calling that action.
