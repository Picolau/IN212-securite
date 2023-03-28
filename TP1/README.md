# TP1 - Recherche d’Informations en Source Ouverte
Leonardo Picoli - 27/03/2023

## Introduction
Utilisation de nmap

## 1 Scan actifs

### 1.1 Scans nmap: Application sur un serveur présent sur Internet

**Q 1.1.1: À partir de l’outil nmap et des options -n -sn, déterminez si l’hôte d’adresse IP 164.132.172.108 est fonctionnel ou non :**  
  
En éxécutant le code `nmap -n -sn 164.132.172.108 ` on a le résultat suivant: 
```
Starting Nmap 7.93 ( https://nmap.org ) at 2023-03-27 07:43 EDT
Nmap scan report for 164.132.172.108
Host is up (0.017s latency).
Nmap done: 1 IP address (1 host up) scanned in 0.18 seconds
```
On peut constater que l'hôte est fonctionnel.

**Q 1.1.2: Quelles sont les options passées à l’outil ? À quoi servent-elles?**  
**Q 1.1.3: Quelle technique utilise nmap pour détecter un hôte?**

D'après `man nmap`, on voit que:

Nmap uses raw IP packets in novel ways to determine what hosts are available on the network, what services (application name and version) those hosts are offering, what operating systems (and OS versions) they are running, what type of packet filters/firewalls are in use, and dozens of other characteristics.

En plus, les descriptions des options se retrouvent ci-dessous:

- **sn (No port scan)**
This option tells Nmap not to do a port scan after host
discovery, and only print out the available hosts that responded
to the host discovery probes. This is often known as a “ping
scan”, but you can also request that traceroute and NSE host
scripts be run. This is by default one step more intrusive than
the list scan, and can often be used for the same purposes. It
allows light reconnaissance of a target network without
attracting much attention. It can easily be used to count available machines on a network or monitor server availability. The default host discovery done with -sn consists of an ICMP
echo request, TCP SYN to port 443, TCP ACK to port 80, and an
ICMP timestamp request by default. When executed by an
unprivileged user, only SYN packets are sent (using a connect
call) to ports 80 and 443 on the target. When a privileged user
tries to scan targets on a local ethernet network, ARP requests
are used unless --send-ip was specified.

- **n (No DNS resolution)**  
Tells Nmap to never do reverse DNS resolution on the active IP addresses it finds. Since DNS can be slow even with Nmap's built-in parallel stub resolver, this option can slash scanning times.

**Q 1.1.4 - Par rapport à ce qui a été vu en cours, avec des serveurs directement accessibles sur le réseau local, quelle différence observez-vous au niveau de la technique de détection utilisée ?**  

Le scan actif avec Nmap consiste à envoyer des paquets de test à un hôte cible pour déterminer s'il est actif sur le réseau. Dans le cas de serveurs directement accessibles sur le réseau local, la technique de détection utilisée par Nmap serait généralement le "ping scan", qui envoie des paquets ICMP echo request (ping) à l'hôte cible pour vérifier sa disponibilité.

Cependant, le "ping scan" peut être bloqué par des pare-feu ou des routeurs configurés pour ne pas répondre aux requêtes ICMP. Dans ce cas, Nmap peut utiliser d'autres techniques de détection, telles que la balayage TCP SYN, qui envoie des paquets SYN à un port spécifique pour déterminer si l'hôte cible est actif.

En résumé, la technique de détection utilisée par Nmap pour un scan actif dépendra des configurations des hôtes et des pare-feu sur le réseau local, mais le "ping scan" est souvent la méthode de base utilisée pour les hôtes directement accessibles sur le réseau local.

### 1.2 Scan nmap : découverte des services sur le système ciblé!

**Q 1.2.1 - Détecter les ports ouverts/fermés/filtrés sur le système d’adresse IP 164.132.172.108 !**

Pour les ports TCP : `nmap -n -sS -PN 164.132.172.108` 

```
Starting Nmap 7.93 ( https://nmap.org ) at 2023-03-27 08:42 EDT
Nmap scan report for 164.132.172.108
Host is up (0.019s latency).
Not shown: 993 filtered tcp ports (no-response)
PORT     STATE SERVICE
25/tcp   open  smtp
80/tcp   open  http
443/tcp  open  https
465/tcp  open  smtps
587/tcp  open  submission
4343/tcp open  unicall
8008/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 4.34 seconds
```

