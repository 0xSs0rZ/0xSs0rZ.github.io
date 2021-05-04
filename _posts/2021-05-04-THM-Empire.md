---
layout: post
title: TryHackMe: Empire
subtitle: Empire Post Exploitation Framework
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
tags: [THM, Windows, C2, Empire, Powershell Empire, StarKiller, Eternalblue, Mimikatz]
---

![Empire-1.png](/img/Empire-1.png)

**Empire est un serveur C2, Command and Control, créé par BC-Security. Il permet de déployer des agents sur des machines et d'exécuter des modules à distance. Empire est une alternative open-source à Cobalt Strike.**

Afin d'acquérir des fondamentaux sur ce C2 incontournable, TryHackMe à créé une [room dédiée à Empire](https://tryhackme.com/room/rppsempire){:target="_blank"}. Voici un résumé des fonctions essentielle de Empire.

- **Installation de Empire**

1. `cd /opt`
2. `git clone https://github.com/BC-SECURITY/Empire/`
3. `cd /opt/Empire`
4. `./setup/install.sh`

- **Installation de StartKiller**

StartKiller fournit une interface graphique pour Empire.

1. `cd /opt`
2. Télécharger StartKiller: [https://github.com/BC-SECURITY/Starkiller/releases](https://github.com/BC-SECURITY/Starkiller/releases){:target="_blank"}
3. `chmod +x starkiller-0.0.0.AppImage`

- **Lancer Empire**

1. `cd /opt/Empire`
2. `./empire --rest`

![Empire-2.png](/img/Empire-2.png)

- **Lancer StarKiller**

1. `cd /opt`
2. `./starkiller-0.0.0.AppImage`
3. Se loguer: uri: `127.0.0.1:1337` ; default credentials: `empireadmin::password123`

![Empire-3.png](/img/Empire-3.png)

- **Éléments du menu**

**Listeners:** permet de créer et de lister les listeners disponibles.
**Stagers:** permet de créer et de lister les stagers. Un stager est l'équivalent d'un payload. Il permet le déploiement d'un agent.
**Agents:** permet de lister et d'interagir avec les agents. Un agent permet de lancer des commandes et des modules.
**Modules:** permet de lister les modules et de chercher un module. Un module est un outil spécifique ou un exploit qui peut être utilisé par un agent
**Credentials:** permet de sauvegarder les identifiants trouvés
**Reporting:** permet de voir les commandes qui ont été envoyés dans le passé

- **Demo**

Pour tester Empire, nous allons attaquer la box Blue également disponible sur THM. Blue est une machine Windows vulnérable à Eternalblue 

Utilisons Metasploit pour compromettre cette box

`use exploit/windows/smb/ms17_010_eternalblue`

![Empire-4.png](/img/Empire-4.png)

Exploit:

![Empire-5.png](/img/Empire-5.png)

Parfait :) On pourra uploader notre stager

- **Création d'un listener**

La création d'un listener est intuitive. Pas besoin de s'étendre. Ici on crée un listener http en écoute sur le port 31337.

![Empire-6.png](/img/Empire-6.png)

![Empire-7.png](/img/Empire-7.png)

- **Création d'un stager**

Ici nous allons créer un stager `windows/launcher_bat` qui utilise le listener que nous venons de créer.

![Empire-8.png](/img/Empire-8.png)

![Empire-9.png](/img/Empire-9.png)

On peut désormais télécharger le launcher puis le transférer sur la victime. 

![Empire-10.png](/img/Empire-10.png)

Lancer le stager:

![Empire-11.png](/img/Empire-11.png)

On obtient notre premier agent dans StarKiller :)

![Empire-12.png](/img/Empire-12.png)

On peut désormais interagir avec l'agent. Ex: `whoami`

![Empire-13.png](/img/Empire-13.png)

Résultat:

![Empire-14.png](/img/Empire-14.png)

On peut également utiliser des modules. Parmis les modules on retrouve des outils forts utiles tels que Seatbelt, Mimikatz, WinPEASS, etc.

Par exemple, récupération de hash avec Mimikatz: `powershell/credentials/mimikatz/sam` 

![Empire-15.png](/img/Empire-15.png)

Résultat:

![Empire-15.png](/img/Empire-16.png)

![Empire-15.png](/img/Empire-17.png)


Et voilà, c'est fini pour cette room de THM :) 


**Poursuivez avec :** 

- [SSH Port Forwarding - Cheat Sheet](https://0xss0rz.github.io/2020-11-21-SSH-Tunneling/)

- [Attack Detection Fundamentals - Initial Access Lab 3](https://0xss0rz.github.io/2021-01-06-Attack-Detection-Initial-Access-3/)

- [Hack The Box - Remote](https://0xss0rz.github.io/2020-08-23-HTB-Remote/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
