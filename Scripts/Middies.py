def mids():
    # Import dependencies
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from myfunctions import homeOrAway, homeAwayDifference, cloneDfs, linearRegressionAnalysis, cleanDataFrame, categoryPerCost
    import dataframe_image as dfi


    # read in the data
    midDf = pd.read_csv('Resources/Midfielders.csv')
    midDf
    lastWeekRankDf = pd.read_csv('Rankings/MidRank.csv')[['Name','Ranking']]
    lastWeekRankDf = lastWeekRankDf.set_index('Name')


    midDf, costDf, midForm = cleanDataFrame(midDf)
    midDf

    midDfHome, midDfAway = cloneDfs(midDf)


    midGroupbyDf = midDf.groupby('Name').mean()

    listOfCategories = ['Pts', 'Goals scored', 'Assists', 'Clean sheets', 'Goals conceded', 'Own goals', 'Penalties saved', 'Penalties missed', 'Yellow cards', 'Red cards', 'Saves', 'Bonus', 'Bonus Points System']

    categoryPerCost(midGroupbyDf, listOfCategories)

    midGroupbyDf['Availability'] = midGroupbyDf['Minutes played']/90
    midGroupbyDf['Form'] = midForm


    prodMidDf = linearRegressionAnalysis(midGroupbyDf)
    prodMidDf['Cost'] = costDf


    homeAwayDiffDf = homeAwayDifference(midDfHome, midDfAway).dropna()

    homeAwayDiffmid = linearRegressionAnalysis(homeAwayDiffDf)

    prodMidDf['Home and Away'] = homeAwayDiffmid['Value']

    prodMidDf = prodMidDf[['Value', 'Cost', 'Home and Away']]

    prodMidDf['Ranking'] = prodMidDf['Value'].rank(ascending=False)
    prodMidDf['Last Week Ranking'] = lastWeekRanMid

    prodMidDf.to_csv('Rankings/midRank.csv')

    dfi.export(prodMidDf.head(20), 'static/MidRank.png')
