def forwards():
    # Import dependencies
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from myfunctions import homeOrAway, homeAwayDifference, cloneDfs, linearRegressionAnalysis, cleanDataFrame, categoryPerCost, zScore
    import dataframe_image as dfi

    # Load in the data
    forwardsDf = pd.read_csv('Resources/Forwards.csv')
    lastWeekRankDf = pd.read_csv('Rankings/forwardsRank copy.csv')[['Name','Total Rank']]
    lastWeekRankDf = lastWeekRankDf.set_index('Name')

    # Clean the data to make suitable for linear regression analysis
    forwardsDf, costDf, forwardForm = cleanDataFrame(forwardsDf)

    # Create the home and away tables to determine the spread
    forwardsDfHome, forwardsDfAway = cloneDfs(forwardsDf)

    # Group by name and get the averages
    forwardsGroupbyDf = forwardsDf.groupby('Name').mean()

    listOfCategories = ['Pts', 'Goals scored', 'Assists', 'Clean sheets', 'Goals conceded', 'Own goals', 'Penalties saved', 'Penalties missed', 'Yellow cards', 'Red cards', 'Saves', 'Bonus', 'Bonus Points System']

    forwardsGroupbyDf = categoryPerCost(forwardsGroupbyDf, listOfCategories)

    forwardsGroupbyDf['Availability'] = forwardsGroupbyDf['Minutes played']/90

    # Run linear regression analysis
    prodForwardDf = linearRegressionAnalysis(forwardsGroupbyDf)
    prodForwardDf['Cost'] = costDf




    homeAwayDiffDf = homeAwayDifference(forwardsDfHome, forwardsDfAway).dropna()

    homeAwayDiffForwards = linearRegressionAnalysis(homeAwayDiffDf)

    # Add in the home away value
    prodForwardDf['Home and Away'] = homeAwayDiffForwards['Value']

    prodForwardDf = prodForwardDf[['Value', 'Prediction', 'Cost', 'Home and Away']]

    prodForwardDf['Last Week Ranking'] = lastWeekRankDf
    prodForwardDf['Projection'] = prodForwardDf['Prediction'] * prodForwardDf['Cost']
    prodForwardDf['Form'] = forwardForm


    prodForwardDf = zScore(prodForwardDf)


    # Save files to Rankings and static folders
    prodForwardDf.to_csv('Rankings/forwardsRank.csv')

    dfi.export(prodForwardDf.head(20), 'static/ForwardRank.png')
