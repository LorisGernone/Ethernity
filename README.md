# Ethernity

Chat en réseau en Python. Un serveur reçoit les messages et les renvoie à tous les clients connectés, qui discutent dans une fenêtre Tkinter.

TP final Python au CFA Insta, à partir du code de base du formateur :
https://gitlab.com/f.cardenas14/tp_python_clientserver_chat

## Équipe

- [LorisGernone](https://github.com/LorisGernone) : `client.py` + interface Tkinter
- [kirian-devops](https://github.com/kirian-devops) : `server.py`
- [rlutinier-lgtm](https://github.com/rlutinier-lgtm) : `clientthread.py` + commentaires

## Fichiers

- `server.py` : lance le serveur, accepte les clients, renvoie les messages à tout le monde
- `clientthread.py` : gère chaque client connecté dans un thread séparé (pseudo, commandes, déconnexion)
- `client.py` : la fenêtre de chat, connexion puis envoi/réception des messages

## Lancer le chat

1. `python server.py` — demande un port (Entrée = 5555) et un nom (Entrée = Ethernity)
2. `python client.py`
3. Pseudo, clic sur Se connecter, puis Envoyer

Le client se connecte à `chat-srv.ecole.homelab` sur le port 5555 (VPN de l'école nécessaire).

## Commandes du serveur

- `USERNAME <pseudo>` : envoyée automatiquement à la connexion, annonce l'arrivée à tout le monde
- `NAME` : le serveur répond son nom
- `QUIT` : déconnecte le client, annonce son départ

## Ce qu'on a corrigé et ajouté

Côté client : pseudo vide refusé, message d'erreur si le serveur est éteint ou injoignable au lieu d'un plantage, QUIT bien reconnu par le serveur, le client s'arrête si le serveur coupe, interface Tkinter.

Côté serveur : port et nom demandés au lancement, redemande un port si celui choisi est déjà pris, commande NAME, les clients déconnectés sont retirés de la liste au lieu de faire planter le serveur, import `socket` corrigé dans `clientthread.py`, arrêt propre au Ctrl+C.

## Technologies

Python 3, socket, threading, tkinter.

