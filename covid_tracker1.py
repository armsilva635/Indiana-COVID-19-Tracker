#!/usr/bin/env python
import xlrd
import time as t
from covid_tracker2 import *
    
def countyStats(countyNum):
    #For each county data saved like:
    #[Location ID, Covid Count, Covid Test, County Name]
    
    stats = [excelSheet.cell(countyNum,i).value for i in range(5)]
    
    return stats

def stateStats():
    #Tallies up state total
    #92 counties
    
    stats = [0,0,0]
    
    for i in range(1, 93):
        for x in range(1,4):
            stats[x-1] += int(excelSheet.cell(i,x).value)
            
    return stats

def formMessage():
    # Forms an HTML message to send through email for each county
    # Checks previous day cases numbers and finds difference

    global oldTotal

    # Add county and county number here
    counties_dict = {"LAKE": countyStats(45),"MARION": countyStats(49), "MONROE": countyStats(53)}
    
    message = ""

    for county in counties_dict:
        m = countyMessage(counties_dict[county][4].title(), int(counties_dict[county][1]), int(counties_dict[county][2]), int(counties_dict[county][3]))
        message += m
        if int(counties_dict[county][1]) > int(oldCounties[county]):
            difference = int(counties_dict[county][1]) - int(oldCounties[county])
            message += "<b>New cases in "+counties_dict[county][4].title()+" County: +" + "{:,}".format(difference)+"</b><br>"
            oldCounties[county] = int(counties_dict[county][1])
        else:
            oldCounties[county] = int(counties_dict[county][1])

    # Creates message for state totals
    state = stateStats()
    message += stateMessage(state[0],state[1],state[2])
    if oldTotal < state[0]:
        diff = state[0] - oldTotal
        message += "<b>Total new cases: +" + "{:,}".format(diff)+"</b>"
        oldTotal = state[0]
    else:
        oldTotal = state[0]

    return message

def usaMessage():
    # Creates United States cases total messsage
    
    global oldCases
    
    cases, USA = usaData()
    message = USA

    if oldCases < cases:
        diff = cases - oldCases
        message += "<b>Total new cases: +" + "{:,}".format(diff)+"</b>"
        oldCases = cases
    else:
        oldCases = cases

    return message

#Opens file with email login information
login = ''
with open('credentials.txt','r') as f:
    login = f.readlines()

#Loads list of emails to send message to
emails = ''
with open('emails.txt','r') as f:
    emails = f.readlines()
        
# Must match counties_dict, this keeps track of counties previous day totals
oldCounties = {"LAKE": 0,"MARION": 0, "MONROE": 0}

# Tracks country totals
oldTotal = 0
oldCases = 0
oldMessage = ""
oldCount = []

while True:
    #Pulls Indiana data and opens excelsheet
    getData()
    excelSheet = xlrd.open_workbook('data.xls')
    excelSheet = excelSheet.sheet_by_name("Report")

    message = formMessage()

    # Constructs HTML email
    if message != oldMessage:
        oldMessage = message
        message += usaMessage()
        top_news = news()
        message += top_news
    
    for email in emails:
        email(login[0],login[1], str(email), "Indiana COVID-19 Update", message)
        print("Sent\n")
    else:
        print("Not sent\n")
        oldMessage = message

    #Runs every 12 hours    
    t.sleep(60*60*12)







