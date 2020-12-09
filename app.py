from flask import Flask, render_template, request
from myfunctions import homeOrAway, homeAwayDifference, cloneDfs, linearRegressionAnalysis, cleanDataFrame, categoryPerCost
import dataframe_image as dfi
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from Scripts import Defenders, Forwards, Goalies, Middies
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/copies', methods=['POST'])
def copies():
    if request.method=='POST':
        os.popen('cp Rankings/DefendersRank.csv Rankings/DefendersRank\ copy.csv')
        os.popen('cp Rankings/ForwardsRank.csv Rankings/ForwardsRank\ copy.csv')
        os.popen('cp Rankings/GoalieRank.csv Rankings/GoalieRank\ copy.csv')
        os.popen('cp Rankings/midRank.csv Rankings/midRank\ copy.csv')
        return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    if request.method=='POST':
        Defenders.defenders()
        Forwards.forwards()
        Goalies.goalies()
        Middies.mids()
        return render_template('index.html')

if __name__ == '__main__':
    app.run
