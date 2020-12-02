# %%
# Import dependencies
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from myfunctions import homeOrAway, homeAwayDifference, cloneDfs, linearRegressionAnalysis, cleanDataFrame, categoryPerCost
import dataframe_image as dfi

# %%
forwardsDf = pd.read_csv('Resources/Forwards.csv')
forwardsDf
lastWeekRankDf = pd.read_csv('Rankings/forwardsRank.csv')[['Name','Ranking']]
lastWeekRankDf = lastWeekRankDf.set_index('Name')

# %%
forwardsDf, costDf, forwardForm = cleanDataFrame(forwardsDf)
forwardsDf


forwardsDfHome, forwardsDfAway = cloneDfs(forwardsDf)


forwardsGroupbyDf = forwardsDf.groupby('Name').mean()

listOfCategories = ['Pts', 'Goals scored', 'Assists', 'Clean sheets', 'Goals conceded', 'Own goals', 'Penalties saved', 'Penalties missed', 'Yellow cards', 'Red cards', 'Saves', 'Bonus', 'Bonus Points System']

categoryPerCost(forwardsGroupbyDf, listOfCategories)

forwardsGroupbyDf['Availability'] = forwardsGroupbyDf['Minutes played']/90
forwardsGroupbyDf['Form'] = forwardForm


prodForwardDf = linearRegressionAnalysis(forwardsGroupbyDf)
prodForwardDf['Cost'] = costDf




homeAwayDiffDf = homeAwayDifference(forwardsDfHome, forwardsDfAway).dropna()

homeAwayDiffForwards = linearRegressionAnalysis(homeAwayDiffDf)

prodForwardDf['Home and Away'] = homeAwayDiffForwards['Value']

prodForwardDf = prodForwardDf[['Value', 'Cost', 'Home and Away']]

# %%
prodForwardDf['Ranking'] = prodForwardDf['Value'].rank(ascending=False)
prodForwardDf['Last Week Ranking'] = lastWeekRankDf

prodForwardDf.to_csv('Rankings/forwardsRank.csv')

dfi.export(prodForwardDf.head(20), 'static/ForwardRank.png')

# %%
