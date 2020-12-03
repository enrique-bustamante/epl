def mids():
    # Import dependencies
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from myfunctions import homeOrAway, homeAwayDifference, cloneDfs, linearRegressionAnalysis, cleanDataFrame, categoryPerCost
    import dataframe_image as dfi

    # Load in the data
    midDf = pd.read_csv('Resources/Midfielders.csv')
    lastWeekRankDf = pd.read_csv('Rankings/midRank.csv')[['Name','Ranking']]
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
    midGroupbyDf['Form'] = midForm

    # Run linear regression analysis
    prodMidDf = linearRegressionAnalysis(midGroupbyDf)
    prodMidDf['Cost'] = costDf


    homeAwayDiffDf = homeAwayDifference(midDfHome, midDfAway).dropna()

    homeAwayDiffmid = linearRegressionAnalysis(homeAwayDiffDf)

    # Add in the home away value
    prodMidDf['Home and Away'] = homeAwayDiffmid['Value']

    prodMidDf = prodMidDf[['Value', 'Cost', 'Home and Away']]

    prodMidDf['Ranking'] = prodMidDf['Value'].rank(ascending=False)
    prodMidDf['Last Week Ranking'] = lastWeekRankDf

    # Save file to Rankings folder
    prodMidDf.to_csv('Rankings/midRank.csv')

    dfi.export(prodMidDf.head(20), 'static/MidRank.png')