Pour les ports UDP : `nmap -n -sU -PN 164.132.172.108`  

```
Starting Nmap 7.93 ( https://nmap.org ) at 2023-03-27 07:51 EDT
Nmap scan report for 164.132.172.108
Host is up (0.016s latency).
Not shown: 995 filtered udp ports (port-unreach)
PORT      STATE         SERVICE
67/udp    open|filtered dhcps
68/udp    open|filtered dhcpc
520/udp   open|filtered route
4500/udp  open|filtered nat-t-ike
27444/udp open|filtered Trinoo_Bcast

Nmap done: 1 IP address (1 host up) scanned in 1101.74 seconds
```

**Q 1.2.2 - À partir de captures wireshark, quelle différence pouvez-vous noter entre ces deux protocoles ?**

Exemple TCP Wireshark:

| Source | Dest | Protocol | Info |
| ---    | ---- | ---      |  --  |
| 10.0.2.15 | 164.132.172.108 |	TCP	| 56803 → 34573 **[SYN]** Seq=0 Win=1024 Len=0 MSS=1460 |
| 164.132.172.108 | 10.0.2.15 | TCP	| 80 → 56801 **[SYN, ACK]** Seq=0 Ack=1 Win=65535 Len=0 MSS=1460 |
| 10.0.2.15 | 164.132.172.108 | TCP	| 56801 → 80 **[RST]** Seq=1 Win=0 Len=0 |
| 164.132.172.108 | 10.0.2.15 | TCP | 9876 → 56801 **[RST, ACK]** Seq=1 Ack=1 Win=0 Len=0 |

Exemple UDP Wireshark: 

| Source | Dest | Protocol | Info |
| ---    | ---- | ---      |  --  |
10.0.2.15 |164.132.172.108 | UDP | 61238 → 33717 Len=40
10.0.2.15 |164.132.172.108 | UDP | 61238 → 2865 Len=0
10.0.2.2 | 10.0.2.15 | ICMP | 70 Destination unreachable (Port unreachable) |

**Q 1.2.3 - Quelle différence y a-t-il entre UDP et TCP pour découvrir un service présent sur une cible ? Qu’est-ce que cela implique lors de la découverte des services des cibles présentes?**

UDP (User Datagram Protocol) et TCP (Transmission Control Protocol) sont deux protocoles de communication utilisés pour transférer des données sur un réseau informatique.

La principale différence entre UDP et TCP est la manière dont ils gèrent la transmission des données. TCP est un protocole orienté connexion, ce qui signifie qu'il établit une connexion entre les deux extrémités avant de transférer les données. Il utilise un système de contrôle de flux et de retransmission pour s'assurer que toutes les données sont correctement reçues.

D'un autre côté, UDP est un protocole sans connexion qui ne nécessite pas d'établir une connexion avant de transférer les données. Il ne fournit pas de mécanisme de contrôle de flux et de retransmission, ce qui signifie que les données peuvent être perdues ou reçues dans un ordre différent de celui dans lequel elles ont été envoyées.

Lorsqu'on utilise nmap pour découvrir un service présent sur une cible, on peut utiliser des scans de ports TCP et/ou UDP. Les scans de ports TCP sont généralement plus fiables car TCP assure une transmission fiable des données, ce qui permet de garantir que les informations de service sont correctement reçues.

Les scans de ports UDP peuvent être moins fiables car UDP ne garantit pas la réception fiable des données. Cependant, les scans de ports UDP peuvent être utiles pour découvrir des services qui ne répondent pas aux scans de ports TCP ou pour identifier des services qui ne sont disponibles que sur des ports UDP spécifiques.

**Q 1.2.4 - Doit-on scanner l’ensemble des ports TCP/UDP (0→65535) ?**

Scanner l'ensemble des ports TCP/UDP (0→65535) peut être utile dans certaines circonstances, mais cela peut également être très long et consommer beaucoup de ressources.

