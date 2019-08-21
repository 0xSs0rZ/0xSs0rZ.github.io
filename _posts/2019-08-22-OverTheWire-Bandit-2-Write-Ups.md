---
layout: post
title: OverTheWire - Bandit 2
subtitle: OverTheWire - Bandit - Level 11 → 23 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [CTF, OverTheWire, Réseautique, Commandes, Write-Up]
comments: false
---

**Nous continuons notre série sur le wargame _Bandit_ d' _OverTheWire._ Voici les solutions pour les niveaux 11 à 23**

Retrouvez les solutions pour les niveaux 0 à 11 ici: [OverTheWire - Bandit 2](https://0xss0rz.github.io/2019-08-20-OverTheWire-Bandit-1-Write-Ups/)

## 0x00 - Bandit Level 11 → Level 12

The password for the next level is stored in the file data.txt, where all lowercase (a-z) and uppercase (A-Z) letters have been rotated by 13 positions

**Solution:**

~~~
bandit11@bandit:~$ ls
data.txt
bandit11@bandit:~$ cat data.txt 
Gur cnffjbeq vf 5Gr8L4qetPEsPk8htqjhRK8XSP6x2RHh
bandit11@bandit:~$ python
Python 2.7.13 (default, Sep 26 2018, 18:42:22) 
[GCC 6.3.0 20170516] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import codecs
>>> codecs.decode("Gur cnffjbeq vf 5Gr8L4qetPEsPk8htqjhRK8XSP6x2RHh", "rot_13")
u'The password is passwordBandit12'
~~~

## 0x01 - Bandit Level 12 → Level 13

The password for the next level is stored in the file data.txt, which is a hexdump of a file that has been repeatedly compressed. For this level it may be useful to create a directory under /tmp in which you can work using mkdir. For example: mkdir /tmp/myname123. Then copy the datafile using cp, and rename it using mv (read the manpages!)

_Ref:_ [https://unix.stackexchange.com/questions/306515/how-to-convert-hexdump-to-text](https://unix.stackexchange.com/questions/306515/how-to-convert-hexdump-to-text)

**Solution:**

~~~
bandit12@bandit:~$ ls
data.txt
bandit12@bandit:~$ cd /tmp
bandit12@bandit:/tmp$ mkdir 0xSs
bandit12@bandit:/tmp$ cd /home/bandit12
bandit12@bandit:~$ cp data.txt /tmp/0xSs/data.txt
bandit12@bandit:~$ cd /tmp/0xSs
bandit12@bandit:/tmp/0xSs$ ls
data.txt
bandit12@bandit:/tmp/0xSs$ xxd -r data.txt > revert1
bandit12@bandit:/tmp/0xSs$ file revert1 
revert1: gzip compressed data, was "data2.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix
bandit12@bandit:/tmp/0xSs$ gunzip -c revert1 > unzip1
bandit12@bandit:/tmp/0xSs$ file unzip1 
unzip1: bzip2 compressed data, block size = 900k
bandit12@bandit:/tmp/0xSs$ bzip2 -dk unzip1
bzip2: Can't guess original name for unzip1 -- using unzip1.out
bandit12@bandit:/tmp/0xSs$ file unzip1.out 
unzip1.out: gzip compressed data, was "data4.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix
bandit12@bandit:/tmp/0xSs$ gunzip -c unzip1.out > unzip2
bandit12@bandit:/tmp/0xSs$ file unzip2
unzip2: POSIX tar archive (GNU)
bandit12@bandit:/tmp/0xSs$ tar -xvf unzip2
data5.bin
bandit12@bandit:/tmp/0xSs$ file data5.bin 
data5.bin: POSIX tar archive (GNU)
bandit12@bandit:/tmp/0xSs$ tar -xvf data5.bin
data6.bin
bandit12@bandit:/tmp/0xSs$ file data6.bin
data6.bin: bzip2 compressed data, block size = 900k
bandit12@bandit:/tmp/0xSs$ bzip2 -dk data6.bin
bzip2: Can't guess original name for data6.bin -- using data6.bin.out
bandit12@bandit:/tmp/0xSs$ file data6.bin.out
data6.bin.out: POSIX tar archive (GNU)
bandit12@bandit:/tmp/0xSs$ tar -xvf data6.bin.out
data8.bin
bandit12@bandit:/tmp/0xSs$ file data8.bin
data8.bin: gzip compressed data, was "data9.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix
bandit12@bandit:/tmp/0xSs$ gunzip -c data8.bin > unzip3
bandit12@bandit:/tmp/0xSs$ file unzip3
unzip3: ASCII text
bandit12@bandit:/tmp/0xSs$ cat unzip3
The password is passwordBandit13
~~~

## 0x02 - Bandit Level 13 → Level 14

The password for the next level is stored in /etc/bandit_pass/bandit14 and can only be read by user bandit14. For this level, you don’t get the next password, but you get a private SSH key that can be used to log into the next level. Note: localhost is a hostname that refers to the machine you are working on

_Ref:_ [https://support.rackspace.com/how-to/logging-in-with-an-ssh-private-key-on-linuxmac/](https://support.rackspace.com/how-to/logging-in-with-an-ssh-private-key-on-linuxmac/)

**Solution:**

~~~
bandit13@bandit:~$ ls
sshkey.private
bandit13@bandit:~$ cat sshkey.private 
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAxkkOE83W2cOT7IWhFc9aPaaQmQDdgzuXCv+ppZHa++buSkN+
(...)
kAWpXbv5tbkkzbS0eaLPTKgLzavXtQoTtKwrjpolHKIHUz6Wu+n4abfAIRFubOdN
/+aLoRQ0yBDRbdXMsZN/jvY44eM+xRLdRVyMmdPtP8belRi2E2aEzA==
-----END RSA PRIVATE KEY-----
bandit13@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
┌─[xor@parrot]─[~]
└──╼ $sudo vim sshkey.private
[sudo] Mot de passe de xor :
#Copier la clé dans ce fichier 
┌─[xor@parrot]─[~]
└──╼ $ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220
bandit14@bandit:~$ cat /etc/bandit_pass/bandit14
passwordBandit14
~~~

## 0x03 - Bandit Level 14 → Level 15

The password for the next level can be retrieved by submitting the password of the current level to port 30000 on localhost

**Solution:**

~~~
bandit14@bandit:~$ echo passwordBandit14 | nc localhost 30000
Correct!
passwordBandit15
~~~

## 0x04 - Bandit Level 15 → Level 16

The password for the next level can be retrieved by submitting the password of the current level to port 30001 on localhost using SSL encryption.

Helpful note: Getting “HEARTBEATING” and “Read R BLOCK”? Use -ign_eof and read the “CONNECTED COMMANDS” section in the manpage. Next to ‘R’ and ‘Q’, the ‘B’ command also works in this version of that command…

_Ref:_ [https://www.feistyduck.com/library/openssl-cookbook/online/ch-testing-with-openssl.html](https://www.feistyduck.com/library/openssl-cookbook/online/ch-testing-with-openssl.html)

**Solution:**
 
~~~
bandit15@bandit:~$ echo passwordBandit15 | openssl s_client -quiet -connect localhost:30001
depth=0 CN = localhost
verify error:num=18:self signed certificate
verify return:1
depth=0 CN = localhost
verify return:1
Correct!
passwordBandit16
~~~

## 0x05 - Bandit Level 16 → Level 17

The credentials for the next level can be retrieved by submitting the password of the current level to a port on localhost in the range 31000 to 32000. First find out which of these ports have a server listening on them. Then find out which of those speak SSL and which don’t. There is only 1 server that will give the next credentials, the others will simply send back to you whatever you send to it.

**Solution:** 

~~~
bandit16@bandit:~$ nmap -p 31000-32000 localhost

Starting Nmap 7.40 ( https://nmap.org ) at 2019-08-19 18:56 CEST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00026s latency).
Not shown: 999 closed ports
PORT      STATE SERVICE
31518/tcp open  unknown
31790/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 0.09 seconds
bandit16@bandit:~$ echo passwordBandit15 | openssl s_client -quiet -connect localhost:31790
depth=0 CN = localhost
verify error:num=18:self signed certificate
verify return:1
depth=0 CN = localhost
verify return:1
Correct!
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAvmOkuifmMg6HL2YPIOjon6iWfbp7c3jx34YkYWqUH57SUdyJ
imZzeyGC0gtZPGujUSxiJSWI/
(...)
77pBAoGAMmjmIJdjp+Ez8duyn3ieo36yrttF5NSsJLAbxFpdlc1gvtGCWW+9Cq0b
dxviW8+TFVEBl1O4f7HVm6EpTscdDxU+bCXWkfjuRb7Dy9GOtt9JPsX8MBTakzh3
vBgsyi/sN3RqRBcGU40fOoZyfAMT8s1m/uYv52O6IgeuZ/ujbjY=
-----END RSA PRIVATE KEY-----
~~~

La clé ssh est le credential pour le prochain niveau.
Copier la et enregistrer la dans un fichier. Voir Bandit Level 13 → 14 pour utiliser une clé lors d'une connexion SSH.

## 0x06 - Bandit Level 17 → Level 18

There are 2 files in the homedirectory: passwords.old and passwords.new. The password for the next level is in passwords.new and is the only line that has been changed between passwords.old and passwords.new

NOTE: if you have solved this level and see ‘Byebye!’ when trying to log into bandit18, this is related to the next level, bandit19

**Solution:**

~~~
bandit17@bandit:~$ diff passwords.old  passwords.new
42c42
< oldPassword
---
> passwordBandit18
~~~

## 0x07 - Bandit Level 18 → Level 19

The password for the next level is stored in a file readme in the homedirectory. Unfortunately, someone has modified .bashrc to log you out when you log in with SSH.

Explications:

-t pour forcer la connection sur un port tty: terminal = tty = text input/output environment
/bin/sh pour lancer le shell bach

/!\ il faut être loggué sur le compte de bandit17

**Solution:**

~~~
$ssh -i sshkey.private bandit17@bandit.labs.overthewire.org -p 2220

bandit17@bandit:~$ ssh -t bandit18@localhost /bin/sh
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit17/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0640 for '/home/bandit17/.ssh/id_rsa' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "/home/bandit17/.ssh/id_rsa": bad permissions
bandit18@localhost's password: 
$ ls
readme
$ cat readme
passwordBandit19
~~~

## Bandit Level 19 → Level 20

To gain access to the next level, you should use the setuid binary in the homedirectory. Execute it without arguments to find out how to use it. The password for this level can be found in the usual place (/etc/bandit_pass), after you have used the setuid binary.

**Solution:**

~~~
bandit19@bandit:~$ ls -la
total 28
drwxr-xr-x  2 root     root     4096 Oct 16  2018 .
drwxr-xr-x 41 root     root     4096 Oct 16  2018 ..
-rwsr-x---  1 **bandit20** bandit19 7296 Oct 16  2018 bandit20-do
-rw-r--r--  1 root     root      220 May 15  2017 .bash_logout
-rw-r--r--  1 root     root     3526 May 15  2017 .bashrc
-rw-r--r--  1 root     root      675 May 15  2017 .profile
# le propriétaire de bandit20-do est bandit20
bandit19@bandit:~$ ./bandit20-do
Run a command as another user.
  Example: ./bandit20-do id
bandit19@bandit:~$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
(...)
bandit20:x:11020:11020:bandit level 20:/home/bandit20:/bin/bash
(...)
# Essai avec l'id de bandit20
bandit19@bandit:~$ ./bandit20-do 11020
env: ‘11020’: No such file or directory
# Ok il faut un fichier: "The password for this level can be found in the usual place (/etc/bandit_pass)"
bandit19@bandit:~$ find /etc/*pass
/etc/bandit_pass
(...)
/etc/bandit_pass/bandit20
(...)
bandit19@bandit:~$ cat /etc/bandit_pass/bandit20
cat: /etc/bandit_pass/bandit20: Permission denied #rien d'étonnant
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
passwordBandit20
~~~

## 0x09 - Bandit Level 20 → Level 21

There is a setuid binary in the homedirectory that does the following: it makes a connection to localhost on the port you specify as a commandline argument. It then reads a line of text from the connection and compares it to the password in the previous level (bandit20). If the password is correct, it will transmit the password for the next level (bandit21).

_Ref:_ [https://linuxize.com/post/how-to-use-linux-screen/](https://linuxize.com/post/how-to-use-linux-screen/)

**Solution:**

~~~
#Utiliser screen
bandit20@bandit:~$ screen

#Ecran 1
bandit20@bandit:~$ ls
suconnect

#“Ctrl-A” and “c“ pour creer un nouvel écran
#Ecran 2
bandit20@bandit:~$ nc -lvp 4444
listening on [any] 4444 ...

#“Ctrl-A” and “n“ pour retourner à l'écran 1
#écran 1
bandit20@bandit:~$ ./suconnect 4444

#“Ctrl-A” and “p“ pour retourner à l'écran 2
#écran 2
connect to [127.0.0.1] from localhost [127.0.0.1] 53814
#saisir le mot de passe
passwordBandit20

#écran 1
bandit20@bandit:~$ ls
suconnect
bandit20@bandit:~$ ./suconnect 4444
Read: passwordBandit20
Password matches, sending next password
bandit20@bandit:~$ 

#écran 2
bandit20@bandit:~$ ls
suconnect
bandit20@bandit:~$ nc -lvp 4444
listening on [any] 4444 ...
connect to [127.0.0.1] from localhost [127.0.0.1] 53814
passwordBandit20
passwordBandit21
bandit20@bandit:~$ 
~~~

## 0x0A - Bandit Level 21 → Level 22

A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in /etc/cron.d/ for the configuration and see what command is being executed

**Solution:**

~~~
bandit21@bandit:~$ cd /etc/cron.d/
bandit21@bandit:/etc/cron.d$ ls
cronjob_bandit22  cronjob_bandit23  cronjob_bandit24
bandit21@bandit:/etc/cron.d$ cat cronjob_bandit22
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
bandit21@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
bandit21@bandit:/etc/cron.d$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
passwordBandit22
~~~

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).


