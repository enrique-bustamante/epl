def mids():
    # Import dependencies
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from myfunctions import homeOrAway, homeAwayDifference, cloneDfs, linearRegressionAnalysis, cleanDataFrame, categoryPerCost, zScore
    import dataframe_image as dfi

    # Load in the data
    midDf = pd.read_csv('Resources/Midfielders.csv')
    lastWeekRankDf = pd.read_csv('Rankings/midRank copy.csv')[['Name','Total Rank']]
    lastWeekRankDf = lastWeekRankDf.set_index('Name')

    # Clean the data to make suitable for linear regression analysis
    midDf, costDf, midForm = cleanDataFrame(midDf)

    # Create the home and away tables to determine the spread
    midDfHome, midDfAway = cloneDfs(midDf)

    # Group by name and get the averages
    midGroupbyDf = midDf.groupby('Name').mean()

    listOfCategories = ['Pts', 'Goals scored', 'Assists', 'Clean sheets', 'Goals conceded', 'Own goals', 'Penalties saved', 'Penalties missed', 'Yellow cards', 'Red cards', 'Saves', 'Bonus', 'Bonus Points System']

    midGroupbyDf = categoryPerCost(midGroupbyDf, listOfCategories)

    midGroupbyDf['Availability'] = midGroupbyDf['Minutes played']/90

    # Run linear regression analysis
    prodMidDf = linearRegressionAnalysis(midGroupbyDf)
    prodMidDf['Cost'] = costDf


    homeAwayDiffDf = homeAwayDifference(midDfHome, midDfAway).dropna()

    homeAwayDiffmid = linearRegressionAnalysis(homeAwayDiffDf)

    # Add in the home away value
    prodMidDf['Home and Away'] = homeAwayDiffmid['Value']

    prodMidDf = prodMidDf[['Value', 'Prediction', 'Cost', 'Home and Away']]

    prodMidDf['Last Week Ranking'] = lastWeekRankDf
    prodMidDf['Projection'] = prodMidDf['Prediction'] * prodMidDf['Cost']
    prodMidDf['Form'] = midForm


    prodMidDf = zScore(prodMidDf)

    # Save files to Rankings and static folders
    prodMidDf.to_csv('Rankings/midRank.csv')

    dfi.export(prodMidDf.head(20), 'static/MidRank.png')
