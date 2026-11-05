# Ethernity 💬

Ethernity est un chat en réseau écrit en Python. Un serveur reçoit les messages et les renvoie à tous les clients connectés, qui discutent ensemble dans une fenêtre Tkinter.

Projet réalisé dans le cadre du TP final Python au CFA Insta, à partir du code de base fourni par le formateur :
https://gitlab.com/f.cardenas14/tp_python_clientserver_chat

## 👥 L'équipe

| Membre | Rôle |
|---|---|
| [LorisGernone](https://github.com/LorisGernone) | Client (`client.py`) + interface Tkinter |
| [kirian-devops](https://github.com/kirian-devops) | Serveur (`server.py`) |
| [rlutinier-lgtm](https://github.com/rlutinier-lgtm) | Gestion des clients côté serveur (`clientthread.py`) + commentaires |

## 📁 Les fichiers

| Fichier | À quoi il sert |
|---|---|
| `server.py` | Lance le serveur, accepte les clients et renvoie les messages à tout le monde |
| `clientthread.py` | Gère chaque client connecté, dans un thread séparé : pseudo, commandes, déconnexion |
| `client.py` | La fenêtre de chat : on se connecte avec un pseudo, puis on envoie et on reçoit les messages |

## ▶️ Lancer le chat

1. Lancer le serveur :
   `python server.py`
   Il demande un port (Entrée = 5555) et un nom (Entrée = Ethernity).
2. Lancer le client :
   `python client.py`
3. Écrire son pseudo, cliquer sur **Se connecter**, puis discuter avec **Envoyer**.

Le client se connecte au serveur `chat-srv.ecole.homelab` sur le port 5555 (VPN de l'école nécessaire).

## 📡 Les commandes du serveur

| Commande | Effet |
|---|---|
| `USERNAME <pseudo>` | Envoyée automatiquement à la connexion. Le serveur annonce l'arrivée du pseudo à tout le monde |
| `NAME` | Le serveur répond avec son nom (Ethernity par défaut) |
| `QUIT` | Déconnecte le client, et le serveur annonce son départ |

## 🛠️ Ce qu'on a amélioré

**Côté client**
- Un pseudo vide est refusé
- Message d'erreur si le serveur est éteint ou introuvable, au lieu d'un plantage
- La commande QUIT est bien reconnue par le serveur (le pseudo n'est plus ajouté devant)
- Le client s'arrête si le serveur est coupé
- Interface graphique Tkinter : pseudo, zone de messages, champ de saisie, bouton Envoyer

**Côté serveur**
- Choix du port et du nom du serveur au lancement
- Un autre port est demandé si celui choisi est déjà utilisé, au lieu de planter
- Nouvelle commande `NAME` qui renvoie le nom du serveur
- Les clients déconnectés sont retirés de la liste au lieu de bloquer le serveur
- Correction de l'import de `socket` dans `clientthread.py`, pour que les déconnexions soient bien détectées
- Arrêt propre du serveur avec Ctrl + C

## 🧰 Technologies

- Python 3
- socket (réseau)
- threading (recevoir les messages en continu)
- tkinter (interface graphique)

