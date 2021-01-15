---
layout: post
title: Attack Detection Fundamentals - Discovery Lab 1
subtitle: Workshop de F-Secure - LDAP Reconnaissance
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
tags: [Covenant, C2, Rubeus, Kerberoast, AS-REP roast, SharpSploit, .NET, ETW, SilkETW, SilkService, Windows, Blue Team, Red Team, Active Directory, LDAP, HELK, LDAP Recon, PowerSploit, MITRE ATT&CK]
---

![bdc1ff29d8e4fdaff0c8f1e2691a839d.png](/img/07c6239b49ac4dada3e2d10ef617ea53.png)

Lors des labs précédents, nous avons étudié les étapes d'accès initial, d'exécution de code et de persistance du framework MITRE ATT&CK en imitant certains acteurs malveillants.

- [Attack Detection Fundamentals - Initial Access Lab 1](https://0xss0rz.github.io/2021-01-04-Attack-Detection-Initial-Access-1/){:target="_blank"}
- [Attack Detection Fundamentals - Initial Access Lab 2](https://0xss0rz.github.io/2021-01-04-Attack-Detection-Initial-Access-2/){:target="_blank"}
- [Attack Detection Fundamentals - Initial Access Lab 3](https://0xss0rz.github.io/2021-01-06-Attack-Detection-Initial-Access-3/){:target="_blank"}
- [Attack Detection Fundamentals - Code Execution](https://0xss0rz.github.io/2021-01-09-Attack-Detection-Code-Execution/){:target="_blank"}
- [Attack Detection Fundamentals - Persistence](https://0xss0rz.github.io/2021-01-10-Attack-Detection-Persistence/){:target="_blank"}

Nous allons désormais nous intéresser à la phase de reconnaissance, de "découverte", du framework MITRE ATT&CK [1]:

![1ec5cc74cbb2202e1d1c1a25a886ed5f.png](/img/99448452130043768bb337583555d532.png)

Dans ce premier lab de la série *Discovery and Lateral Movement* du workshop *Attack Detection Fondamentals* nous allons utiliser le framework Covenant et explorer des techniques permettant d'obtenir des crédentials. [2]

Covenant fait partie des [outils préférés des black hat](https://0xss0rz.github.io/2021-01-13-Outils-Black-Hat/){:target="_blank"}.

Nous allons utiliser Rubeus, un outil integré dans Covenant, afin de réaliser les attaques *kerberoasting* et *AS-REP roasting*.

Au préalable, nous avons déjà créé un [lab Active Directory vulnérable à ces attaques](https://0xss0rz.github.io/2021-01-14-Lab-AD-Vulnerable/){:target="_blank"}.

Nous utiliserons également SharpSploit (PowerSploit) pour énumérer les utilisateurs et les groupes du domaine.

Pour l'analyse de cette attaque, nous étudierons les *Event Tracing for Windows* ETW qui permettent entre autre d'avoir des données concernant l'utilisation de .NET [3,4]. Pour loguer les événements ETW nous utiliserons SilkService.

SilkService n'est pas un outil encore prêt à être déployé en entreprise. Toutefois la télémétrie qu'il génère est comparable à celle qui peut être utilisée par des *Endpoint Detection and Response* (EDR).

**Config du lab**: VM Win 10 avec SilkService + VM Windows Server 2016 avec AD vulnérable au kerberoasting et au AS-REP roasting + VM Ubuntu avec Covenant.

- Pour installer Covenant sur Ubuntu, voir [lab 1 Initial Access](https://0xss0rz.github.io/2021-01-04-Attack-Detection-Initial-Access-1/){:target="_blank"}
- Pour créer un lab Active Directory vulnérable, voir [cet article](https://0xss0rz.github.io/2021-01-14-Lab-AD-Vulnerable/){:target="_blank"}

# Installation de SilkService

{: .box-note}
*Remarque: Problème rencontré pour loguer les évenements ldap avec Win 7 -> Utiliser une VM Windows 10*

{: .box-note}
***Event Tracing for Windows (ETW**) is a system and software diagnostic, troubleshooting and performance monitoring component of Windows [5] ETW is an efficient kernel-level tracing facility that lets you log kernel or application-defined events to a log file [6].*

**Fonctionnement de SilkETW / SilkService [7]:**

![0e24793ca84cf807598fdc98e5f655c4.png](/img/1b02c98e93b54e0190cefeaf341a3878.png)

Sur la VM Win 10:

- **Pré-requis**

Installer VC++ 2015 x86 redistributable package, *Dependencies\vc2015_redist.x86.exe*: [https://www.microsoft.com/en-us/download/details.aspx?id=48145](https://www.microsoft.com/en-us/download/details.aspx?id=48145){:target="_blank"}

Installer Microsoft .NET Framework 4.5, *Dependencies\dotNetFx45_Full_setup.exe*: [https://www.microsoft.com/en-ie/download/details.aspx?id=30653](https://www.microsoft.com/en-ie/download/details.aspx?id=30653){:target="_blank"}

- **SilkETW**

Télécharger la dernière version de SilkETW: [https://github.com/fireeye/SilkETW/releases](https://github.com/fireeye/SilkETW/releases){:target="_blank"} 

![4e51c45a6ad3a3debfd962ffa73d19c4.png](/img/96dd5895ee994502bb026f830fc15700.png)

- **SilkService**

Avec un compte admin: `sc create SillkService binPath= "C:\Path\To\SilkService.exe" start= demand`

![4bca0e8a288320767cd29a2163b52ae7.png](/img/7affe27dc4b744be872ce1377e10e8c1.png)

![c15438a6c51bfe95f53cdab89f0bc077.png](/img/bc4bc2072897484ab94c45dfff38f7b7.png)

Configuration SilkService utilisée,  `SilkServiceConfig.xml`: 

 ```
<SilkServiceConfig>
    <!--
    Microsoft-Windows-LDAP-Client ETW Provider
    -->
    <ETWCollector>
        <Guid>859efb51-6985-480f-8094-77192b2a7407</Guid>
        <CollectorType>user</CollectorType>
        <ProviderName>099614a5-5dd7-4788-8bc9-e29f43db28fc</ProviderName>
        <UserKeywords>0x1</UserKeywords><!--Search-->
        <OutputType>eventlog</OutputType>
    </ETWCollector>
</SilkServiceConfig>
```
**Explication:** 

- Crée un *consumer* [8] et capture les événements du fournisseur ETW *Microsoft-Windows-LDAP-Client*: capture les requêtes LDAP émises par l'hôte. 
- Le flag 0x1 signifie que nous journalisons uniquement les requêtes de recherche, *search*, et leur paramètres, pas les réponses [9]

Enregistrer sous `SilkServiceConfig.xml` et placer le fichier dans le même dossier que `SilkService.exe`

Au besoin, modifier la ligne GUID par un nouveau GUID [10]. Pour créer un nouveau GUID:  `New-Guid`

![1bde8f0f1479f1a97ad07737154f5f28.png](/img/cb8246a7f224442eb07af334bb73182d.png)

![32bf98c43d14c3cf39b3aa5bdada92aa.png](/img/9ceeb2154d024009b052fef23e9a332c.png)

Lancer SilkService. En tant qu'admin: `Services > SilkService`. Clic-droit `Start`

![2c256a5e08db82bd1295e7d06a484bd4.png](/img/22592c3440c1433182b78df32462cffc.png)

On a désormais des logs `SilkService` dans l'`Event Viewer`

![fcea6c61299095ad9c3461e5bc2c3b1e.png](/img/b3b9a53c873245fc8ad8f0f1ca9a3ceb.png)

# The Hunting ELK, HELK:

The Hunting ELK est un projet développé par Roberto Rodriguez, aka Cyb3rWard0g [11]

![7a0d4c4f2bef52a88e440bca02049c7a.png](/img/208f70e3bb16497590b7e744c883092f.png)

Il est possible de forwarder les évenements ETW dans HELK. 

Pour installer HELK, voir [12,13,14]

Toutefois, HELK nécessite au minimum 5GB de RAM...

# Attaques

Créer un nouveau listener dans Covenant: `http://127.0.0.1:7443/listener`

![da0cd4d5e8a50cc04b0db1e39083f423.png](/img/ffedd8270a43462597f5056319d86076.png)

Créer un binary launcher `http://127.0.0.1:7443/launcher`

![2aa7b8d759e42866880c2bf7680e091f.png](/img/493a214c1c924927b7cc7b6a79e26ab6.png)

Générer le binary launcher et le download: `GruntHTTP.exe`

Transférer le launcher sur la victime, VM Win 10. Dans mon cas j'utilise un serveur http pour le transfert

![3d75d712634518652c832b0bff94cb30.png](/img/e74717117e2e46eebf08e032c40ae75c.png)

Penser à désactiver l'AV et le FW

Exécuter le launcher

Résultat, on a un grunt:

![b81923beaf4387f39a95330badb39ee6.png](/img/3b4aa15c2f6e4473b2f0545d62508db1.png)

On peut interagir avec `Interact`

***Kerberoasting:***

![0d04f2307efcb30fe660d1877d7c4ca0.png](/img/20005c319e3f4564b1a35f205642cdb8.png)
*Source: [15]*

Pour en savoir plus sur cette attaque voir [16,17,18]

Il existe plusieurs outils pour réaliser l'attaque Kerberoast [17,19]. Dans notre cas nous allons utiliser Rubeus [20] qui vient avec Covenant.

`Rubeus kerberoast`

![4fcf43064c9ffa5480ac0a1780792c07.png](/img/25e05ec3239f42af9032006833391931.png)

![beda144f7b7ecee024e0e4724b667b9d.png](/img/77025a9b912f41ce99b08e8328e268a9.png)

On retrouve bien le `user1` que nous avons créé lors de la [mise en place du lab AD vulnérable](https://0xss0rz.github.io/2021-01-14-Lab-AD-Vulnerable/){:target="_blank"}

Il est possible de détecter les activités de reconnaissance LDAP en examinant les filtres de recherche utilisés [21]

Evt ID 3 - Dans `SilkService-Log` on trouve:

![6b7bfffb26186a4e69ea2aea88f1671b.png](/img/1538156f6e81462b812c19ba7c2a8b73.png)

LDAP Recon - SPNs search filter: `(&(samAccountType=805306368)(servicePrincipalName=*)` [21,22,23]

Il s'agit du filtre utilisé par Rubeus

Vérification dans AD:
 
![78397268d75abe79697e75483948a6ae.png](/img/af0bf66bfdd34ba6adb3dab8e1df1f6e.png)
 
![7ce87a1f0833ff262a0866022f1e53f2.png](/img/8726c595ddc44d7a9edb0bdec6e6ff27.png)

{: .box-note}
***AS-REP roasting** is a technique that allows retrieving password hashes for users that have Do not require Kerberos preauthentication property selected* [24]

`Rubeus asreproast`

![660bc0c77525eaefb263899ca8aba5fb.png](/img/df8ad6f670384fa79f217d9b47361ba9.png)

![37396d95c9f7076e5e540003e3889b70.png](/img/b3ca489f84484f39ae3de6b30d8eb19d.png)

On retrouve le `user2` qu'on avait créé précédement lors de la [création du lab AD vulnérable](https://0xss0rz.github.io/2021-01-14-Lab-AD-Vulnerable/){:target="_blank"}

Evt ID 3 - Dans `SilkService-Log` on trouve:

![cdbc3729a3a62006138da49c6f55f83f.png](/img/c1b703f58d54436b8574e7aa1775506b.png)

*"Do not require kerberos preauthentication"* enabled - Search filter: `(userAccountControl:1.2.840.113556.1.4.803:=4194304))` [25]
 
Vérification dans AD:
 
![c127f942757a3eb35b9e77f40d584a5c.png](/img/abfefc52c3bb4719909202ad7f5ed0eb.png)
 
**SharpSploit - PowerSploit**

En plus de Rubeus, Covenant vient avec SharpSploit. SharpSploit permet d'utiliser PowerSploit [26] et son module PowerView.

`Get-DomainGroup “Admins du domaine”`

![3d8be48325aaae45996f9b3318995ad0.png](/img/eecbb9134ea145caa9d295e1f5abbf24.png)

`SilkService-Log`:

![17b81287c9e9746040ecb1d52a3b58bb.png](/img/7c896476dbf946e5826b3d23ca19ff16.png)

# Conclusion

Dans ce lab, nous avons vu comment un attaquant peut identifer des utilisateurs intéressants dans AD et des cibles pour les attaques Kerberoast et AS-REP roasting.

Grâce à la télémétrie ETW nous sommes en mesure de retrouver les filtres LDAP utilisés pour réaliser la reconnaissance.

# Références

[1] MITRE ATT&CK, *Discovery*, [https://attack.mitre.org/tactics/TA0007/](https://attack.mitre.org/tactics/TA0007/){:target="_blank"}

[2] F-Secure, *Attack Detection Fundamentals: Discovery and Lateral Movement - Lab #1*, [https://labs.f-secure.com/blog/attack-detection-fundamentals-discovery-and-lateral-movement-lab-1](https://labs.f-secure.com/blog/attack-detection-fundamentals-discovery-and-lateral-movement-lab-1){:target="_blank"}

[3] F-Secure, *Detecting Malicious Use of .NET – Part 2*, [https://blog.f-secure.com/detecting-malicious-use-of-net-part-2/](https://blog.f-secure.com/detecting-malicious-use-of-net-part-2/){:target="_blank"}

[4] FireEye, *SilkETW: Because Free Telemetry is … Free!*, [https://www.fireeye.com/blog/threat-research/2019/03/silketw-because-free-telemetry-is-free.html](https://www.fireeye.com/blog/threat-research/2019/03/silketw-because-free-telemetry-is-free.html)

[5] Microsoft, *Part 1 - ETW Introduction and Overview*, [https://docs.microsoft.com/en-gb/archive/blogs/ntdebugging/part-1-etw-introduction-and-overview](https://docs.microsoft.com/en-gb/archive/blogs/ntdebugging/part-1-etw-introduction-and-overview){:target="_blank"}

[6] Roberto Rodriguez, *Threat Hunting with ETW events and HELK — Part 1: Installing SilkETW*, [https://medium.com/threat-hunters-forge/threat-hunting-with-etw-events-and-helk-part-1-installing-silketw-6eb74815e4a0](https://medium.com/threat-hunters-forge/threat-hunting-with-etw-events-and-helk-part-1-installing-silketw-6eb74815e4a0){:target="_blank"}

[7] Roberto Rodriguez, *Threat Hunting with ETW events and HELK — Part 2: Shipping ETW events to HELK*, [https://medium.com/threat-hunters-forge/threat-hunting-with-etw-events-and-helk-part-2-shipping-etw-events-to-helk-16837116d2f5](https://medium.com/threat-hunters-forge/threat-hunting-with-etw-events-and-helk-part-2-shipping-etw-events-to-helk-16837116d2f5){:target="_blank"}

[8] Microsoft, *Consumers*, [https://docs.microsoft.com/en-us/windows/win32/etw/about-event-tracing#consumers](https://docs.microsoft.com/en-us/windows/win32/etw/about-event-tracing#consumers){:target="_blank"}

[9] Microsoft, *Event Tracing in LDAP Applications*, [https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ldap/ldap-and-etw](https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ldap/ldap-and-etw){:target="_blank"}

[10] *Tracing as a Service with SilkETW, pt I*, [https://blog.iisreset.me/tracing-as-a-service-with-silketw-pt/](https://blog.iisreset.me/tracing-as-a-service-with-silketw-pt/){:target="_blank"}

[11] Cyb3rWard0g, *HELK*, [https://github.com/Cyb3rWard0g/HELK](https://github.com/Cyb3rWard0g/HELK){:target="_blank"}

[12] Roberto Rodriguez, *Welcome to HELK! : Enabling Advanced Analytics Capabilities*, [https://cyberwardog.blogspot.com/2018/04/welcome-to-helk-enabling-advanced_9.html](https://cyberwardog.blogspot.com/2018/04/welcome-to-helk-enabling-advanced_9.html){:target="_blank"}

[13] The HELK, *Installation*, [https://thehelk.com/installation.html](https://thehelk.com/installation.html){:target="_blank"}

[14] Roberto Rodriguez, *Threat Hunting with ETW events and HELK — Part 2: Shipping ETW events to HELK*, [https://medium.com/threat-hunters-forge/threat-hunting-with-etw-events-and-helk-part-2-shipping-etw-events-to-helk-16837116d2f5](https://medium.com/threat-hunters-forge/threat-hunting-with-etw-events-and-helk-part-2-shipping-etw-events-to-helk-16837116d2f5){:target="_blank"}

[15] MITRE ATT&CK, *Steal or Forge Kerberos Tickets: Kerberoasting*, [https://attack.mitre.org/techniques/T1558/003/](https://attack.mitre.org/techniques/T1558/003/){:target="_blank"}

[16] Hackndo, *Kerberoasting*,[https://beta.hackndo.com/kerberoasting/](https://beta.hackndo.com/kerberoasting/){:target="_blank"}

[17] m0chan, *How To Attack Kerberos 101*, [https://m0chan.github.io/2019/07/31/How-To-Attack-Kerberos-101.html#invoke-kerberoastps1](https://m0chan.github.io/2019/07/31/How-To-Attack-Kerberos-101.html){:target="_blank"}

[18] Pentestlab, *Kerberoast*, [https://pentestlab.blog/2018/06/12/kerberoast/](https://pentestlab.blog/2018/06/12/kerberoast/){:target="_blank"}

[19] Tarlogic, *How To Attack Kerberos*, [https://www.tarlogic.com/en/blog/how-to-attack-kerberos/](https://www.tarlogic.com/en/blog/how-to-attack-kerberos/){:target="_blank"}

[20] *Rubeus*, [https://github.com/GhostPack/Rubeus](https://github.com/GhostPack/Rubeus){:target="_blank"}

[21] Microsoft, *Hunting for reconnaissance activities using LDAP search filters*, [https://techcommunity.microsoft.com/t5/microsoft-defender-for-endpoint/hunting-for-reconnaissance-activities-using-ldap-search-filters/ba-p/824726](https://techcommunity.microsoft.com/t5/microsoft-defender-for-endpoint/hunting-for-reconnaissance-activities-using-ldap-search-filters/ba-p/824726){:target="_blank"}

[22] CalCom, *Preventing LDAP Reconnaissance - The First Step Of AD Attacks*, [https://calcomsoftware.com/preventing-ldap-reconnaissance/](https://calcomsoftware.com/preventing-ldap-reconnaissance/){:target="_blank"}

[23] StealhBits, *LDAP Reconnaissance*, [https://attack.stealthbits.com/ldap-reconnaissance-active-directory](https://attack.stealthbits.com/ldap-reconnaissance-active-directory){:target="_blank"}

[24] Red Team Experiments, *AS-REP Roasting*,[https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/as-rep-roasting-using-rubeus-and-hashcat](https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/as-rep-roasting-using-rubeus-and-hashcat){:target="_blank"}

[25] Microsoft, *Active Directory: LDAP Syntax Filters*, [https://social.technet.microsoft.com/wiki/contents/articles/5392.active-directory-ldap-syntax-filters.aspx](https://social.technet.microsoft.com/wiki/contents/articles/5392.active-directory-ldap-syntax-filters.aspx){:target="_blank"}

[26] Ryon Cobbr, *Introducing SharpSploit: A C# Post-Exploitation Library*, [https://posts.specterops.io/introducing-sharpsploit-a-c-post-exploitation-library-5c7be5f16c51?gi=dbe93a9bd871](https://posts.specterops.io/introducing-sharpsploit-a-c-post-exploitation-library-5c7be5f16c51?gi=dbe93a9bd871){:target="_blank"}

**Poursuivez avec :** 

- [SSH Port Forwarding - Cheat Sheet](https://0xss0rz.github.io/2020-11-21-SSH-Tunneling/)

- [Attack Detection Fundamentals - Initial Access Lab 3](https://0xss0rz.github.io/2021-01-06-Attack-Detection-Initial-Access-3/)

- [Hack The Box - Remote](https://0xss0rz.github.io/2020-08-23-HTB-Remote/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
