import random
import threading
import os
from time import sleep
import socket
from multiprocessing.dummy import Pool
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

pool = Pool(10)

print("Lancement du programme...")

LISTEN_PORT = int(os.environ.get('LISTEN_PORT', '5005'))

OTHER_ADDRESSES = os.environ.get('OTHER_ADDRESSES', '127.0.0.1:5005') # comma separated addresses of other containers
SEND_BALL = os.environ.get('SEND_BALL', 'n').upper() in ['YES', 'Y', 'OUI', 'O']
INIT_BOUNCE_COUNT = int(os.environ.get('REBONDS', 5))

# Liste des joueurs
joueurs = OTHER_ADDRESSES.split(',')
for i in range(len(joueurs)):
    joueurs[i] = f"{socket.gethostbyname_ex(joueurs[i].split(':')[0])[2][0]}:{joueurs[i].split(':')[1]}"

# Variables globales
global score
score = 0

# Fonction pour envoyer une balle
def envoie_balle(adresse_adversaire, nb_rebonds):
    try:
        print(f"[ENVOI] Balle envoyée à {adresse_adversaire} avec {nb_rebonds} rebonds restants.")
        pool.apply_async(requests.get, [f'http://{adresse_adversaire}/{nb_rebonds}'])
    except Exception as e:
        print(f"[ERREUR] Problème lors de l'envoi de la balle : {e}")

# Fonction pour traiter une balle reçue
def traitement(nb_rebonds):
    print("paquet http recu")
    global score

    print(f"[REÇU] Balle reçue avec {nb_rebonds} rebonds restants.")
    if nb_rebonds > 0:
        nb_rebonds -= 1
        score += 1
        print(f"[SCORE] Nouveau score : {score}")

        prochain_joueur = random.choice(joueurs)
        print(f"[DEBUG] Prochain joueur sélectionné : {prochain_joueur}")
        envoie_balle(prochain_joueur, nb_rebonds)
    else:
        print("[FIN] La balle a atteint 0 rebonds. Aucun envoi supplémentaire.")

class BalleHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        self.wfile.write(bytes("<html><head><title>Bounce HTTP</title></head><body>", "utf-8"))
        self.wfile.write(bytes(f"<p>Score : {score}</p>", "utf-8"))
        if self.path.strip('/').isdigit():
            self.wfile.write(bytes(f"<p>There is {self.path.strip('/')} bounces left.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        
        try:
            traitement(int(self.path.strip('/')))
        except ValueError:
            pass


def ecoute_balle():
    with HTTPServer(('0.0.0.0', LISTEN_PORT), BalleHTTPHandler) as httpd:
        print("serving at port", LISTEN_PORT)
        httpd.serve_forever()

# Fonction pour démarrer l'envoi initial
def start():
    print("Lancement de la balle dans 2s...")
    sleep(2)
    print("Lancement de la balle...")
    envoie_balle(joueurs[0], INIT_BOUNCE_COUNT)

# Lancement du programme
if SEND_BALL:
    th = threading.Thread(target=start)
    th.start()
ecoute_balle()
