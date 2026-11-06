import threading
import socket
import time
import re
import tkinter as tk


class Client():
    #créer une connexion TCP vers server + port et envoie username
    def __init__(self, username, server, port):
        self.socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #Crée le socket réseau en TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
        self.socket.connect((server, port))
        self.username= username
        self.send("USERNAME {0}".format(username))
        self.listening= True


    def listener(self):
        #écoute en continu les messages du serveur
        while self.listening:
            data= ""
            try:
                data= self.socket.recv(1024).decode('UTF-8')  #recv() est bloquant tant qu'aucun message n'arrive
            except socket.error:
                print("Unable to receive data")
            #data vide ou "QUIT" fait appeler tidy_up() dans handle_msg, ce qui arrête la boucle
            self.handle_msg(data)
            time.sleep(0.1)  #faut faire une pause sur chaque boucle sinon CPU 100%


    def listen(self):
        #Lance listener() dans un thread séparé sinon fenêtre Tkinter = bloqué
        self.listen_thread = threading.Thread(target=self.listener)
        self.listen_thread.daemon = True  #le thread s'arrête avec le programme
        self.listen_thread.start()

    def send(self, message):
        #envoyer n'importe quel texte au serveur, mais en lui ajoutant le pseudo devant
        try:
            username_result = re.search('^USERNAME (.*)$', message)
            if not username_result and message != "QUIT":      # si ce n'est PAS un message USERNAME ET que ce n'est PAS QUIT", alors c'est que du texte
                message= "{0}: {1}".format(self.username, message)
            self.socket.sendall(message.encode("UTF-8"))
        except socket.error:
            print("unable to send message")

    def tidy_up(self):
        #Arrête proprement le client : stoppe la boucle d'écoute et ferme le socket
        self.listening = False
        self.socket.close()

    def handle_msg(self, data):
        if data=="QUIT":
            self.tidy_up()
        elif data=="":
            self.tidy_up()  #chaîne vide = connexion fermée côté serveur
        else:
            #Affiche le message reçu dans la zone de texte de la fenêtre
            zone_messages.insert(tk.END, data + "\n")

def connecter():
    #Appelée au clic sur "Se connecter" + préfère mettre les infos du srv et port en brut vue que pas d'autre srv
    global client
    username = champ_pseudo.get()
    server= "chat-srv.ecole.homelab"
    port_validation = False
    try:
        port= int(5555)
        port_validation = True
    except ValueError:
        zone_messages.insert(tk.END, "Le port doit être un nombre\n")

    if username == "":
        zone_messages.insert(tk.END, "il faut un pseudo valide\n")  #pseudo vide = refusé
    elif port_validation == True :
        try:        #essaie de se connecter au serveur. Si ca rate il renvoie un message au lieu de planter, else démarre l'écoute
            client= Client(username, server, port)
        except socket.error:
            zone_messages.insert(tk.END, "impossible d'accéder au serveur ! \n")
        else:
            client.listen()

def envoyer():
    #Appelée au clic sur "Envoyer"
    message = champ_message.get()
    client.send(message)
    champ_message.delete(0, tk.END)  #vide le champ pour le prochain message


#Construction de la fenêtre tkinter, widget par widget | et le .pack() empile les widgets les uns en dessous des autres
fenetre = tk.Tk()
fenetre.title("Ethernity")
tk.Label(fenetre, text="Pseudo : ").pack()
champ_pseudo = tk.Entry(fenetre)
champ_pseudo.pack()
tk.Button(fenetre, text="Se connecter", command=connecter).pack()  #pas de parenthèses : sinon s'exécute tout de suite
zone_messages = tk.Text(fenetre, height=15, width= 50)
zone_messages.pack()
champ_message = tk.Entry(fenetre, width=40)
champ_message.pack()
tk.Button(fenetre, text="Envoyer", command=envoyer).pack()
fenetre.mainloop()  #doit rester la dernière ligne : boucle bloquante qui écoute les événements
