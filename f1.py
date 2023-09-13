import xdrlib
import pandas            as pd
import streamlit         as st
import seaborn           as sns
import numpy as np
import matplotlib.pyplot as plt
from PIL                 import Image
from io                  import BytesIO
from pandas_profiling import ProfileReport
import matplotlib.cm as cm
import matplotlib.colors as colors
import tkinter
import matplotlib
matplotlib.use('TkAgg')



custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

@st.cache(allow_output_mutation=True)
def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True) 

def main():
    st.set_page_config(page_title = 'F1 Analises', \
        page_icon = "C:\\Users\\Fernanda\\Downloads\\f1.png",
    )
 
    st.write('# Analisando o 2022 da F1')
    st.markdown("---")

    image = Image.open("C:\\Users\\NandaeDigo\\Downloads\\f12.jpg")
    st.sidebar.image(image)

if __name__ == '__main__':
	main()
    

drivers = pd.read_csv(R"C:\\Users\NandaeDigo\\Downloads\\Formula1_2022season_drivers.csv",sep=',')
calend = pd.read_csv("C:\\Users\\NandaeDigo\\Downloads\\Formula1_2022season_calendar.csv", sep=',')
calend.set_index('Round', inplace=True)
raceResults = pd.read_csv("C:\\Users\\NandaeDigo\\Downloads\\Formula1_2022season_raceResults.csv", sep=',')
sprintQualiResults = pd.read_csv("C:\\Users\\NandaeDigo\\Downloads\\Formula1_2022season_sprintRaceResults.csv", sep=',')
teams = pd.read_csv("C:\\Users\\NandaeDigo\\Downloads\\Formula1_2022season_teams.csv", sep=',')
teams.index = range(1,11)
  
drivers[['No', 'Driver', 'Country', 'Date of Birth', 'Place of Birth', 'Team', 'World Championships', 'Grands Prix Entered',
         'Podiums', 'Points', 'Highest Race Finish', 'Highest Grid Position']]

calend[['GP Name', 'Country', 'City', 'Circuit Name', 'Race Date', 'Number of Laps', 'Turns', 'DRS Zones', 
          'Race Distance(km)', 'Lap Record', 'Record Owner', 'Record Year']]

raceResults[['Track', 'Position', 'No','Driver', 'Team', 'Starting Grid', 'Laps', 'Time/Retired', 'Points', '+1 Pt', 'Fastest Lap']]

driverPts = raceResults.groupby(['Driver', 'Team'])['Points'].sum()
sprintQualiDriverPts = sprintQualiResults.groupby(['Driver', 'Team'])['Points'].sum()
driverPts = (driverPts+sprintQualiDriverPts).sort_values(ascending=False).reset_index()
driverPts.index = [i for i in range(1,23)]
driverPts      

def assign_color(val_type, values):
    cl = []
    for val in values:
        if val_type == 'drivers':  abbr = val.split()[1].upper()[0:3]
        elif val_type == 'teams':  abbr = val[0:4].upper()
        if abbr in ['ALFA','ZHO','BOT']:   cl.append('#900000')
        elif abbr in ['HAAS','MSC','MAG']:       cl.append('#ffffff')
        elif abbr in ['ASTO','VET','STR','HUL']:       cl.append('#006f62')
        elif abbr in ['WILL','ALB','LAT','DEV']:       cl.append('#0072ff')
        elif abbr in ['ALPH','GAS','TSU']:       cl.append('#2b5962')
        elif abbr in ['MCLA','RIC','NOR']:       cl.append('#ff8700')
        elif abbr in ['RED ','VER','PER']:       cl.append('#0600f0')
        elif abbr in ['FERR','LEC','SAI']:       cl.append('#cb0000')
        elif abbr in ['MERC','HAM','RUS']:       cl.append('#00d2bd')
        elif abbr in ['ALPI','ALO','OCO']:       cl.append('#0090ff')
    return cl 

