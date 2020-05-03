# import HTMLSession from requests_html
#http://theautomatic.net/2019/01/19/scraping-data-from-javascript-webpage-python/
#https://www.codeur.com/projects/241729-scrapping-de-pages-en-python
from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Création un objet Session HTML
session = HTMLSession()
# List des URL à tester
urls=[
 "https://transparencyreport.google.com/safe-browsing/search?url=etoro.com%2Fmarkets%2Fbtc&hl=fr",
 "https://transparencyreport.google.com/safe-browsing/search?url=sncf.fr&hl=fr",
 "https://transparencyreport.google.com/safe-browsing/search?url=fdj.fr&hl=fr"    
]
# listing des URL testées avec le resultat
list_url =[]
# Etat des resultats, 0 si aucune anomalie, 1 si au moins un resultat est incorecte => declanche l'envoi d'un mail

def connection(urls):
    status = 0 #initialisation de la variable defaut, 0 = pas de defaut
    for url in urls:
        # Utilisation de l'objet pour se connecter à la page Web requise
        resp = session.get(url)

        # Execution du code JavaScript sur la page Web
        resp.html.render()
        # Recuperation du code HTML généré
        soup = BeautifulSoup(resp.html.html, "lxml")
        # Recherche de la balise ciblée
        option_tags = soup.find_all('span', attrs={'class': ''} ) 
        results = [tag.text for tag in option_tags]
        #mise en forme du resultat : URL + etat
        result = "%s \\ %s " % (url, results[0])
        list_url.append(result)
        # Verification que l'url retournent un texte différent de “Aucun contenu suspect détecté”
        if results[0] != "Aucun contenu suspect détecté":
            status = 1 # Texte different
        content = {"status" : status, "list url" : list_url}
    return content 

def mail(content):
    if content['status'] == 1:
        for list in content['list_url']:
            print(list)

content = connection(urls)
mail(content)


