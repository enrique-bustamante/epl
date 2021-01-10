def defenders():
   # %%
   from sklearn.model_selection import train_test_split
   from myfunctions import homeOrAway, homeAwayDifference, cloneDfs, linearRegressionAnalysis, cleanDataFrame, categoryPerCost
   import dataframe_image as dfi
   import pandas as pd

   # %%
   # Load in the data
   defenderDf = pd.read_csv('Resources/Defenders.csv')
   lastWeekRankDf = pd.read_csv('Rankings/DefendersRank copy.csv')[['Name','Total Rank']]
   lastWeekRankDf = lastWeekRankDf.set_index('Name')
# Import dependencies
   import pandas as pd
   from sklearn.linear_model import LinearRegression

   # %%
   # Clean the data to make suitable for linear regression analysis
   defenderDf, costDf, defenderForm = cleanDataFrame(defenderDf)

   # Create the home and away tables to determine the spread
   defenderDfHome, defenderDfAway = cloneDfs(defenderDf)

   # Group by name and get the averages
   defenderGroupbyDf = defenderDf.groupby('Name').mean()

   listOfCategories = ['Pts', 'Goals scored', 'Assists', 'Clean sheets', 'Goals conceded', 'Own goals', 'Penalties saved', 'Penalties missed', 'Yellow cards', 'Red cards', 'Saves', 'Bonus', 'Bonus Points System']

   defenderGroupbyDf = categoryPerCost(defenderGroupbyDf, listOfCategories)

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

   prodDefDf = prodDefDf[['Value', 'Prediction', 'Cost', 'Home and Away']]
   prodDefDf['Ranking'] = prodDefDf['Value'].rank(ascending=False)
   prodDefDf['Last Week Ranking'] = lastWeekRankDf
   prodDefDf['Projection'] = prodDefDf['Prediction'] * prodDefDf['Cost']
   prodDefDf['Proj Rank'] = prodDefDf['Projection'].rank(ascending=False)
   prodDefDf['Total Rank'] = (prodDefDf['Proj Rank'] + prodDefDf['Ranking']).rank(ascending=True)
   prodDefDf = prodDefDf[['Value', 'Projection', 'Cost', 'Last Week Ranking', 'Total Rank', 'Home and Away']]

   # Save files to Rankings and static folders
   prodDefDf.to_csv('Rankings/DefendersRank.csv')

   dfi.export(prodDefDf.head(20), 'static/DefenderRank.png')
