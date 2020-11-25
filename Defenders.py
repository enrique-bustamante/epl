# %%
# Import dependencies
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from myfunctions import homeOrAway, homeAwayDifference, cloneDfs, linearRegressionAnalysis, cleanDataFrame, categoryPerCost
import dataframe_image as dfi

# %%
# Load in the data
defenderDf = pd.read_csv('Resources/Defenders.csv')
defenderDf

# %%
defenderDf.isnull().sum()
# %%
# Clean the data to make suitable for linear regression analysis
defenderDf, costDf, defenderForm = cleanDataFrame(defenderDf)
defenderDf

defenderDfHome, defenderDfAway = cloneDfs(defenderDf)


defenderGroupbyDf = defenderDf.groupby('Name').mean()

listOfCategories = ['Pts', 'Goals scored', 'Assists', 'Clean sheets', 'Goals conceded', 'Own goals', 'Penalties saved', 'Penalties missed', 'Yellow cards', 'Red cards', 'Saves', 'Bonus', 'Bonus Points System']

categoryPerCost(defenderGroupbyDf, listOfCategories)

defenderGroupbyDf['Availability'] = defenderGroupbyDf['Minutes played']/90
defenderGroupbyDf['Form'] = defenderForm
#%%
# Run linear regression analysis
prodDefDf = linearRegressionAnalysis(defenderGroupbyDf)
prodDefDf['Cost'] = costDf

homeAwayDiffDf = homeAwayDifference(defenderDfHome, defenderDfAway).dropna()

homeAwayDiffdefender = linearRegressionAnalysis(homeAwayDiffDf)

#%%
# Add in the home away value
prodDefDf['Home and Away'] = homeAwayDiffdefender['Value']

prodDefDf = prodDefDf[['Value', 'Cost', 'Home and Away']]

# Save file to Rankings folder
prodDefDf.to_csv('Rankings/DefendersRank.csv')

dfi.export(prodDefDf.head(20), 'static/DefenderRank.png')