tracks = raceResults['Track'].unique()
plt.style.use('seaborn')
plt.style.use('white_background')
plt.rcParams['axes.facecolor'] = '#15151d'
plt.rcParams['figure.facecolor'] = '#15151d'
plt.rcParams['grid.color'] = '#444444'
top10 = driverPts['Driver'].values[:10]
("drivers", top10)
plt.figure(figsize=(16,7))
plt.axis([-0.4, 21.4, -10, 410])
for i in range(len(top10)):
    ls = '-'
    pts = raceResults[raceResults['Driver'] == top10[i]]['Points'].values
    if top10[i] == "Max Verstappen":     pts[9] += 3;  pts[13] += 2;  pts[18] += 2
    elif top10[i] == "Lewis Hamilton":   pts[9] += 2;
    elif top10[i] == "Valtteri Bottas":  pts[9] += 1;  pts[13] += 3;  pts[18] += 3;  ls = '--';
    elif top10[i] == "Daniel Ricciardo":  pts[13] += 1;  ls = '--';
    elif top10[i] == "Carlos Sainz":     pts[18] += 1;
    elif top10[i] == "Sergio Perez" or top10[i] == "Charles Leclerc":  ls = '--'
    plt.plot(np.cumsum(pts), linewidth=3, label=top10[i].split()[1], linestyle=ls)
plt.title("Formula 1 - 2021 Season\nTop 10 Drivers' Points Progression", color='#bbbbbb', fontsize=22, fontweight='bold')
plt.legend(fontsize=15)
plt.xlabel('RACES', fontsize=16, color='#ffff55', fontweight='bold')
plt.xticks(range(0,len(tracks)), tracks, fontsize=14, color='#ffff55', rotation=80)
plt.ylabel('POINTS', fontsize=16, color='#ffff55', fontweight='bold')
plt.yticks(fontsize=14, color='#ffff55')
plt.show()



verPts = raceResults[raceResults['Driver'] == 'Max Verstappen']['Points'].values
verPts[9] += 3;  verPts[13] += 2;  verPts[18] += 2
LecPts = raceResults[raceResults['Driver'] == 'Charles Leclerc']['Points'].values
LecPts[9] += 2
pointsGap = np.cumsum(verPts) - np.cumsum(LecPts)
c = []
for i in range(len(pointsGap)):
    if pointsGap[i] >= 0:   c.append('#DAA520')
    else:    c.append('#00FF00')
plt.figure(figsize=(16,7))
plt.axis([-0.7, 21.7, min(pointsGap)-3, max(pointsGap)+4])
plt.bar(tracks, pointsGap, color=c)
for i in range(len(pointsGap)):
    if pointsGap[i] >= 0:   vsh = 0.5
    else:   vsh = -2
    plt.text(i-0.2, pointsGap[i]+vsh, "{:2}".format(int(abs(pointsGap[i]))), fontsize=16)
plt.axhline(0, color='#000000')
plt.text(17.5, 32, "VERSTAPPEN", color='#000000', fontsize=20, fontweight='bold')
plt.text(18, -13, "Leclerc", color='#000000', fontsize=20, fontweight='bold')
plt.title("Formula 1 - 2021 Season\nHead to Head - Verstappen vs Leclerc", color='#000000', 
          fontsize=22, fontweight='bold')
plt.xlabel('RACES', fontsize=16, color='#000000', fontweight='bold')
plt.xticks(range(0,len(tracks)), tracks, fontsize=14, color='#000000', rotation=80)
plt.ylabel('POINTS GAP', fontsize=16, color='#000000', fontweight='bold')
plt.yticks(fontsize=16, color='#000000')
plt.show()


teamPts = raceResults.groupby('Team')['Points'].sum()
sprintQualiTeamPts = sprintQualiResults.groupby('Team')['Points'].sum()
teamPts = (teamPts+sprintQualiTeamPts).sort_values(ascending=False).reset_index()
teamPts.index = [i for i in range(1,11)]
teamPts

sprintQualiDriver = sprintQualiResults.groupby(['Driver', 'Team'])['Points'].sum().sort_values(ascending=False)
sprintQualiDriver = sprintQualiDriver[sprintQualiDriver > 0].reset_index()
sprintQualiDriver.index +=1
surnames = [driver.split()[1] for driver in sprintQualiDriver['Driver']]
plt.figure(figsize=(14,6))
plt.axis([0,7.2,4.7,-0.7])
plt.barh(surnames, sprintQualiDriver['Points'], color=c)
for i in range(1,len(sprintQualiDriver)+1):
    plt.text(sprintQualiDriver['Points'][i]-0.2, i-0.88, sprintQualiDriver['Points'][i], fontsize=24, color='k')
