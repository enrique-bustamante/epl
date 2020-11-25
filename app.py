from flask import Flask, render_template
from myfunctions import homeOrAway, homeAwayDifference, cloneDfs, linearRegressionAnalysis, cleanDataFrame, categoryPerCost
import dataframe_image as dfi
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from Scripts import Defenders, Forwards, Goalies, Middies

app = Flask(__name__)

@app.route('/')
def index():
    Defenders.defenders()
    Forwards.forwards()
    Goalies.goalies()
    Middies.mids()
    return render_template('index.html')

if __name__ == '__main__':
    app.run
