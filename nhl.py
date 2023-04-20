# Your name: Emy Klepacki
# Your student id: 55166246
# Your email: klepacki@umich.edu

import matplotlib
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import requests
import json

# PART 2 -- gather data into DB
def setUpDatabase():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect("sports.db")
    cur = conn.cursor()
    return cur, conn

def getAPI(url):
    response = requests.get(url)
    json_file = response.json()
    # print(json_file)
    return json_file

def create_team_table(cur, conn):
    # cur.execute("DROP TABLE IF EXISTS nhldraft2022")
    cur.execute("CREATE TABLE nhldraft2022 (pickOverall INTEGER PRIMARY KEY, teamID INTEGER, playerID INTEGER, name TEXT, team TEXT)")

    
def add_draft_data(cur, conn, jfile):
    # print(jfile)
    count = 1
    ifbreak = False
    data = jfile.get('drafts')
    data = data[0]
    data = data.get('rounds')
    for i in range(len(data)):
        if (ifbreak):
            break
        picks = data[i].get('picks')
        for pick in picks:
            pickOverall = pick.get('pickOverall') #1
            team = pick.get('team')
            teamID = team.get('id') #2
            teamName = team.get('name') # 5
            prospect = pick.get('prospect')
            playerName = prospect.get('fullName') #4
            playerID = prospect.get('id') #3
            test = cur.execute("SELECT * FROM nhldraft2022 WHERE name = ?", (playerName, )).fetchall() # see if exists
            if (len(test) == 0):
                cur.execute("INSERT INTO nhldraft2022 (pickOverall, teamID, playerID, name, team) VALUES (?,?, ?, ?, ?)",(pickOverall , teamID, playerID, playerName, teamName))
                count += 1
                if(count == 26):
                    ifbreak = True
                    break
    
    conn.commit()    
    
#  PART 3- PROCESS DATA
    # will be calculating the count of how many times a team shows up
    # data in draftTeams.csv

def calculate_teams(cur, conn):
    filename = "draftTeams.csv"
    teams = cur.execute("SELECT team FROM nhldraft2022").fetchall() 
    teamDict = {}

    for team in teams:
        test = teamDict.get(team[0])
        if(test == None):
            teamDict[team[0]] = 1
        else:
            teamDict[team[0]] += 1
    
    # print(teamDict)
    fout= open(filename, 'w')
    fout.write("Team Counts for 2022 NHL Draft:\n")
    data = sorted(teamDict, key = lambda t:t[1])
    for data in teamDict:
        fout.write(data)
        fout.write(": ")
        fout.write(str(teamDict[data]))
        fout.write("\n")
    fout.close()
    return teamDict

# PART 4 -- VISUALIZE DATA
def visualizeData(cur, conn, dct):
    teamLst = []
    countLst = []
    for d in dct:
        print(d)
        teamLst.append(d)
        countLst.append(dct[d])
    fig,ax = plt.subplots()
    ax.barh(teamLst, countLst, color='purple')
    ax.set_facecolor('pink')
    ax.set_xlabel('Draft Prospect Counts')
    ax.set_ylabel('NHL Teams')
    ax.set_title('2022 Draft Counts by NHL Team', fontsize=20)
    ax.grid()
    plt.show()


# MAIN
def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase()
    draft2022 = getAPI('https://statsapi.web.nhl.com/api/v1/draft/2022')
    # CREATE TABLE IF DOESNT ALREADY EXIST
    # cur.execute("DROP TABLE nhldraft2022")
    # try:
    #     cur.execute("SELECT * FROM nhldraft2022")
    # except:
    #     create_team_table(cur,conn)
    # #
    # add_draft_data(cur, conn, draft2022)
    teamDict = calculate_teams(cur, conn)
    visualizeData(cur, conn, teamDict)
    
    




if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)