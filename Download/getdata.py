'''
Created on 27 Mar 2010

@author: Mike Thomas
'''

from BeautifulSoup import BeautifulSoup
import re
from urllib import urlopen

soup = BeautifulSoup(open("testdata/meetings.html"))
raceFinder = re.compile("/horses2/cards/card.sd\?race_id=(\d+)")
racesDone = set()
for link in soup.findAll("a", href = raceFinder):
    raceId = raceFinder.search(link["href"]).group(1)
    if raceId in racesDone: continue
    racesDone.add(raceId)
    address = "http://www.racingpost.com%s" % link["href"]
    urlHandle = urlopen(address)
    print raceId
    doc = urlHandle.read()
    urlHandle.close()
    handle = open("testdata/race_%s.html" % raceId, "w")
    handle.write(doc)
    handle.close()

