import pandas as pd
from datetime import *

# read the file
df = pd.read_csv('us-states.csv')

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
          'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
          'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
          'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
          'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
          'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
          'West Virginia', 'Wisconsin', 'Wyoming']


# We will need to make a couple of dictionaries or lists that make other lists and dictionaries with the
# corresponding state name
dictList = {key:{} for key in states}
# These lists will be used to create individual DataFrames for the states
casesList = {key: [] for key in states}
# These dictionaries are for the actual DataFrames
stateDataF = {key:{} for key in states}


def changeDate(aDate):
    aDate = datetime.strptime(aDate, '%Y-%m-%d')
    finalDate = aDate.date()
    return finalDate

# Need to assign a dictionary to the states
for state in states:
    stateFilter = (df['state']==state)
    dictList[state]= df[stateFilter]
    dictList[state].reset_index(inplace=True)

# This function returns the date of the first reported case
def getFirstEvent(name):
    result = dictList[name].loc[0, 'date']
    return result


# This function returns the number of days between the first case and the first death
def caseToDeath(state):
    minList = []
    # We want to find the date of the first death so it has to be greater than 0, if we append it to a list,
    # then we can get the first value and that will be the date of the first death
    for ind, row in dictList[state].iterrows():
        if row[5] > 0:
            minList.append(row[1])
    firstDeath = minList[0]
    firstCaseDate = getFirstEvent(state)
    # change the dates to datetime objects to be able to get difference between first death date and first case date
    firstDeathDate = changeDate(firstDeath)
    firstCaseDate = changeDate(firstCaseDate)
    daysInBetween = firstDeathDate - firstCaseDate
    daysInBetween = daysInBetween.days

    return daysInBetween

# Returns the numbers of cases or deaths for the date
def eventsOnDate(state, date,event):
    dictList[state].reset_index(inplace=True)
    dictList[state].set_index('date',inplace=True)
    if event == 'cases':
        result = dictList[state].loc[date,'cases']
    elif event == 'deaths':
        result = dictList[state].loc[date,'deaths']
    return result

# This returns the number of cases between the specified dates
def casesBetweenDates(state,firstDate,secondDate):
    firstResults = eventsOnDate(state, firstDate,'cases')
    secondResults = eventsOnDate(state, secondDate,'cases')
    firstResults = int(firstResults)
    secondResults = int(secondResults)
    difference = secondResults - firstResults
    return difference

# To be used later
def previousDate(date):
    date = changeDate(date)
    dateBefore = date - timedelta(days=1)
    return dateBefore

# This function returns a DataFrame that shows the number of new cases for
def caseChanges(state):
    # make it easier to access
    stateDF = dictList[state]
    # Will be used for indexing
    i = 1

    stateDF.reset_index(inplace=True)

    otherLastIndex = stateDF.index[-1]

    for item in range(otherLastIndex, 0, -1):
        # The last index
        lastIndex = stateDF.index[-i]

        # Date that corresponds to the last index
        lastDate = stateDF.loc[lastIndex, 'date']

        # Number of casese that correspond to the last date
        lastDateCases = stateDF.loc[lastIndex, 'cases']

        # Date for the day before
        dayBefore = stateDF.loc[lastIndex - 1, 'date']

        # The cases for the day before the last index
        previousDayCases = stateDF.loc[(lastIndex - 1), 'cases']

        # Change between the previous day cases and the last date cases
        difference = lastDateCases - previousDayCases
        dateString = str(dayBefore) + ' to ' + str(lastDate)

        # Add to the list that will be transformed into a DataFrame
        casesList[state].append([dayBefore, previousDayCases, lastDate, lastDateCases, dateString, difference])
        # casesList[state].append(dayBefore)
        i += 1
    casesList[state].reverse()

    return difference