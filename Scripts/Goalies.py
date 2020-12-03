def goalies():
# Import dependencies
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from myfunctions import homeOrAway, homeAwayDifference, cloneDfs, linearRegressionAnalysis, cleanDataFrame, categoryPerCost
    import dataframe_image as dfi

    # Load in the data
    goalieDf = pd.read_csv('Resources/Goalkeepers.csv')
    lastWeekRankDf = pd.read_csv('Rankings/GoalieRank.csv')[['Name','Ranking']]
    lastWeekRankDf = lastWeekRankDf.set_index('Name')

    # Clean the data to make suitable for linear regression analysis
    goalieDfClean, costDf, goalieForm = cleanDataFrame(goalieDf)

    # Create the home and away tables to determine the spread
    goalieDfHome, goalieDfAway = cloneDfs(goalieDfClean)

    # Group by name and get the averages
    goalieGroupbyDf = goalieDf.groupby('Name').mean()
    listOfCategories = ['Pts', 'Goals scored', 'Assists', 'Clean sheets', 'Goals conceded', 'Own goals', 'Penalties saved', 'Penalties missed', 'Yellow cards', 'Red cards', 'Saves', 'Bonus', 'Bonus Points System']

    goalieGroupbyDf = categoryPerCost(goalieGroupbyDf, listOfCategories) # feed in the list of categories and the dataframe to get the new values

    goalieGroupbyDf['Availability'] = goalieGroupbyDf['Minutes played']/90
    goalieGroupbyDf['Form'] = goalieForm

    # Run linear regression analysis
    prodGoalDf = linearRegressionAnalysis(goalieGroupbyDf)
    prodGoalDf['Cost'] = costDf




    homeAwayDiffDf = homeAwayDifference(goalieDfHome, goalieDfAway).dropna()

    homeAwayDiffGoalie = linearRegressionAnalysis(homeAwayDiffDf)

    # Add in the home away value
    prodGoalDf['Home and Away'] = homeAwayDiffGoalie['Value']

    prodGoalDf = prodGoalDf[['Value', 'Cost', 'Home and Away']]

    prodGoalDf['Ranking'] = prodGoalDf['Value'].rank(ascending=False)
    prodGoalDf['Last Week Ranking'] = lastWeekRankDf

    # Save files to Rankings and static folders
    prodGoalDf.to_csv('Rankings/GoalieRank.csv')

    dfi.export(prodGoalDf.head(20), 'static/GoalieRank.png')
