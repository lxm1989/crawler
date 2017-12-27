from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

#InternalLinks
def getInternalLinks(bsObj,includeUrl):
    #includeUrl=urlparse(includeUrl).scheme + "://" + urlparse(includeUrl).netloc
    internalLinks = []
    #for link in bsObj.findAll("a",href=re.compile("^(/|.*"+includeUrl+")")):
    for link in bsObj.findAll("a", href=re.compile("^(/)")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs["href"])
    return internalLinks

#ExternalLinks
def getExternalLinks(bsObj,excludeUrl):
    externalLinks = []
    for link in bsObj.findAll("a",href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace("http://","").split("/")
    return addressParts

def getRandomexternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html,"html.parser")
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    if len(externalLinks) == 0:
        print("No external links.")
        domain = urlparse(startingPage).scheme + "://" + urlparse(startingPage).netloc
        internalLinks = getInternalLinks(bsObj,domain)
        if len(internalLinks) == 0:
            print("No internal links.")
            return None
        else:
            return getRandomexternalLink(internalLinks[random.randint(0,len(internalLinks)-1)])
    else:
        a=externalLinks[random.randint(0,len(externalLinks)-1)]
        #print(a)
        return a

def followExternalOnly(startingSite):
    externalLink = getRandomexternalLink(startingSite)
    if externalLink:
        print("Random external link is:" + externalLink)
        followExternalOnly(externalLink)
    else:
        print("Over.")
        return


followExternalOnly("http://oreilly.com")
#getRandomexternalLink("http://twitter.com/oreillymedia")