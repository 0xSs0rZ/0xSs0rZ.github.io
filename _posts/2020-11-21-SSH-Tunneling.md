---
layout: post
title: SSH Port forwarding - Cheat sheet
subtitle: Tunnel SSH ou SSH Port forwarding - Cheat sheet
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [SSH, Tunneling, Tunnel SSH, Port forwarding, Bypass, Firewall, Redirection de ports, Cheat sheet, Chisel, Plink]
comments: false
---

![Logo](/img/SSH_logo.png){: .center-block :}

**De plus en plus de chall de [CTF](https://0xss0rz.github.io/tags/#CTF) ou de box sur [HTB](https://0xss0rz.github.io/tags/#HTB) nécessitent d'effectuer du port forwarding (ou si vous préférez de créer un tunnel SSH). Vu que je n'y comprenais pas grand chose au début, j'ai un peu creusé le sujet histoire de m'endormir moins bête :)** 

Je vous propose de découvrir dans cet article un condensé des infos pertinentes sur les tunnels SSH, à savoir les concepts et les commandes essentielles pour effectuer du SSH port forwarding.

## Port forwarding, késako?

Le tunneling SSH ou SSH port forwarding est une méthode permettant de créer une connexion SSH chiffrée entre un client et un serveur par lequel les ports peuvent être relayés.

La redirection SSH est utile pour transporter des données de services qui utilisent un protocole non chiffré, comme VNC ou FTP, pour accéder à des contenus géo-limités, ou pour contourner des pare-feux intermédiaires. Les tunnels SSH sont également utilisés pour installer des backdoors dans des réseaux internes.

![Illustration](/img/SSH_1.png){: .center-block :}

En principe, nous pouvons transférer n'importe quel port TCP et faire transiter le trafic par une connexion SSH sécurisée.

Il existe trois types de redirection de port SSH :

1. Redirection de port local. - Transfère une connexion de l'hôte client vers l'hôte du serveur SSH, puis vers le port hôte de destination.
2. Redirection de port à distance. - Transfère un port de l'hôte serveur à l'hôte client et ensuite au port de l'hôte de destination.
3. Redirection dynamique de port. - Crée un serveur proxy SOCKS qui permet la communication sur une série de ports.
 
Nous nous intéresserons ici aux deux premiers types de redirection: **Local port forwarding** et **Remote port forwarding**.
 
Pour effectuer ces types de redirection de port, nous pouvons utiliser plusieurs outils dont **OpenSSH** (machine Linux), **plink.exe** (machine Windows) et **Chisel** (multi OS). Il est aussi possible d'utiliser PuTTY à la place de plink en environnement Windows (voir par exemple l'article de LinuxSize en référence)

![OpenSSH](/img/SSH_2.gif){: .center-block :}
 
