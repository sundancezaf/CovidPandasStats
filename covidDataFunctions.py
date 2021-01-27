import pandas as pd
import matplotlib.pyplot as plt
from datetime import *

# Options for display
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv('us-states.csv')
usTotal = pd.read_csv('us.csv')


class stateDataFrame:
    def __init__(self, name):
        self.name = name
        stateFilter = (df['state'] == self.name)
        self.DataFrame = df[stateFilter]
        self.DataFrame.reset_index(inplace=True, drop=True)
        self.lastIndex = self.DataFrame.index[-1]
        self.Daily = []


    def resetIndex(self):
        self.DataFrame.reset_index(inplace=True, drop=True)

    def showDataFrame(self):
        return self.DataFrame

    def getFirstEvent(self):
        firstEvent = self.DataFrame.loc[0, 'date']
        return firstEvent

    def totalCases(self):
        lastIndex = self.DataFrame.index[-1]
        total = self.DataFrame.loc[lastIndex, 'cases']
        return total

    def totalDeaths(self):
        lastIndex = self.DataFrame.index[-1]
        total = self.DataFrame.loc[lastIndex, 'deaths']
        return total

    def lastCoupleDays(self, days):
        sumList = []
        lastIndex = self.lastIndex
        dailyChange = self.dailyDataFrame()
        for number in range(days):
            change = dailyChange.loc[lastIndex,'Daily Change']
            sumList.append(change)
            lastIndex -= 1
        total = sum(sumList)
        return total

    def dailyChangeDF(self):
        pass

    def dailyDataFrame(self):
        # This creates a list that will be used to create the dailyDataFrame which shows
        # a dataframe containing the number of cases and the change between the current date
        # and the previous day

        # First, need to get the index of the last date. Then it creates a loop that will
        # give the difference between a current date and the previous day.
        # It then appends the differnce to the change list.
        # Returns the change list.
        change = []
        i = 1
        length = self.DataFrame.index[-1]

        for item in range(length, 0, -1):
            currentIndex = self.DataFrame.index[-i]
            currentDate = self.DataFrame.loc[currentIndex, 'date']
            currentCases = self.DataFrame.loc[currentIndex, 'cases']

            #previousDayDate = self.DataFrame.loc[currentIndex-1,'date']
            previousDayCases = self.DataFrame.loc[(currentIndex-1), 'cases']

            difference = currentCases-previousDayCases
            change.append([currentDate, currentCases, difference])
            i += 1
        atZeroCases = self.DataFrame.loc[0, 'cases']
        atZeroDate = self.DataFrame.loc[0, 'date']
        zeroInsert = [atZeroDate, atZeroCases, 0]
        change.reverse()
        change.insert(0, zeroInsert)
        daily = pd.DataFrame(
            change, columns=['Date', 'Total Cases', 'Daily Change'])
        self.Daily = daily
        return self.Daily

    def deathDailyDataFrame(self):
        change = []
        i = 1
        length = self.DataFrame.index[-1]
        for item in range(length, 0, -1):
            currentIndex = self.DataFrame.index[-i]
            currentDate = self.DataFrame.loc[currentIndex, 'date']
            currentDeaths = self.DataFrame.loc[currentIndex, 'deaths']

            previousDayDeaths = self.DataFrame.loc[(currentIndex-1), 'deaths']

            difference = currentDeaths-previousDayDeaths
            change.append([currentDate, currentDeaths, difference])
            i += 1
        atZeroDeaths = self.DataFrame.loc[0, 'deaths']
        atZeroDate = self.DataFrame.loc[0, 'date']
        zeroInsert = [atZeroDate, atZeroDeaths, 0]
        change.reverse()
        change.insert(0, zeroInsert)
        deathsDaily = pd.DataFrame(
            change, columns=['Date', 'Total Deaths', 'Daily Change'])
        self.deathsDaily = deathsDaily
        return self.deathsDaily

    def saveAsCSV(self, name):
        return self.Daily.to_csv(name)


def getTotalCases():
    lastIndex = usTotal.index[-1]
    totalCases = usTotal.loc[lastIndex, 'cases']
    return totalCases


def getTotalDeaths():
    lastIndex = usTotal.index[-1]
    totalDeaths = usTotal.loc[lastIndex, 'deaths']
    return totalDeaths


def USDeathChange():
    # This creates a list that will be used to create the dailyDataFrame. 
    # The dailyDataFrame shows a dataframe containing the number of cases 
    # and the change between the current date and the previous day

    # First, need to get the index of the last date. Then it creates a loop that will
    # give the difference between a current date and the previous day.
    # It then appends the differnce to the change list.
    # Returns the change list.
    
    change = []
    i = 1
    length = len(usTotal)
    index = usTotal.index[-1]
    lastDateCases = usTotal.loc[index, 'deaths']
    for item in range(length-1, 0, -1):
        currentIndex = usTotal.index[-i]
        currentDate = usTotal.loc[currentIndex, 'date']
        currentDeaths = usTotal.loc[currentIndex, 'deaths']
        previousDayDeaths = usTotal.loc[(currentIndex-1), 'deaths']
        difference = currentDeaths-previousDayDeaths
        change.append([currentDate, currentDeaths, difference])
        i += 1
    atZeroDeaths = usTotal.loc[0, 'deaths']
    atZeroDate = usTotal.loc[0, 'date']
    zeroInsert = [atZeroDate, atZeroDeaths, 0]
    change.reverse()
    change.insert(0, zeroInsert)
    deathsDaily = pd.DataFrame(
        change, columns=['Date', 'Total Deaths', 'Daily Change'])

    return deathsDaily


def USCaseChange():
    change = []
    i = 1
    length = len(usTotal)
    index = usTotal.index[-1]
    lastDateCases = usTotal.loc[index, 'cases']
    for item in range(length-1, 0, -1):
        currentIndex = usTotal.index[-i]
        currentDate = usTotal.loc[currentIndex, 'date']
        currentCases = usTotal.loc[currentIndex, 'cases']
        previousDayCases = usTotal.loc[(currentIndex-1), 'cases']
        difference = currentCases-previousDayCases
        change.append([currentDate, currentCases, difference])
        i += 1
    atZeroCases = usTotal.loc[0, 'cases']
    atZeroDate = usTotal.loc[0, 'date']
    zeroInsert = [atZeroDate, atZeroCases, 0]
    change.reverse()
    change.insert(0, zeroInsert)
    casesDaily = pd.DataFrame(
        change, columns=['Date', 'Total Cases', 'Daily Change'])
    return casesDaily


def makeStateDF(name):
    name = stateDataFrame(str(name))
