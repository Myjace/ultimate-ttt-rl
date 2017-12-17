from ultimateboard import UTTTBoard, UTTTBoardDecision
from player import RandomTTTPlayer, RLTTTPlayer
from ultimateplayer import RandomUTTTPlayer, RLUTTTPlayer
from learning import NNUltimateLearning, TableLearning
from plotting import drawXYPlotByFactor
import os, csv
from game import GameSequence

LEARNING_FILE = 'ultimate_player_nn1.h5'
WIN_PCT_FILE = 'win_pct_player_1.csv'

def playTTTAndPlotResults():
    learningPlayer = RLTTTPlayer()
    randomPlayer = RandomTTTPlayer()
    results = []
    numberOfSetsOfGames = 5
    for i in range(numberOfSetsOfGames):
        games = GameSequence(1000, learningPlayer, randomPlayer)
        results.append(games.playGamesAndGetWinPercent())
    plotValues = {'X Win Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[0], results)),
                  'O Win Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[1], results)),
                  'Draw Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[2], results))}
    drawXYPlotByFactor(plotValues, 'Set Number', 'Fraction')

def playUltimateAndPlotResults():
    learningPlayer = RLUTTTPlayer(NNUltimateLearning)
    randomPlayer = RandomUTTTPlayer()
    results = []
    numberOfSetsOfGames = 50
    if os.path.isfile(LEARNING_FILE):
        learningPlayer.loadLearning(LEARNING_FILE)
    for i in range(numberOfSetsOfGames):
        games = GameSequence(100, learningPlayer, randomPlayer, BoardClass=UTTTBoard, BoardDecisionClass=UTTTBoardDecision)
        results.append(games.playGamesAndGetWinPercent())
    learningPlayer.saveLearning(LEARNING_FILE)
    writeResultsToFile(results)
    plotValues = {'X Win Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[0], results)),
                  'O Win Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[1], results)),
                  'Draw Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[2], results))}
    drawXYPlotByFactor(plotValues, 'Set Number', 'Fraction')

def playUltimateForTraining():
    learningPlayer = RLUTTTPlayer(TableLearning)
    randomPlayer = RandomUTTTPlayer()
    games = GameSequence(4000, learningPlayer, randomPlayer, BoardClass=UTTTBoard, BoardDecisionClass=UTTTBoardDecision)
    games.playGamesAndGetWinPercent()
    learningPlayer.saveLearning(NNUltimateLearning.TABLE_LEARNING_FILE)

def writeResultsToFile(results):
    with open(WIN_PCT_FILE, 'a') as outfile:
        for result in results:
            outfile.write('%s,%s,%s\n'%(result[0], result[1], result[2]))

def plotResultsFromFile(resultsFile):
    results = []
    with open(resultsFile, 'r') as infile:
        reader = csv.reader(infile)
        results = map(tuple, reader)
    numberOfSetsOfGames = len(results)
    plotValues = {'X Win Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[0], results)),
                  'O Win Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[1], results)),
                  'Draw Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[2], results))}
    drawXYPlotByFactor(plotValues, 'Set Number', 'Fraction')

if __name__ == '__main__':
    #playTTTAndPlotResults()
    #playUltimateForTraining()
    #playUltimateAndPlotResults()
    plotResultsFromFile('results/ultmate_nn1_results.csv')
