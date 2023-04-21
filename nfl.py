
import requests
import matplotlib.pyplot as plt
import sqlite3

def load_data_25(db):
    response = requests.get("https://api.collegefootballdata.com/draft/picks?year=2022", headers = {"accept": "application/json", "Authorization":"Bearer 4ThlVHwnLufpOPUo/4CRM9OoQ0ekJEpzEiv2nqKO64J8OntrgEPvBxO/ilSriJ9r"})
    data = response.json()
    
    # connect to the database
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # create the table
    cur.execute('''CREATE TABLE IF NOT EXISTS nfl_data
                (nfl_athlete_id INTEGER PRIMARY KEY,
                college_athlete_id INTEGER,
                college_id INTEGER,
                college_team TEXT,
                college_conference TEXT,
                nfl_team TEXT,
                year INTEGER,
                overall INTEGER,
                round INTEGER,
                pick INTEGER,
                name TEXT,
                position TEXT,
                height INTEGER,
                weight INTEGER,
                pre_draft_ranking INTEGER,
                pre_draft_position_ranking INTEGER,
                pre_draft_grade INTEGER)''')

    rows = 0
    for player in data:
        playerdata = (player['nflAthleteId'], player['collegeAthleteId'], player['collegeId'], player['collegeTeam'], player['collegeConference'], player['nflTeam'], player['year'], player['overall'], player['round'], player['pick'], player['name'], player['position'], player['height'], player['weight'], player['preDraftRanking'], player['preDraftPositionRanking'], player['preDraftGrade'])
        if cur.execute('SELECT * FROM nfl_data WHERE nfl_athlete_id = ' + str(player['nflAthleteId'])).fetchall() == []:
            cur.execute("INSERT OR IGNORE INTO nfl_data (nfl_athlete_id, college_athlete_id, college_id, college_team, college_conference, nfl_team, year, overall, round, pick, name, position, height, weight, pre_draft_ranking, pre_draft_position_ranking, pre_draft_grade) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", playerdata)
            rows += 1
        if rows == 25:
            break
    
    conn.commit()
    conn.close()

def load_data_full(db):
    for i in range(11):
        load_data_25(db)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    teamdata = {}
    athletes = cur.execute('SELECT nfl_team FROM nfl_data')
    for athlete in athletes:
        if athlete[0] in teamdata:
            teamdata[athlete[0]] += 1
        else:
            teamdata[athlete[0]] = 1

    conn.close()
    teamdata_sort = sorted(teamdata.items(), key=lambda x: x[1], reverse=True)
    names = [x[0] for x in teamdata_sort]
    counts = [x[1] for x in teamdata_sort]
    outfile = open('nfldraft.txt', 'w')
    outfile.write("Players Drafted Per Team in the 2022 NFL Draft:")
    for i in range(len(names)):
        outfile.write("\n" + names[i] + ": " + str(counts[i]))
    outfile.close()
    return teamdata

def graphdata(datadict):
    datadict_sort = sorted(datadict.items(), key=lambda x: x[1], reverse=False)
    names = [x[0] for x in datadict_sort]
    counts = [x[1] for x in datadict_sort]
    plt.barh(names, counts, color=('purple'))
    plt.title('Players Drafted Per Team in the 2022 NFL Draft:')
    plt.ylabel('Teams')
    plt.xlabel('Number of Players')
    plt.tight_layout()
    plt.show()

graphdata(load_data_full("sports.db"))