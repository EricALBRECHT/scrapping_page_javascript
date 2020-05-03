# import HTMLSession from requests_html
#http://theautomatic.net/2019/01/19/scraping-data-from-javascript-webpage-python/
#https://www.codeur.com/projects/241729-scrapping-de-pages-en-python
from requests_html import HTMLSession
from bs4 import BeautifulSoup

# create an HTML Session object
session = HTMLSession()
 
# Use the object above to connect to needed webpage
resp = session.get("https://transparencyreport.google.com/safe-browsing/search?url=etoro.com%2Fmarkets%2Fbtc&hl=fr")
 
# Run JavaScript code on webpage
resp.html.render()

#option_tags = resp.html.find("span")
 
#dates = [tag.text for tag in option_tags]

#print(dates)

soup = BeautifulSoup(resp.html.html, "lxml")
 
option_tags = soup.find_all('span', attrs={'class': ''} )
#option_tags = soup.find_all('div', attrs={'class': 'value'}) 

dates = [tag.text for tag in option_tags]

print(dates[0])

#i = 0

#for date in dates:
#    print(i,date)
#    i += 1  
    
#print(soup)
