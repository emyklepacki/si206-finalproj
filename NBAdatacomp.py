#access and store 100 items in database from your API in at least one table 
#limit how much data you store from an API into the database each time you execute the file that stores data to the database to 25 or fewer items 




#import stuff 
import http.client
import json
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import os
import sqlite3
import unittest
import time

#code to create the teams table, used to match up teams and their id numbers 
# example response:
#{'id': 1, 'name': 'Atlanta Hawks', 'nickname': 'Hawks', 'code': 'ATL', 'city': 'Atlanta', 'logo': 'https://upload.wikimedia.org/wikipedia/fr/e/ee/Hawks_2016.png', 'allStar': False, 'nbaFranchise': True, 'leagues': {'standard': {'conference': 'East', 'division': 'Southeast'}, 'vegas': {'conference': 'summer', 'division': None}, 'utah': {'conference': 'East', 'division': 'Southeast'}, 'sacramento': {'conference': 'East', 'division': 'Southeast'}}}
#input is the id value you want to start at, and the database you want to store information to 
#output is nothing, but it inputs data to the database
def teamtable(start, db):
	#accessing the API
	conn = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")

	headers = {
    'X-RapidAPI-Key': "0789cc1cd1mshc148ec2619dac87p1a462ajsn9b6d75d5dad6",
    'X-RapidAPI-Host': "api-nba-v1.p.rapidapi.com"
    }

	conn.request("GET", "/teams", headers=headers)
	#getting the data from the API
	res = conn.getresponse()
	teams = res.read()

	dteams = json.loads(teams.decode("utf-8"))
	dtresponse = dteams['response']
	#connecting to the database 
	conn = sqlite3.connect(db)
	cur = conn.cursor()
	#create table
	cur.execute('CREATE TABLE IF NOT EXISTS NBATeams (id INTEGER, name TEXT PRIMARY KEY)')
	#adding team to the database
	for team in dtresponse:
		#making sure its an NBA team and that it is the team specified 
		if team['nbaFranchise'] == True and team['id'] == start:
			cur.execute('INSERT OR IGNORE INTO NBATeams (id,name) VALUES (?,?)', (team['id'],team['name']))
			
	conn.commit()
	


# code to get season stats for 5 teams 
#example response
#{'games': 94, 'fastBreakPoints': 941, 'pointsInPaint': 4334, 'biggestLead': 1237, 'secondChancePoints': 1318, 'pointsOffTurnovers': 1394, 'longestRun': 1026, 'points': 10550, 'fgm': 3782, 'fga': 8204, 'fgp': '46.2', 'ftm': 1829, 'fta': 2261, 'ftp': '80.9', 'tpm': 1157, 'tpa': 3174, 'tpp': '36.3', 'offReb': 971, 'defReb': 3292, 'totReb': 4263, 'assists': 2197, 'pFouls': 1870, 'steals': 653, 'turnovers': 1198, 'blocks': 433, 'plusMinus': 124}
#input is the id of the team you want stats for and the database you're putting data into 
# output is nothing 
def getstats(id,db):
	#connecting to database to create table
	conn = sqlite3.connect(db)
	cur = conn.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS NBASeasonStats (id INTEGER PRIMARY KEY, games INTEGER, points INTEGER, pointsinpaint INTEGER, rebounds INTEGER, assists INTEGER, pfouls INTEGER, steals INTEGER, turnovers INTEGER, blocks INTEGER)')

	#accessing API
	conn = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")

	headers = {
    'X-RapidAPI-Key': "0789cc1cd1mshc148ec2619dac87p1a462ajsn9b6d75d5dad6",
    'X-RapidAPI-Host': "api-nba-v1.p.rapidapi.com"
    	}

	conn.request("GET", "/teams/statistics?id={}&season=2020".format(id), headers=headers)
	#getting the data 
	res = conn.getresponse()
	data = res.read()
	respdict = json.loads(data.decode("utf-8"))
	print(respdict)
	resp = respdict['response']
	team = resp[0]
	#connecting to the database and adding the data 
	conn = sqlite3.connect(db)
	cur = conn.cursor()
	cur.execute('INSERT OR IGNORE INTO NBASeasonStats (id,games,points,pointsinpaint,rebounds,assists,pfouls,steals,turnovers,blocks) VALUES (?,?,?,?,?,?,?,?,?,?)',(id,team['games'],team['points'],team['pointsInPaint'],team['totReb'],team['assists'],team['pFouls'],team['steals'],team['turnovers'],team['blocks']))
	conn.commit()
	

#choosing the database
deeb = "sports.db"
#connecting to the database 
conn = sqlite3.connect(deeb)
cur = conn.cursor()
#doing the first value, in order to ensure the database is set up
getstats(1,deeb)
teamtable(1,deeb)
#getting the highest id (primary key) from the table, to figure out where to start adding values from 
cur.execute('SELECT MAX(id) FROM NBASeasonStats')
statstart = cur.fetchone()[0]
cur.execute('SELECT MAX(id) FROM NBATeams')
teamstart = cur.fetchone()[0]
#loop to add 11 values to each database for each time you run the file
for i in range(teamstart+1,teamstart+12):
	#there are only 41 teams, so don't want to go above it
	if i > 41:
		break
	else:
		teamtable(i,deeb)
	#time delay added so as to not go over the allotted requests per minute for the API
	time.sleep(8)
for i in range(statstart+1,statstart+12):
	#breaks once i is larger than the amount of rows in the data set 
	if i > 100: 
		break
	else:
		getstats(i,deeb)
	#time delay to avoid the requests per minute issue
	time.sleep(8)




	






	
	