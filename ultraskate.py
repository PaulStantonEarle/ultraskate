# -*- coding: utf-8 -*-
"""
This program web scrapes the results from the 2019 Mami Ultra
and make some plots.

http://jms.racetecresults.com/results.aspx?CId=16370&RId=352

"""

import re
import urllib
import pickle
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup



def getstats(skaters):
    
    for skater in skaters:        
        skaterurl = urllib.request.urlopen(skater['url'])
        skaterhtml = str(skaterurl.read())
    
        times = re.findall(r"\d\d:\d\d:\d\d",skaterhtml)
        laps = re.findall(r"Lap (\d+)",skaterhtml)
# check for slowest lap > 10 hours because it will mess up my kludge
        hh,mm,ss = times[0].split(':')
        if(float(hh) >10):
            tmp = times.pop(0)
            print(tmp)
        acctimes = times[0::3]
        splitTimes = times[1::3]
        
        time = []
        distance = []
        for idx, acctime in enumerate(acctimes):
            hh,mm,ss = acctime.split(':')
            time.append(float(hh) + float(mm)/60 + float(ss)/3600)   
            distance.append(float(laps[idx])*1.46)
    
        split = []
        lap = []        
        for idx, splitTime in enumerate(splitTimes):
            hh,mm,ss = splitTime.split(':')
            split.append(float(hh)*60 + float(mm) + float(ss)/60)
            lap.append(laps[idx])
        
        finalDistance = float(re.findall(r'<b>(\d+\.\d+)</b>',skaterhtml)[0])    
        averageLap = re.findall(r'<b>(\d+\:\d+:?\d+?)</b>',skaterhtml)[2]
        avglap = averageLap.split(':')
        ss = avglap[-1]
        mm = avglap[-2]
        if len(avglap) == 2:
            finalTime = (float(mm)/60 + float(ss)/3600)*finalDistance/1.46
        else:
            finalTime = (float(avglap[0]) + float(mm)/60 + float(ss)/3600)*finalDistance/1.46
        
        print(skater['name'])
        print(finalDistance)
        print(finalTime,"\n")   
        time.append(finalTime)
        distance.append(finalDistance)
        
        distance.insert(0,0)
        time.insert(0,0)
        skater['distances'] = distance
        skater['times'] = time
        skater['laps'] = lap
        skater['splits'] = split
    
    return

def getskaters():
    
    skaters = []
    
# I manually downloaded the pages to local disk because I could not access the 
# second page automatically     
    for file in ["racers1.html","racers2.html"]:
        soup = BeautifulSoup(open(file),features="html.parser")
      
        for link in soup.find_all('a'):     
            href = str(link.get('href'))
            if href.find("MyResults") > -1:
                skater = {}
                skater['url'] = 'http://jms.racetecresults.com/'+str(link.get('href'))
                skater['name'] = str(link.getText())     
                skaters.append(skater)

    return skaters



def pltTimeVsDist(skaters):
    fig, ax1 = plt.subplots(1,1)
    for skater in skaters:
        distance = skater['distances']
        time = skater['times']
        pace = distance[-1]/time[-1]
        projected = pace * 24
        print(skater['name'])
        print('Pace: ' + "%.2f" % pace)
        print('Total miles: ' + "%.2f" % distance[-1])
        print('Total time: ' + "%.2f" % time[-1]+"\n")
    
        label = skater['name'] + '  ' + "%.1f" % distance[-1] +'mi'
        ax1.plot(time,distance,'k-',alpha=0.1,label=label)
        ax1.plot(time[-1],distance[-1],'r.',markersize=3)
#        ax1.text(time[-1]+0.2,distance[-1],skater['name'])
    
    
    #ax1.legend()
    ax1.set_title('Ultra Skaters')
    ax1.set_xlabel('time [hours]')
    ax1.set_ylabel('distance [miles]')
    ax1.set_xlim([0,24])
    #ax1.set_ylim([0,310])
    ax1.grid(alpha = 0.2)
    plt.show()


def pltDistHist(skaters):
    # histograms of distances
    fig2, ax2 = plt.subplots(1,1)
    totdists = [ skater['distances'][-1] for skater in skaters]
    ax2.hist(totdists,bins=range(0,311,10))
    ax2.set_title('Total Distance (10 mile bins)')
    ax2.set_xlabel('number of skaters')
    ax2.set_ylabel('distance [miles]')
    plt.show()
    
def pltLapHist(skater):
    fig, ax1 = plt.subplots(1,1)
    ax1.hist(skater['splits'], bins = 30, range = (0,30))
    ax1.set_title(skater['name'])
    plt.show()

    
# main

# load skater data
try:
    pkl_file = open('skaters.pkl', 'rb')
    skaters = pickle.load(pkl_file)
    pkl_file.close() 
except IOError: 
    print('Skater lap data not found. Downloading data from web')
    skaters = getskaters()
    getstats(skaters)
    output = open('skaters.pkl', 'wb')
    pickle.dump(skaters, output)
    output.close()


pltTimeVsDist(skaters)

pltDistHist(skaters)

for skater in skaters:
    pltLapHist(skater)






# colorado 
#skaters['1 Joe'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141134'
#skaters['4 Peter'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141123'
#skaters['3 Rick'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141153'
#skaters['2 Spencer'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141152'
 
# 50+
#skaters['Rick'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141153'
#skaters['Ian'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141161'
#skaters['Barry'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141159'
#skaters['Phillip'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141150'
#skaters['Raymond'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141154'
#skaters['Anne'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141143'

# top 5
#skaters['1 Joe'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141134'
#skaters['2 Angel'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141102'
#skaters['3 Mathieu'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141108'
#skaters['4 Adrian'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141142'
#skaters['5 Calleigh'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141131' 

