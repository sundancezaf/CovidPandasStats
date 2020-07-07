import pandas as pd
import matplotlib.pyplot as plt
from datetime import *

# The following line is to show inline graphs in jupyter so disregard if not on a jupyter notebook uncomment if needed

# %matplotlib inline 

# These options are for jupyter notebook to show max rows, columns as specified
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# read the file
df = pd.read_csv('us-states.csv')

# This csv contains the population numbers for the states
popDF = pd.read_csv('population.csv', index_col='state')

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
          'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
          'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
          'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
          'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
          'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
          'West Virginia', 'Wisconsin', 'Wyoming']

# This creates separate dictionaries 
dictList = {key:{} for key in states}
# These lists will be used to create individual DataFrames for the states
casesList = {key: [] for key in states}
# These dictionaries are for the actual DataFrames
stateDataFrame = {key:{} for key in states}

# Need to assign a dictionary to the states
for state in states:
    # This filters out the values in the data by state
    stateFilter = (df['state']==state)  
    # This creates a dictionary from the filtered results 
    dictList[state]= df[stateFilter]
    # This will reset the index in case it's messed up
    dictList[state].reset_index(inplace=True)

# This function transforms a date to a Python date
def changeDate(aDate):
    aDate = datetime.strptime(aDate, '%Y-%m-%d')
    finalDate = aDate.date()
    return finalDate

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
   
# 
def previousDate(date):
    date = changeDate(date)
    dateBefore = date - timedelta(days=1)
    return dateBefore

# This function returns the population for the state
def eventsPerCapita(name):
    stateyDF = dictList[name]
    population = popDF.loc[name,'population']
    # last index to get the total number of cases
    lastIndex =  stateyDF.index[-1]
    totalEvents = stateyDF.loc[lastIndex,'cases']
    # instead of multiplying by 100K at the end, divide pop by 100K and then divide total events
    # by the result
    perHundred = population / 100000
    difference = totalEvents/perHundred
    return difference

# This function returns a DataFrame that shows the number of new cases for
def caseChanges(state):
    
    # make it easier to access
    stateDF = dictList[state]
    # Will be used for indexing
    i = 1
    
    # this gets the population for the state
    population = popDF.loc[state,'population']
    
    # To find the cases per Capita we need to divide the population by 100K
    perHundred = population/100000
    
    # This resets the index
    stateDF.reset_index(inplace=True)
    
    # This finds the last index number for the state DF
    otherLastIndex = stateDF.index[-1]
    
    for item in range(otherLastIndex,0,-1):
        
        # The last index
        lastIndex = stateDF.index[-i]
        
        # Date that corresponds to the last index
        lastDate = stateDF.loc[lastIndex,'date']
        
        # Number of cases that correspond to the last date
        lastDateCases = stateDF.loc[lastIndex,'cases']
        
        # Cases per capita for last date
        lastDatePerCapita = lastDateCases/perHundred
        
        # Date for the day before
        dayBefore = stateDF.loc[lastIndex-1,'date']
        
         # The cases for the day before the last index
        previousDayCases = stateDF.loc[(lastIndex-1),'cases']
        
        # Previous day cases per capita
        previousDayPerCapita = previousDayCases/perHundred
        
        # Change between the previous day cases and the last date cases
        difference = lastDateCases - previousDayCases
        dateString = str(dayBefore) + ' to ' + str(lastDate)        
        
        # Add to the list that will be transformed into a new DataFrame
        casesList[state].append([lastDate,lastDateCases,lastDatePerCapita,difference])
        #casesList[state].append(dayBefore)
        i+=1
    casesList[state].reverse()
     
    return difference

for name in states:
    caseChanges(name)

# This creates the states DataFrames using the following column names: 'Date','Total Cases','per Capita', 'Daily Change'
for stateName in states:
    stateDataFrame[stateName]=pd.DataFrame(casesList[stateName],columns=['Date','Total Cases','per Capita','Daily Change'])


# To access the newly created DataFrames do as follows:
print(stateDataFrame['Texas'])

# This function finds the sum of the new cases for the specified days for the specified state
# Ex. If you want to find out the new cases in the last 5 days for California
# you can do so as: print(lastCoupleDays("California",5))
def lastCoupleDays(state, days):
    daysList = []
    daysDF = stateDataF[state]
    i = 1
    lastIndex = daysDF.index[-1]
    totalDays = lastIndex - days
    # 
    for numba in range(lastIndex,totalDays,-1):
        findIndex = daysDF.index[-i]
        allCases = daysDF.loc[findIndex,'Daily Change']
        daysList.append(allCases)
        i+=1
    totalNumber = sum(daysList)
    return totalNumbe


# This function gives the total number of cases in the United States
def totalCasesUS():
    totalCasesList =  []
    for aState in states:
        lastIndex = stateDataF[aState].index[-1]
        totalCases = stateDataF[aState].loc[lastIndex, 'Total Cases']
        totalCasesList.append(totalCases)
    total = sum(totalCasesList)
    return total

# The following comman is if you are using a Jupyter Notebook, you can use the following format to look at graphs
# uncomment to use

#stateDataFrame['New Hampshire'].plot(x='Date', y='Daily Change', kind='line')