Si vous avez besoin de découvrir tous les services disponibles sur une cible, il peut être judicieux de scanner l'ensemble des ports TCP/UDP. Cela peut être particulièrement utile si vous ne savez pas quels ports sont utilisés par les services que vous souhaitez découvrir.

Cependant, si vous avez une idée des services que vous souhaitez découvrir, vous pouvez limiter le scan aux ports couramment utilisés par ces services. Cela peut réduire considérablement le temps de scan et la quantité de données à analyser.

**Q 1.2.5 - Quelle stratégie peut-on mettre en place pour gagner en efficacité?**

Par exemple:
1. Scanner uniquement les ports pertinents.  
Par exemple, pour un serveur web, limiter le scan aux ports 80 (HTTP) et 443 (HTTPS);
2. Utiliser des options de scan spécifiques. Par exemple utiliser l'option -n pour ne pas faire le DNS reverse, ce qui optimise le scan.
3. Utiliser la parallélisation; 

**Q 1.2.6 - À quel compromis ?**

Le compromis le plus évident est celui entre le **temps de scan et la précision des résultats**. En général, plus on scanne un grand nombre de ports, plus cela prendra de temps, mais on obtient des résultats plus précis. À l'inverse, si on limite le scan à un nombre restreint de ports, cela prendra moins de temps, mais on risque de manquer certains services qui seraient présent sur d'autres ports.

Un autre compromis concerne la **quantité de ressources utilisées**. Si on utilise des options de scan plus avancées, cela peut consommer plus de ressources, notamment en termes de bande passante et de puissance de traitement. Cela peut entraîner des problèmes de performance pour la cible, d'autant plus que certains environnements de réseau peuvent détecter et bloquer les scans de port agressifs.

Enfin, il y a également un compromis entre la **discrétion et la visibilité**. Si on utilise des techniques de scan avancées ou des scripts NSE, cela peut être plus efficace pour découvrir les services et les vulnérabilités, mais cela peut également augmenter les risques de détection et d'alerte par les systèmes de sécurité de la cible.

**Q 1.2.7 - Quelle option fournissez-vous donc à nmap?**

Exemple `nmap -PN -n -sS --top-ports 100 164.132.172.108` 

### 1.3 Scan nmap : identifier les services accessibles

**Q 1.3.1 - Identifiez les services accessibles fonctionnant sur les ports découverts précédemment! Est-il possible de connaitre les versions de ces services?**

Après avoir éxécuté: `nmap -sV -p 25,80,443,465,587,4343,8008 164.132.172.108`
On le résultat suivant, avec les respectifs versions :
``` 
Starting Nmap 7.93 ( https://nmap.org ) at 2023-03-27 15:30 EDT
Nmap scan report for ns3304136.ip-164-132-172.eu (164.132.172.108)
Host is up (0.031s latency).

PORT     STATE SERVICE  VERSION
25/tcp   open  smtp     Postfix smtpd
80/tcp   open  http     Apache httpd 2.4.54 ((Debian))
443/tcp  open  ssl/http Apache httpd 2.4.54 ((Debian))
465/tcp  open  ssl/smtp Postfix smtpd
587/tcp  open  smtp     Postfix smtpd
4343/tcp open  ssh      OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
8008/tcp open  http
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8008-TCP:V=7.93%I=7%D=3/27%Time=6421EECE%P=x86_64-pc-linux-gnu%r(Ge
SF:tRequest,D3,"HTTP/1\.1\...
Service Info: Host:  mail.pelicanux.net; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

**Q 1.3.2 - Certains de ces services / systèmes sont-ils vulnérables ?**
* Scripts NSE (nmap scripting engine)    
  * --script “not intrusive”
  * --script “default and safe"
  * --script “(default or safe) and http-*”

* Les scripts sont accessibles dans les répertoires de nmap où ils peuvent être analysés 
  * Par exemple : ls /usr/share/nmap/scripts/http-*

## 2 Récupération d’informations publiques

### 2.1 Informations de premier niveau

**Q 2.1.1 - Récupérez l’adresse IP des sites :**
* **http://ensta.fr,**
* **https://cours.pelicanux.net.**

Pour faire ça, il suffit de taper le code suivant:  
`dig ensta.fr +short` >> 217.182.194.63  
`dig pelicanux.net +short` >> 164.132.172.108  

**Q 2.1.2 - À quoi sert l’outil whois? Quelles informations permet-il de récupérer?**  
**Q 2.1.3 - À partir de cet outil, déterminez :**
* **Les contacts administratifs**
* **Le réseau dans lequel l’IP du site est située**

Si on tape `whois 217.182.194.63` pour l'hôte ensta.fr par exemple, on a le résultat suinant avec les informations démandés dans les questions:

```
% This is the RIPE Database query service.
% The objects are in RPSL format.
%
% The RIPE Database is subject to Terms and Conditions.
% See http://www.ripe.net/db/support/db-terms-conditions.pdf

