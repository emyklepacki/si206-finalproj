#calculate something from the data 
#do at least one database join to select your data for your calculations/visualizations 
#write out the calculated data to a file as text 
import http.client
import json
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import os
import sqlite3
import unittest
import time
import numpy as np

#setting the desired database and connecting to it 
deeb = "sports.db"
conn = sqlite3.connect(deeb)
cur = conn.cursor()

#getting the NBA team ids
cur.execute('SELECT id FROM NBATeams')
nbaids = cur.fetchall()


#input is the list of team id's 
#output is a list of tuples with the format team id, team name, games per season, points per season
def teaminfo(idlist):
	ppergamebyid = []
	for id in idlist:
		#join statement to match up id's and names from the two separate NBA tables and get all the data 
		cur.execute('SELECT NBASeasonStats.id, NBATeams.name, NBASeasonStats.games, NBASeasonStats.points FROM NBASeasonStats JOIN NBATeams on NBASeasonStats.id = NBATeams.id WHERE NBASeasonStats.id = ?',id)
		points = cur.fetchone()
		t = (points[0],points[1],points[2],points[3])
		ppergamebyid.append(t)
	return ppergamebyid
#running the team info function, and saving it as a variable 
ts = teaminfo(nbaids)
#opening the file to write calculations to 
f= open("NBAcalc.txt","w")
#input is the list of tuples with the format team id, team name, games per season, points per season
#output is nothing, but it writes to a file 
def calc_pper(pperlist,f):
	#header 
	f.write("NBA Teams Average Points Per Game for the 2020 Season\n")
	f.write("\n")
	ppers = []
	
	for team in pperlist:
		#making sure the team did not play 0 games 
		if team[2] != 0:
			#saving each value as a more easily accessible /understandable variable 
			id = team[0]
			name = team[1]
			games = team[2]
			points = team[3]
			#calculate points per game
			pper = round(float(int(points)/int(games)),2)
			t = (name,pper)
			#adding it to a list of pper game
			ppers.append(t)
			#writing the data to the file
			write = "The "+name+" had "+str(points) + " points in "+ str(games) + " games in the 2020 season, averaging "+str(pper)+ " points per game.\n"
			f.write(write)
			f.write("-------------------------\n")
	#sorting points per game, most to least 
	sortppers = sorted(ppers, key=lambda x:x[1], reverse=True)
	highest = sortppers[0]
	lowest = sortppers[-1]
	#writing out the highest and lowest scoring teams on average 
	write = "The "+ highest[0]+" had the highest average points per game at "+str(highest[1])+" points per game\n"
	f.write(write)
	f.write("AND\n")
	write = write = "The "+ lowest[0]+" had the lowest average points per game at "+str(lowest[1])+" points per game\n"
	f.write(write)


#writing out the file
calc_pper(ts,f)
#close file 
f.close()
#creating a list of tuples to use for the bar chart in the format of name, pper game
tave = []
for team in ts:
	if team[2] != 0:
			
			name = team[1]
			games = team[2]
			points = team[3]
			pper = round(float(int(points)/int(games)),2)
			t = (name,pper)
			tave.append(t)
tave = sorted(tave, key=lambda x:x[1])
#input is a list of tuples in the format name, ave points per game 
# output is none, but it produces a bar chart 	
def vis(tavers):
	
	figure(figsize=(2,1),dpi = 80)
	x = []
	y = []
	#separating out the x and y values from the tuple list 
	for val in tavers:
		x.append(val[0])
		y.append(val[1])
	plt.barh(x,y, color = "pink")
	plt.xticks(rotation = 45)
	plt.xlabel("Teams", fontweight = "bold")
	plt.ylabel("Average Points Per Game", fontweight = "bold")
	plt.title("Average Points Per Game for NBA Teams in the 2020 Season", fontweight = "bold")
	
	
	plt.show()

vis(tave)










