import socket
import threading 
import re 
import time

class ClientListener(threading.Thread):

    # Enregistre un nouveau client avec ses information de connection
    def __init__(self, server, socket, address):
        super(ClientListener, self).__init__()
        self.server= server
        self.socket= socket
        self.address= address
        self.listening= True
        self.username= "No username"

# Recoit les messages du client tant qu'il est connecté et gère les erreurs de reception
    def run(self):
        while self.listening:
            data= ""
            
            try:
                # On recoit les messages du client
                data = self.socket.recv(1024).decode('UTF-8')
          
            except OSError:
                # Si une erreur ce produit
                print("Unable to receive data")
                self.quit()
                break

            # On traite le message reçu
            self.handle_msg(data)
            time.sleep(0.1)
        print("Ending client thread for", self.address)
 
 
    def quit(self):
        # Si le client est deja deconnecté on ne fait rien
        if not self.listening:
            return
        self.listening = False      # On indique que le client est déconnecté
        self.socket.close()         # On ferme la connection
        self.server.remove_socket(self.socket)              # On retire le client du server
      
        #Pas d'annonce si le client n'avait pas de pseudo (ex : recherche de serveurs)
        if self.username != "No username":
            self.server.echo("{0} has quit\n".format(self.username))

    # Analyse les messages reçus et gère les informations du client
    def handle_msg(self, data):
        print(self.address, "sent :", data)
        username_result = re.search('^USERNAME (.*)$', data)
        if username_result:
            self.username = username_result.group(1)
            self.server.echo("{0} has joined.\n".format(self.username))
        elif data == "NAME":
            #On répond seulement au client qui a demandé le nom
            self.socket.sendall(self.server.name.encode("UTF-8"))
        elif data == "QUIT":
            self.quit()
        elif data == "":
            self.quit()
        else:
            self.server.echo(data)