% Note: this output has been filtered.
%       To receive output for a database update, use the "-B" flag.

% Information related to '164.132.160.0 - 164.132.175.255'

% Abuse contact for '164.132.160.0 - 164.132.175.255' is 'abuse@ovh.net'

inetnum:        164.132.160.0 - 164.132.175.255
netname:        SD-RBX6
country:        FR
org:            ORG-OS3-RIPE
admin-c:        OTC2-RIPE
tech-c:         OTC2-RIPE
status:         LEGACY
mnt-by:         OVH-MNT
created:        2018-12-05T08:41:14Z
last-modified:  2018-12-05T08:41:14Z
source:         RIPE

organisation:   ORG-OS3-RIPE
org-name:       OVH SAS
country:        FR
org-type:       LIR
address:        2 rue Kellermann
address:        59100
address:        Roubaix
address:        FRANCE
phone:          +33972101007
admin-c:        OTC2-RIPE
admin-c:        OK217-RIPE
admin-c:        GM84-RIPE
abuse-c:        AR15333-RIPE
mnt-ref:        OVH-MNT
mnt-ref:        RIPE-NCC-HM-MNT
mnt-by:         RIPE-NCC-HM-MNT
mnt-by:         OVH-MNT
created:        2004-04-17T11:23:17Z
last-modified:  2020-12-16T10:24:51Z
source:         RIPE # Filtered

role:           OVH Technical Contact
address:        OVH SAS
address:        2 rue Kellermann
address:        59100 Roubaix
address:        France
admin-c:        OK217-RIPE
tech-c:         GM84-RIPE
tech-c:         SL10162-RIPE
nic-hdl:        OTC2-RIPE
abuse-mailbox:  abuse@ovh.net
mnt-by:         OVH-MNT
created:        2004-01-28T17:42:29Z
last-modified:  2014-09-05T10:47:15Z
source:         RIPE # Filtered

% Information related to '164.132.0.0/16AS16276'

route:          164.132.0.0/16
descr:          OVH
origin:         AS16276
mnt-by:         OVH-MNT
created:        2015-12-09T09:54:51Z
last-modified:  2015-12-09T09:58:12Z
source:         RIPE

% This query was served by the RIPE Database Query Service version 1.106 (SHETLAND)

