def linearRegressionAnalysis(df):
    y = df['Pts']
    X = df.drop(columns=['Cost','Pts', 'Minutes played'])

    from sklearn.linear_model import LinearRegression
    regr = LinearRegression()

    regr.fit(X, y)
    y_pred = regr.predict(X)

    regr.coef_
    prodDf = X * regr.coef_
    prodDf['Value'] = prodDf.sum(axis=1)
    prodDf = prodDf.sort_values('Value', ascending=False)

    return prodDf


def homeAwayDifference(df1, df2):
    groupbyDfHome = df1.groupby('Name').mean().dropna()
    groupbyDfAway = df2.groupby('Name').mean().dropna()
    homeAwayDiffDf = groupbyDfHome - groupbyDfAway
    return homeAwayDiffDf


def cloneDfs(df):

    homeDf = df[df['Location'] == 'Home']
    awayDf = df[df['Location'] == 'Away']
    return homeDf, awayDf


def cleanDataFrame(df):
    gameWeek: int = df['Gameweek'].max()

    df['Cost'] = df['Cost'].replace('£','', regex=True).astype(float)

    df['Location'] = df['Opposition'].apply(homeOrAway)

    costDf = df[df['Gameweek'] == gameWeek][['Name','Cost']]
    costDf = costDf.set_index('Name')
    dfForm = df[df['Gameweek'] >= (gameWeek-3)]
    formSeries = dfForm.groupby('Name')['Pts'].mean()

    df = df.drop(columns=['Gameweek','Opposition', 'Net Transfers', 'Selected by','ICT Index'])

    return df, costDf, formSeries

def homeOrAway(data: str) -> str:
        if '(H)' in data:
            return 'Home'
        else:
            return 'Away'

def categoryPerCost(df, listOfCategories):
    for category in listOfCategories:
        df[category] = df[category]/df['Cost']
    return df


