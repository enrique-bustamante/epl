# %%
# Import dependencies
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from myfunctions import homeOrAway, homeAwayDifference, cloneDfs, linearRegressionAnalysis, cleanDataFrame, categoryPerCost
import dataframe_image as dfi

# %%
goalieDf = pd.read_csv('Resources/Goalkeepers.csv')
goalieDf
lastWeekRankDf = pd.read_csv('Rankings/GoalieRank.csv')[['Name','Ranking']]
lastWeekRankDf = lastWeekRankDf.set_index('Name')


goalieDfClean, costDf, goalieForm = cleanDataFrame(goalieDf)
goalieDfClean

goalieDfHome, goalieDfAway = cloneDfs(goalieDfClean)


goalieGroupbyDf = goalieDf.groupby('Name').mean()

listOfCategories = ['Pts', 'Goals scored', 'Assists', 'Clean sheets', 'Goals conceded', 'Own goals', 'Penalties saved', 'Penalties missed', 'Yellow cards', 'Red cards', 'Saves', 'Bonus', 'Bonus Points System']

categoryPerCost(goalieGroupbyDf, listOfCategories)

goalieGroupbyDf['Availability'] = goalieGroupbyDf['Minutes played']/90
goalieGroupbyDf['Form'] = goalieForm


prodGoalDf = linearRegressionAnalysis(goalieGroupbyDf)
prodGoalDf['Cost'] = costDf




homeAwayDiffDf = homeAwayDifference(goalieDfHome, goalieDfAway).dropna()

homeAwayDiffGoalie = linearRegressionAnalysis(homeAwayDiffDf)

prodGoalDf['Home and Away'] = homeAwayDiffGoalie['Value']

prodGoalDf = prodGoalDf[['Value', 'Cost', 'Home and Away']]

# %%
prodGoalDf['Ranking'] = prodGoalDf['Value'].rank(ascending=False)
prodGoalDf['Last Week Ranking'] = lastWeekRankDf


prodGoalDf.to_csv('Rankings/GoalieRank.csv')

dfi.export(prodGoalDf.head(20), 'static/GoalieRank.png')

# %%
