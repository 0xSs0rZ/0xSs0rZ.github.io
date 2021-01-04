---
layout: post
title: Attack Detection Fundamentals - Initial Access Lab 2
subtitle: Workshop de F-Secure - Utilisation de Koadic C2
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [Koadic, C2, Mshta, post-exploitation, Windows, Sysmon, HTA, Defense Evasion, Red Team, Blue Team, MITRE ATT&CK]
---

![Logo](/img/Koadic.png){: .center-block :}

Nous poursuivons la première partie *Initial Access* du workshop *Attack Detection Fundamentals* de F-Secure.

Dans le [lab 1](https://0xss0rz.github.io/2021-01-04-Attack-Detection-Initial-Access-1/){:target="_blank"}, nous avons vu que nous pouvons échapper à la détection en spoofant le PPID. Il est également possible de lancer l'exécution via des objects COM. Se sera le but du deuxième lab [1].

Pour cela, nous utiliserons un nouvel outil: Koadic

**Koadic**, *or COM Command & Control, is a Windows post-exploitation rootkit similar to other penetration testing tools such as Meterpreter and Powershell Empire. The major difference is that Koadic does most of its operations using Windows Script Host (a.k.a. JScript/VBScript)*[2]

**Pourquoi Koadic ?**

*'security teams are looking for unusual PS activity in the Windows event logs. (cf Lab 1) They are not as focused (yet) on scripts run by the Windows Script Host engine.'* [3]

**Lab:** On garde le même [setup que pour le lab1](https://0xss0rz.github.io/2021-01-04-Attack-Detection-Initial-Access-1/){:target="_blank"} soit une VM Win 7 et une VM Ubuntu

**Installation de Koadic**

```
git clone https://github.com/zerosum0x0/koadic.git
cd koadic
pip3 install -r requirements.txt
./koadic
```
![d4547d155eef4e704c88a6d2c72e683e.png](/img/837467001b6b4b4c8b556b59f8270a99.png)

**Config du listener**

Par défaut, utilisation de Mshta [4] [5] [6]

![4bca67342e63b0db6f55c675c9a5a6a5.png](/img/c20fa72c3679455cbe34bcb303309e7f.png)

Le fonctionnement est similaire à celui de Metasploit

![28929fc2a09675a6b51e286a9b463865.png](/img/6d2cdc6070bf43779990c3286bfac4d3.png)

Execution

1. Extraire le payload

![761df604a4e89c65896fc7d9c9efd49d.png](/img/2abae881c33840f9800914481656f5a7.png)

2. Transférer le paylaod sur la machine windows et exécuter

Pour le transfert j'utilise un serveur http 

![b92061363da64f623749dcbc30fe0ad3.png](/img/2d1f7da2dec94acf88e1f1f6181eaa44.png)

Exécuter le fichier sur la machine windows. 

Résultat:

![dfffe516d347115449821762fca8ad2f.png](/img/9534828bff674927a14d4e0ecee0db58.png)


![c8bd7f7cd28ae5a49155a878b763e2e8.png](/img/8beafc40d5fd4782b5201f3a4885009a.png)

# Analyse

1. Event id 1 - Process create: 

mshta:


![4d4dcd85c49b4a6b5ac993c432ff7b84.png](/img/a2c5335ffc9c4f4487a911383aea4e64.png)

Rundll32

![1671f3346afbc6901df3545576346bcf.png](/img/150d1aa8c3c243efb2e0b8dd0675aded.png)

2. Event id 3 - Network connection

On trouve des connections en lien avec mshta et rundll32

![ba2ad3778de08444aa21cab58d205db5.png](/img/3b8ff3d972e1443ab6aa6d9ef4ece99c.png)

![6fb939a58eea64fcc22bf4c7c6a1769a.png](/img/8e1eee92f76d4c41ab9a82109716cb68.png)

# Conclusion

Nous venons d'analyser une anomalie couramment générée par des outils offensifs à savoir la création d'une connection à internet par un binaire. Ce type de connection peut être un indicateur de compromission

[1] F-Secure, *Attack Detection Fundamentals: Initial Access - Lab #2*, [https://labs.f-secure.com/blog/attack-detection-fundamentals-initial-access-lab-2/](https://labs.f-secure.com/blog/attack-detection-fundamentals-initial-access-lab-2/)

[2] Zerosum0x0, *Koadic*, [https://github.com/zerosum0x0/koadic](https://github.com/zerosum0x0/koadic)

[3] Varonis, *Koadic: LoL Malware Meets Python-Based Command and Control (C2) Server, Part I*, [https://www.varonis.com/blog/koadic-lol-malware-meets-python-based-command-and-control-c2-server-part-i/](https://www.varonis.com/blog/koadic-lol-malware-meets-python-based-command-and-control-c2-server-part-i/)

[4] MITRE ATT&CK, *Koadic*, [https://attack.mitre.org/software/S0250/](https://attack.mitre.org/software/S0250/)

[5] MITRE ATT&CK, *Mshta*, [https://attack.mitre.org/techniques/T1218/005/](https://attack.mitre.org/techniques/T1218/005/)

[6] MITRE ATT&CK, *Defense Evasion*, [https://attack.mitre.org/tactics/TA0005/](https://attack.mitre.org/tactics/TA0005/)

**Poursuivez avec :** 

- [SSH Port Forwarding - Cheat Sheet](https://0xss0rz.github.io/2020-11-21-SSH-Tunneling/)

- [Hack The Box - Cache](https://0xss0rz.github.io/2020-11-18-HTB-Cache/)

- [Hack The Box - Remote](https://0xss0rz.github.io/2020-08-23-HTB-Remote/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
