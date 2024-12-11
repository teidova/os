from scapy.all import IP, UDP, Raw, send, sniff, conf
import random
import threading
from time import sleep

# Obtenir l'interface
interface = conf.route.route('127.0.0.1')[0]

# Liste des joueurs
joueurs = ["127.0.0.1:" + input('port other:')]
mon_adresse = "127.0.0.1"
mon_port = int(input('mon port:'))
mon_adresse_et_port = f"{mon_adresse}:{mon_port}"
joueurs.append(mon_adresse_et_port)
envoie_balles = input("envoie balle(y/n):")

# Variables globales
global score
score = 0
processed_packets = set()
lock = threading.Lock()

# Fonction pour envoyer une balle
def envoie_balle(adresse_adversaire, nb_rebonds):
    try:
        print(f"[DEBUG] Préparation de l'envoi à {adresse_adversaire} avec {nb_rebonds} rebonds.")
        ball = IP(src=mon_adresse, dst=adresse_adversaire.split(':')[0]) / \
               UDP(sport=random.randint(1024, 65535), dport=int(adresse_adversaire.split(':')[1])) / \
               Raw(load=f"nb_rebonds:{nb_rebonds}")
        send(ball, verbose=False)
        print(f"[ENVOI] Balle envoyée à {adresse_adversaire} avec {nb_rebonds} rebonds restants.")
    except Exception as e:
        print(f"[ERREUR] Problème lors de l'envoi de la balle : {e}")

# Fonction pour traiter une balle reçue
def traitement(balle):
    global score
    try:
        with lock:
            # Identifier le paquet de manière unique
            packet_id = (balle[IP].src, balle[IP].dst, balle[Raw].load.decode())
            if packet_id in processed_packets:
                print("[DEBUG] Paquet déjà traité.")
                return
            processed_packets.add(packet_id)

            # Traiter le paquet
            if Raw in balle:
                payload = balle[Raw].load.decode()
                if "nb_rebonds" in payload:
                    nb_rebonds = int(payload.split(":")[1])
                    print(f"[REÇU] Balle reçue avec {nb_rebonds} rebonds restants.")

                    if nb_rebonds > 0:
                        nb_rebonds -= 1
                        score += 1
                        print(f"[SCORE] Nouveau score : {score}")

                        # Sélectionner le prochain joueur
                        dernier_joueur = balle[IP].src + ":" + str(balle[UDP].sport)
                        prochain_joueur = random.choice(
                            [p for p in joueurs if p != mon_adresse_et_port and p != dernier_joueur]
                        )
                        print(f"[DEBUG] Prochain joueur sélectionné : {prochain_joueur}")
                        envoie_balle(prochain_joueur, nb_rebonds)
                    else:
                        print("[FIN] La balle a atteint 0 rebonds. Aucun envoi supplémentaire.")
    except Exception as e:
        print(f"[ERREUR] Problème dans le traitement de la balle : {e}")

# Fonction pour écouter les paquets
def ecoute_balle():
    print("[ATTENTE] En écoute pour recevoir une balle sur le port", mon_port)
    sniff(iface=interface, filter=f"udp and dst port {mon_port}", prn=traitement)

# Fonction pour démarrer l'envoi initial
def start():
    sleep(2)
    envoie_balle(joueurs[0], 5)

# Lancement du programme
if envoie_balles == "y":
    th = threading.Thread(target=start)
    th.start()
ecoute_balle()


