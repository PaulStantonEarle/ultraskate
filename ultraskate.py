import re
import urllib
import matplotlib.pyplot as plt

def getstats(url):
    
    skaterurl = urllib.request.urlopen(url)
    skaterhtml = str(skaterurl.read())

    times = re.findall(r"\d\d:\d\d:\d\d",skaterhtml)
    laps = re.findall(r"Lap (\d+)",skaterhtml)
    acctimes = times[0::3]
    
    time = []
    distance = []
    for idx, acctime in enumerate(acctimes):
        hh,mm,ss = acctime.split(':')
        time.append(float(hh) + float(mm)/60 + float(ss)/3600)
        distance.append(float(laps[idx])*1.46)
    
    finalDistance = float(re.findall(r'<b>(\d+\.\d+)</b>',skaterhtml)[0])    
    averageLap = re.findall(r'<b>(\d+\:\d+:?\d+?)</b>',skaterhtml)[2]
    mm,ss = averageLap.split(':')
    finalTime = (float(mm)/60 + float(ss)/3600)*finalDistance/1.46    
    print(finalDistance)
    print(finalTime)   
    time.append(finalTime)
    distance.append(finalDistance)
    
    distance.insert(0,0)
    time.insert(0,0)
    return [time, distance]

# main

skaters = {}

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
skaters['1 Joe'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141134'
skaters['2 Angel'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141102'
skaters['3 Mathieu'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141108'
skaters['4 Adrian'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141142'
skaters['5 Calleigh'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141131' 


#skaters['Calligh'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141131'
#skaters['Alyssa'] = 'http://jms.racetecresults.com/MyResults.aspx?uid=16370-352-1-141139'


fig, ax1 = plt.subplots(1,1)
for key in sorted(skaters.keys()):
    [time, distance] = getstats(skaters[key])
    pace = distance[-1]/time[-1]
    projected = pace * 24
    print(key)
    print('Pace: ' + "%.2f" % pace)
    print('Total miles: ' + "%.2f" % distance[-1])
    print('Projected miles: ' + "%.2f" % projected + "\n" )
    ax1.plot(time,distance,'-',label=key + '  ' + "%.1f" % distance[-1] +'mi')


ax1.legend()
ax1.set_title('Ultra Skaters')
ax1.set_xlabel('time [hours]')
ax1.set_ylabel('distance [miles]')
ax1.set_xlim([0,24])
#ax1.set_ylim([0,310])
ax1.grid()
plt.show()
