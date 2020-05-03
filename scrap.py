# import HTMLSession from requests_html
#http://theautomatic.net/2019/01/19/scraping-data-from-javascript-webpage-python/
#https://www.codeur.com/projects/241729-scrapping-de-pages-en-python

# coding: utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

# Etat des resultats, 0 si aucune anomalie, 1 si au moins un resultat est incorecte => declanche l'envoi d'un mail

def connection(urls):
    status = 0 #initialisation de la variable defaut, 0 = pas de defaut
    # listing des URL testées avec le resultat
    list_url =[]
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
        if results[0] != "Aucun contenu suspect détectéX":
            status = 1 # Texte different
        content = {"status" : status, "listUrl" : list_url}
    return content 

def mail(content):
    list_url = content['listUrl']
    if content['status'] == 1:
        
        
        message =""
        for list in list_url:
            print(list)
            message += list + '\n'
        msg = MIMEMultipart()
        msg['From'] = 'eric.albrecht80@gmail.com'
        msg['To'] = 'cda80@live.fr'
        msg['Subject'] = 'Alert site incorrect' 
        message = "ee"
        msg.attach(MIMEText(message))
        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
       
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login('eric.albrecht80', 'chaton2405811234')
        #server.sendmail(fromaddr, toaddrs, msg)
        mailserver.sendmail('eric.albrecht80@gmail.com', 'cda80@live.fr', msg.as_string())
        mailserver.quit()

            
#content = connection(urls)
#mail(content)


def test():
    
    server = smtplib.SMTP() # Avec TLS, on utilise SMTP()
    # server.set_debuglevel(1) # Décommenter pour activer le debug
    server.connect('smtp.free.fr',25) # On indique le port TLS
    # (220, 'toto ESMTP Postfix') # Réponse du serveur
    #server.ehlo() # On utilise la commande EHLO
    # (250, 'toto\nPIPELINING\nSIZE 10240000\nVRFY\nETRN\nSTARTTLS\nENHANCEDSTATUSCODES\n8BITMIME\nDSN') # Réponse du serveur
    #server.starttls() # On appelle la fonction STARTTLS
    # (220, '2.0.0 Ready to start TLS') # Réponse du serveur
    server.login('hub2you@free.fr', 'hub2you@')
    # (235, '2.7.0 Authentication successful') # Réponse du serveur
    fromaddr = 'TOTO <moi@toto.fr>'
    toaddrs = ['cda80@live.fr','e.albrecht@laposte.net'] # On peut mettre autant d'adresses que l'on souhaite
    sujet = "Un Mail avec Python"
    message = u"""\
    Velit morbi ultrices magna integer.
    Metus netus nascetur amet cum viverra ve cum.
    Curae fusce condimentum interdum felis sit risus.
    Proin class condimentum praesent hendrer
    it donec odio facilisi sit.
    Etiam massa tempus scelerisque curae habitasse vestibulum arcu metus iaculis hac.
    """
    msg = """\
    From: %s\r\n\
    To: %s\r\n\
    Subject: %s\r\n\
    \r\n\
    %s
    """ % (fromaddr, ", ".join(toaddrs), sujet, message)
    try:
        server.sendmail(fromaddr, toaddrs, msg)
        print ('ok')
    except smtplib.SMTPException as e:
        print(e)
        print('erreur')
    # {} # Réponse du serveur
    server.quit()
    # (221, '2.0.0 Bye')
test()