```

Par le résultat on peut voir que la commande `whois` donne pleine d'informations sur l'hôte IP.

D'après la réference [RFC 3912](https://www.rfc-editor.org/rfc/rfc3912)  
WHOIS is a TCP-based transaction-oriented query/response protocol
that is widely used to provide information services to Internet
users.  While originally used to provide "white pages" services and
information about registered domain names, current deployments cover
a much broader range of information services.  The protocol delivers
its content in a human-readable format.

A WHOIS server listens on TCP port 43 for requests from WHOIS
clients.  The WHOIS client makes a text request to the WHOIS server,
then the WHOIS server replies with text content.  All requests are
terminated with ASCII CR and then ASCII LF.  The response might
contain more than one line of text, so the presence of ASCII CR or
ASCII LF characters does not indicate the end of the response.  The
WHOIS server closes its connection as soon as the output is finished.
The closed TCP connection is the indication to the client that the
response has been received.

**Q 2.1.4 - À quoi sert l’outil dig?**

D'après `man dig`: 

**dig**  is  a flexible tool for interrogating DNS name servers. It performs DNS lookups and displays the answers that are returned from the name server(s) that were queried. Most DNS administrators use dig to troubleshoot DNS problems because of its flexibility, ease of use, and clarity of output. Other lookup tools tend to have less functionality than dig.

**Q 2.1.5 - À partir de cet outil, pour chacun de ces domaines, déterminez :**
* **Les serveurs DNS permettant la résolution domaine ↔ IP,**
* **Les serveurs de mails permettant de recevoir les courriels.**

Pour **pelicanux.net**: 

`dig NS pelicanux.net`:  
pelicanux.net.          168616  IN      NS      vps806360.ovh.net.  
pelicanux.net.          168616  IN      NS      ks3269125.kimsufi.com.  

`dig MX pelicanux.net`:  
pelicanux.net.          1000    IN      MX      10 mail.pelicanux.net.  

Pour **ensta.fr**: 

`dig NS ensta.fr`:  
ensta.fr.               7200    IN      NS      ensta.ensta.fr.  
ensta.fr.               7200    IN      NS      ladi1.ensta.fr.  
ensta.fr.               7200    IN      NS      ladi2.ensta.fr.

`dig MX ensta.fr`:  
ensta.fr.               7200    IN      MX      10 mailhost.ensta.fr. 

### 2.2 Shodan!

**Q 2.2.1 - Rendez-vous sur le site https://shodan.io. À partir des résultats précédents, déterminez les versions et les services utilisés sur les adresses obtenues!**

Pour l'addresse **pelicanux.net** [164.132.172.108](https://www.shodan.io/host/164.132.172.108) on trouve les services et les versions suivants:

|Port/Protocol|Service|Version|
| -- | -- | -- |
| 25 / TCP | ESMTP Postfix (Debian/GNU) | - |
| 80 / TCP | Apache httpd | 2.4.54 |
| 443 / TCP | Apache httpd | 2.4.54 |
| 465 / TCP | ESMTP Postfix (Debian/GNU) | - |
| 587 / TCP | ESMTP Postfix (Debian/GNU) | - |


Pour l'addresse **ensta.fr** [217.182.194.63](https://www.shodan.io/host/217.182.194.63) on trouve les services et les versions suivants:

|Port/Protocol|Service|Version|
| -- | -- | -- |
| 22 / TCP | OpenSSH | 7.9p1 Debian 10+deb10u2 |
| 80 / TCP | Apache httpd | - |
| 443 / TCP | Apache httpd | - |
| 123 / UDP | NIP | 3 |

**Q 2.2.2 - Concernant l’adresse 164.132.172.108, retrouvez-vous les résultats obtenus de manière active? Quelle(s) différence(s) avez-vous pu noter?**

On peut constater que on a bien trouvé les mêmes résultats par rapport à ce qu'on a fait en utilisant les commands `nmap`!

La seule différence que j'ai noté c'est que en utilisant `nmap` on a trouvé un port de plus, que c'est la porte 8008, avec la message: "_1 service unrecognized despite returning data_"

### 2.3 Google dorks !

Pour plus d'info, visiter [Google dorks]()

**Q 2.3.1 - Rechercher les fichiers présents sur le site de votre école :**
* **de type PDF**
* **de type Word (doc, docx, xls, xlsx)**
* **de type text**
* **de type php**

Il suffit de taper les commandes suivants:

* `filetype:pdf ensta-paris.fr`
* `filetype:doc ensta-paris.fr` (+ docx, xls, xlsx)
* `filetype:txt ensta-paris.fr`
* `filetype:php ensta-paris.fr`

**Q 2.3.2 - De nouveaux liens peuvent-ils être intéressants dans le cadre d’un test d’intrusion?**

De nouveaux liens peuvent bien être utils dans le cadre d'un test d'intrusion lorsqu'ils permettent de trouver les données qui ne sont pas généralement affichés dans le cadre d'une recherche commune. Grâce à des options de recherche bien choisies, nous pouvons accéder à des données sensibles qui ont fini par être exposées sur l'internet.

**Q 2.3.2 - Ces requêtes permettent-elles de découvrir des informations sensibles (fichiers de sauvegarde, fichiers contenant des mots de passe)?**

Oui, il existe de nombreuses options et sites web que nous pouvons visiter et qui donnent des idées sur les options de "Google Dorking" que nous pouvons faire pour trouver des données sensibles.

