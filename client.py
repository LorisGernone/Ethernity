from tkinter import messagebox
import threading
import socket
import time
import re
import sys
import tkinter as tk





class Client():

    def __init__(self, username, server, port):
        self.socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, port))
        self.username= username
        self.send("USERNAME {0}".format(username))
        self.listening= True


    def listener(self):
        while self.listening:
            data= ""
            try:
                data= self.socket.recv(1024).decode('UTF-8')
            except socket.error:
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1)


    def listen(self):
        self.listen_thread = threading.Thread(target=self.listener)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def send(self, message):
        try:
            username_result = re.search('^USERNAME (.*)$', message)
            if not username_result and message != "QUIT":        #ajoute le pseudo devant les messages
                message= "{0}: {1}".format(self.username, message)
            self.socket.sendall(message.encode("UTF-8"))
        except socket.error:
            print("unable to send message")

    def tidy_up(self):
        self.listening = False
        self.socket.close()

    def handle_msg(self, data):
        if data=="QUIT":
            self.tidy_up()
        elif data=="":
            self.tidy_up()
        else:
            zone_messages.insert(tk.END, data + "\n")

def connecter():
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
        zone_messages.insert(tk.END, "il faut un pseudo valide\n")
    elif port_validation == True :
        try:                                                                  #essaie de se connecter au serveur. Si ca rate il renvoie un message au lieu de planter
            client= Client(username, server, port)
        except socket.error:
            zone_messages.insert(tk.END, "impossible d'accéder au serveur ! \n")
        else:
            client.listen()

def envoyer():
    message = champ_message.get()
    client.send(message)
    champ_message.delete(0, tk.END)


fenetre = tk.Tk()
fenetre.title("Ethernity")
tk.Label(fenetre, text="Pseudo : ").pack()
champ_pseudo = tk.Entry(fenetre)
champ_pseudo.pack()
tk.Button(fenetre, text="Se connecter", command=connecter).pack()
zone_messages = tk.Text(fenetre, height=15, width= 50)
zone_messages.pack()
champ_message = tk.Entry(fenetre, width=40)
champ_message.pack()
tk.Button(fenetre, text="Envoyer", command=envoyer).pack()
fenetre.mainloop()
