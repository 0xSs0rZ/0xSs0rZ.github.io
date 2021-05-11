---
layout: post
title: TryHackMe - Sudo Vulns
subtitle:  Sudo Security Bypass, Sudo Buffer Overflow, Baron Samedit
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
tags: [THM, Linux, Sudo, PrivEsc, buffer overflow, CVE-2019-14287, CVE-2019-18634, CVE-2021-3156, Baron Samedit]
---

![Sudo-1.png](/img/Sudo-1.png)

**L'exploitation de sudo est un excellent moyen d'élever ses privilèges sur une machine Linux. Au cours des dernières années, plusieurs vulnérabilités concernant sudo ont été découvertes notamment les CVE-2019-14287, CVE-2019-18634 et CVE-2021-3156.**

Afin de pratiquer l'exploitation de ces vulnérabilités, [TryHackMe](https://tryhackme.com/){:target="_blank"} a créé une série de trois labs à leur sujet.

Voici une résumé concernant ces trois vulnérabilités:

# CVE-2019-14287 - Sudo Security Bypass

La CVE-2019-14287 affecte les versions de Sudo inférieures à 1.8.28. 

Cette vulnérabilité peut permettre à un utilisateur malveillant d'exécuter des commandes arbitraires en tant qu'utilisateur root, même dans les cas où l'accès root est interdit.

Pour que cette vulnérabilité soit exploitable, dans le fichier `/etc/sudoers`, un utilisateur doit être autorisé à exécuter des programmes comme n'importe quel utilisateur sauf root.

Par exemple: `(ALL, !root) NOPASSWD: /bin/bash`

![Sudo-2.png](/img/Sudo-2.png)

**Exploitation:** `sudo -u#-1 <command>`

Permet d'exécuter une commande en tant que root.

![Sudo-3.png](/img/Sudo-3.png)

Vous trouverez un autre exemple d'exploitation de la CVE-2019-14287 en consultant le solutionnaire de la box [Blunder de HackTheBox](https://0xss0rz.github.io/2020-11-15-HTB-Blunder/){:target="_blank"}

# CVE-2019-18634 - Sudo Buffer Overflow

Cette vulnérabilité utilise un buffer overflow. Elle affecte les versions de Sudo inférieures à 1.8.26.

Pour pouvoir exploiter cette vulnérabilité, la fonctionnalité `pwfeedback` doit être activée dans le fichier `/etc/sudoers`.

Test de la vulnérabilité:

~~~
$ perl -e 'print(("A" x 100 . "\x{00}") x 50)' | sudo -S id
    Password: Segmentation fault
~~~

Saleemrashid a créé un PoC permettant d'exploiter cette CVE: [https://github.com/saleemrashid/sudo-cve-2019-18634](https://github.com/saleemrashid/sudo-cve-2019-18634){:target="_blank"}

**Exploitation:**

![Sudo-4.png](/img/Sudo-4.png)

# CVE-2021-3156 - Baron Samedit

Cette vulnérabilité a été divulguée par Qualys en janvier 2021. Il s'agit d'un heap buffer overflow qui permet à n'importe quel utilisateur d'élever ses privilèges pour devenir root. Aucune configuration spécifique n'est nécessaire !

Baron Samedit affecte les versions de Sudo comprises entre 1.8.2-1.8.31p2 et 1.9.0-1.9.5p1.

Test de la vulnérabilité: `sudoedit -s '\' $(python3 -c 'print("A"*1000)')`

![Sudo-5.png](/img/Sudo-5.png)

Plusieurs PoC ont rapidement été développés notamment celui de blasty: [https://github.com/blasty/CVE-2021-3156](https://github.com/blasty/CVE-2021-3156){:target="_blank"} 

Compilation de l'exploit:

![Sudo-6.png](/img/Sudo-6.png)

**Exploitation:**

![Sudo-7.png](/img/Sudo-7.png)

# Références

[1] CVE-2019-14287 sudo Vulnerability Allows Bypass of User Restrictions, [https://blog.aquasec.com/cve-2019-14287-sudo-linux-vulnerability](https://blog.aquasec.com/cve-2019-14287-sudo-linux-vulnerability){:target="_blank"}
[2] Sudo 1.8.25p - 'pwfeedback' Buffer Overflow (PoC), [https://www.exploit-db.com/exploits/47995](https://www.exploit-db.com/exploits/47995){:target="_blank"}
[3] CVE-2021-3156: Heap-Based Buffer Overflow in Sudo (Baron Samedit), [https://blog.qualys.com/vulnerabilities-research/2021/01/26/cve-2021-3156-heap-based-buffer-overflow-in-sudo-baron-samedit](https://blog.qualys.com/vulnerabilities-research/2021/01/26/cve-2021-3156-heap-based-buffer-overflow-in-sudo-baron-samedit){:target="_blank"}

**Poursuivez avec :** 

- [JISCTF 2020 - Quals](https://0xss0rz.github.io/2020-11-22-JISCTF-2020-Quals/)

- [Attack Detection Fundamentals - Initial Access Lab 3](https://0xss0rz.github.io/2021-01-06-Attack-Detection-Initial-Access-3/)

- [San Diego CTF 2021 - Git Good](https://0xss0rz.github.io/2021-05-10-San-Diego-CTF-Git-Good/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
