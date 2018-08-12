#imports
import re
from urllib.request import urlopen #py 3
#import urllib

from bs4 import BeautifulSoup
import json
import schedule
import time
import datetime

def save_html(time, html):
    with open(time + '.html', 'wb') as outfile:
        outfile.write(html.read())
        print('html saved')

#create list of repositories where each repository is a dictionary
def scrape():
    html = urlopen("https://github.com/trending")
    soup = BeautifulSoup(html, 'html.parser')

    # currentday
    now = datetime.datetime.now()
    # day = now.strftime("%Y-%m-%d")
    time = now.strftime("%Y-%m-%d-%H:%M:%S")

    #get repos
    repos = soup.findAll("li", {"class": "col-12"})
    
    trending_repos = []
    for r in range(len(repos)):

        trend = {}
        trend['name'] = repos[r].a.get('href')[1:]
        trend['rank'] = r+1
        try:
            trend['desc'] = repos[r].p.get_text().strip()
        except:
            trend['desc'] = ''
        try:
            trend['lang'] = repos[r].find(itemprop="programmingLanguage").get_text().strip()
        except:
            trend['lang'] = ''
        try:
            trend['stars'] = int(repos[r].findAll("a", {"class": "muted-link"})[0].get_text().strip().replace(',', ''))
        except:
            save_html(time, html)
            trend['stars'] = 0
        try:
            trend['forks'] = int(repos[r].findAll("a", {"class": "muted-link"})[1].get_text().strip().replace(',',''))
        except:
            save_html(time, html)
            trend['forks'] = 0

        trend['stars_today'] = int(repos[r].find("span", {"class": "d-inline-block float-sm-right"}).get_text().strip().split()[0].replace(',',''))
        contributors = repos[r].find("a", {"class": "no-underline"}).findAll("a", {"class": "d-inline-block"})
        contributor_list = []
        for c in range(len(contributors)):
            contributor = {}
            contributor['user-id'] = contributors[c].get('data-hovercard-user-id')
            contributor['username'] = contributors[c].get('href')[1:]
            contributor_list.append(contributor)
        trend['contributors'] = contributor_list

        trending_repos.append(trend)
        print('Done repository' + str(r))

    d = {}
    d["repos"] = trending_repos
    
    with open(time+'.txt', 'w') as outfile:
        json.dump(d, outfile)
        print('recorded')
#run code everyday
#schedule.every().day.at("13:35").do(scrape)
schedule.every(5).minutes.do(scrape)
while True:
    schedule.run_pending()
    time.sleep(1)
#scrape()