Plink.exe est téléchargeable ici: [https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
 
{: .box-warning}
Utiliser la bonne version (32 ou 64 bits) de plink en fonction du type de machine. Pour obtenir l'architecture: `C:\>wmic os get osarchitecture` ou `systeminfo`
 
![plink](/img/SSH_3.png){: .center-block :}
 
Chisel est disponible ici: [https://github.com/jpillora/chisel](https://github.com/jpillora/chisel)
 
{: .box-note}
'Chisel is a fast TCP tunnel, transported over HTTP, secured via SSH. Single executable including both client and server. Written in Go (golang). Chisel is mainly useful for passing through firewalls, though it can also be used to provide a secure endpoint into your network. Chisel is very similar to crowbar though achieves much higher performance.'
 
Installation de Chisel:
1. `git clone https://github.com/jpillora/chisel.git`
2. Dans le répertoire de chisel: `go build`
 
Avant d'entrer dans le vif du sujet, soulignons qu'un autre outil est intéressant pour faire du port forwarding. Il s'agit de **Ngrock**. Découvrez comment utiliser Ngrock [ici](https://0xss0rz.github.io/2020-06-20-Ngrock-usage/)
    
## 1 - Local port forwarding

La redirection de port local vous permet de transférer un port de la machine locale (client ssh) vers un port de la machine distante (serveur ssh), qui est ensuite transféré vers un port de la machine de destination.

Dans ce type de redirection, le client SSH écoute les connexions sur un port configuré, et lorsqu'il reçoit une connexion, il la tunnelise vers un serveur SSH. Le serveur se connecte à un port de destination configuré, éventuellement sur une autre machine que le serveur SSH.

![local port forward](/img/SSH_4.png){: .center-block :}

### Commandes:

**OpenSSH:**

-L     # Forwarder un port local vers un port distant sur une machine  distante

`ssh -L [LOCAL_IP:]LOCAL_PORT:DESTINATION:DESTINATION_PORT [USER@]SSH_SERVER`

Il est possible d'utiliser tout n'importe quel port supérieur à 1024 comme LOCAL_PORT. Les numéros de port inférieurs à 1024 sont des ports privilégiés et ne peuvent être utilisés que par l'utilisateur privilégié root. Si votre serveur SSH écoute sur un port autre que 22 (par défaut), utilisez l'option -p [PORT_NUMBER].

**plink:**

`C:\>plink32.exe -ssh -l USERNAME -pw MYPASSWORD -L [LOCAL_IP:]LOCAL_PORT:DESTINATION:DESTINATION_PORT SSH_SERVER`

ou 

`C:\>plink.exe -ssh USER@SSH_SERVER -L [LOCAL_IP:]LOCAL_PORT:DESTINATION:DESTINATION_PORT`

**Chisel:**

Sur la machine pivot:

`chisel server -p PORT --host SERVER_SSH -v`

Sur la machine d'attaque:

`chisel client -v SERVER_SSH:PORT [LOCAL_IP:]LOCAL_PORT:DESTINATION:DESTINATION_PORT`

## 2 - Remote port forwarding

La redirection de port à distance est l'opposé de la redirection de port local. Elle permet de transférer un port de la machine distante (serveur ssh) vers un port de la machine locale (client ssh), qui est ensuite transféré vers un port de la machine de destination.

Dans ce type de transfert, le serveur SSH écoute sur un port donné et tunnelise toute connexion à ce port vers le port spécifié sur le client SSH local, qui se connecte ensuite à un port sur la machine de destination. La machine de destination peut être la machine locale ou toute autre machine.

![remote port forward](/img/SSH_5.png){: .center-block :}

### Commandes: 

**OpenSSH:**

-R     # Forwarder un port distant vers un port local sur la machine locale

`ssh -R [REMOTE:]REMOTE_PORT:DESTINATION:DESTINATION_PORT [USER@]SSH_SERVER`

**plink:**

`C:\>plink32.exe -ssh -l USERNAME -pw MYPASSWORD -R [REMOTE]:REMOTE_PORT:DESTINATION:DESTINATION_PORT SSH_SERVER`

ou 

`C:\>plink.exe -ssh USER@SSH_SERVER -R [REMOTE:]REMOTE_PORT:DESTINATION:DESTINATION_PORT`

**Chisel:**

Sur la machine d'attaque:

`chisel server -p PORT [--host HOST_IP] --reverse -v`

Sur la machine pivot:

`chisel client -v HOST_IP:PORT R:[REMOTE:]REMOTE_PORT:DESTINATION:DESTINATION_PORT`

**Happy Hacking !**

**Références:**

1 - OpenSSH

[ - How to setup ssh tunneling - Linuxsize](https://linuxize.com/post/how-to-setup-ssh-tunneling/)

[ - OSCP - Understanding ssh tunnels - FalconSpy](https://falconspy.medium.com/oscp-understanding-ssh-tunnels-519e31c698bf)

[ - SSH Port forwarding examples](https://www.ssh.com/ssh/tunneling/example)

[ - SSH Tunneling](https://www.ssh.com/ssh/tunneling/)

[ - Comprendre la redirection de port (Port forwarding) - Linux France](http://www.linux-france.org/prj/edu/archinet/systeme/ch13s04.html)

2 - Plink

[ - Using the command-line connexion tool plink](https://the.earth.li/~sgtatham/putty/0.52/htmldoc/Chapter7.html)

[ - Tunneling sessions via plink - Booches.nl](https://www.booches.nl/2010/08/tunneling-sessions-via-plink/) 

[ - Setting up an ssh tunnel using plink](https://medium.com/@incubusattax/setting-up-an-ssh-tunnel-using-plink-7d8dacfd4014)

[ - Remote SSH tunneling with plink.exe](https://medium.com/@informationsecurity/remote-ssh-tunneling-with-plink-exe-7831072b3d7d)

3 - Chisel

[ - Tunneling with Chisel and SSF - 0xdf](https://0xdf.gitlab.io/2020/08/10/tunneling-with-chisel-and-ssf-update.html)

[ - Etat de l’art du pivoting réseau en 2019 - Orange CYberdefense](https://orangecyberdefense.com/fr/insights/blog/ethical_hacking/etat-de-lart-du-pivoting-reseau-en-2019/)

**Credit photos:**

[ - MRG-Effitas](https://www.mrg-effitas.com/research/bypass-hardware-firewalls-def-con-22/)

[ - SSH.com](https://www.ssh.com/ssh/tunneling/)

[ - FalconSpy](https://falconspy.medium.com/oscp-understanding-ssh-tunnels-519e31c698bf)

**Poursuivez avec :** 

[- Oneliner shell - Cheat sheet](https://0xss0rz.github.io/2020-05-10-Oneliner-shells/)

[- Over The Wire - Bandit 3 - SSH Part](https://0xss0rz.github.io/2020-05-16-OverTheWire-Bandit-3-SSH-Part/)

[- Redirection de port avec Ngrock](https://0xss0rz.github.io/2020-06-20-Ngrock-usage/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