plt.title("Formula 1 - 2021 Season\nPoints Earned by Drivers in Sprint Qualifying", 
          fontsize=22, fontweight='bold', color='#bbbbbb')
plt.xlabel('POINTS', fontsize=16, color='#ffff55', fontweight='bold')
plt.xticks(fontsize=14, color='#ffff55')
plt.ylabel('DRIVERS', fontsize=16, color='#ffff55', fontweight='bold')
plt.yticks(fontsize=15, color='#ffff55')
plt.show()

raceWinners = raceResults[raceResults['Position'] == '1'].set_index('Track').drop('Position', axis=1)

raceWinnersCnt = raceWinners['Driver'].value_counts()
c = assign_color("drivers", raceWinnersCnt.index)
surnames = [driver.split()[1] for driver in raceWinnersCnt.index]
plt.figure(figsize=(14,6))
plt.axis([0,10.2,5.65,-0.65])
plt.barh(surnames, raceWinnersCnt.values, color=c)
for i in range(len(raceWinnersCnt)):
    plt.text(raceWinnersCnt.values[i]-0.5, i+0.15, "{:3}".format(raceWinnersCnt.values[i]), fontsize=24, color='k')
plt.title("Formula 1 - 2021 Season\nDrivers' Race Win Counts", fontsize=22, fontweight='bold', color='#00008B')
plt.xlabel('RACE WINS', fontsize=16, color='#00008B', fontweight='bold')
plt.xticks(fontsize=14, color='#00008B')
plt.ylabel('DRIVERS', fontsize=16, color='#00008B', fontweight='bold')
plt.yticks(fontsize=15, color='#00008B')
plt.show()

podiumFinish = raceResults[raceResults['Position'].isin(['1','2','3'])].set_index('Track').drop('Position', axis=1)
podiumCnt = podiumFinish['Driver'].value_counts()
c = assign_color("drivers", podiumCnt.index)
plt.figure(figsize=(14,7))
plt.axis([0,18.2,12.65,-0.65])
plt.barh([driver.split()[1] for driver in podiumCnt.index], podiumCnt.values, color=c)
for i in range(len(podiumCnt)):
    plt.text(podiumCnt.values[i]-0.6, i+0.25, "{:2}".format(podiumCnt.values[i]), fontsize=18, color='w')
plt.title("Formula 1 - 2021 Season\nDrivers' Podium Counts", fontsize=22, fontweight='bold', color='#000000')
plt.xlabel('PODIUMS', fontsize=16, color='#FFFF00', fontweight='bold')
plt.xticks(range(0,20,3), fontsize=14, color='#000000')
plt.ylabel('DRIVERS', fontsize=16, color='#FFFF00', fontweight='bold')
plt.yticks(fontsize=15, color='#000000')
plt.show()

topTen = [str(i) for i in range(1,11)]
topTenFinish = raceResults[raceResults['Position'].isin(topTen)]

topTenFinishCnt = topTenFinish['Driver'].value_counts()
c = assign_color("drivers", topTenFinishCnt.index)
plt.figure(figsize=(14,7.5))
plt.axis([0,20.5,17.65,-0.65])
plt.barh([driver.split()[1] for driver in topTenFinishCnt.index], topTenFinishCnt.values, color=c)
for i in range(len(topTenFinishCnt)):
    plt.text(topTenFinishCnt.values[i]-0.57, i+0.26, "{:2}".format(topTenFinishCnt.values[i]), fontsize=16, color='k')
plt.title("Formula 1 - 2021 Season\nDrivers' Top 10 Finish Counts", fontsize=22, fontweight='bold', color='#191970')
plt.xlabel('TOP 10 FINISHES', fontsize=16, color='#0343DF', fontweight='bold')
plt.xticks(range(0,20,3), fontsize=14, color='#228B22')
plt.ylabel('DRIVERS', fontsize=16, color='# #FFFFFF', fontweight='bold')
plt.yticks(fontsize=13, color='#000000')
plt.show()


teamPts = raceResults.groupby('Team')['Points'].sum()
sprintQualiTeamPts = sprintQualiResults.groupby('Team')['Points'].sum()
teamPts = (teamPts+sprintQualiTeamPts).sort_values(ascending=False).reset_index()
teamPts.index = [i for i in range(1,11)]
teamPts