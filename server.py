import socket
import sys #utilisé pour sortir du programme
import time
from clientthread import ClientListener

class Server():

    def __init__(self, port):
        self.listener= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Si le port est déjà pris, on redemande un autre port au user
        while True:
            try:
                self.listener.bind(('', port))
                break
            except OSError:
                print("Le port", port, "est déjà utilisé (ou le serveur vient d'être arrêté : attendre 1 minute)")
                port= ask_port()
        self.listener.listen(1)
        print("Listening on port", port)
        self.clients_sockets= []

    def run(self):
        while True:
            print("listening new customers")
            try:
                (client_socket, client_adress) = self.listener.accept()
            except socket.error:
                sys.exit("Cannot connect clients")
            self.clients_sockets.append(client_socket)
            print("Start the thread for client:", client_adress)
            client_thread= ClientListener(self, client_socket, client_adress)
            client_thread.start()
            time.sleep(0.1)

    def remove_socket(self, socket):
        #Le client a pu être déjà retiré par echo()
        if socket in self.clients_sockets:
            self.clients_sockets.remove(socket)

    def echo(self, data):
        print("echoing:", data)
        #On note les clients déconnectés pour les retirer après la boucle
        dead_sockets= []
        for sock in self.clients_sockets:
            try:
                sock.sendall(data.encode("UTF-8"))
            except OSError:
                print("Client déconnecté, il est retiré de la liste")
                dead_sockets.append(sock)
        for sock in dead_sockets:
            self.remove_socket(sock)


#Demande le port au user : vide = 5555, sinon un nombre entre 1 et 65535
def ask_port():
    while True:
        port_input= input("Port (Entrée = 5555 par défaut) : ")

        if port_input == "":
            return 5555

        try:
            port= int(port_input)
        except ValueError:
            print("Port invalide :", port_input, "- il faut un nombre")
            continue

        if 1 <= port <= 65535:
            return port
        print("Port invalide :", port, "- il doit être entre 1 et 65535")


if __name__ == "__main__":
    port= ask_port()
    server= Server(port)
    server.run()
