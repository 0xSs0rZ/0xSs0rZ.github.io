---
layout: post
title: OverTheWire - Bandit 5 - Git Part
subtitle: OverTheWire - Bandit - Level 27 → 33 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [Waregame, CTF, OverTheWire, Git, Commandes, Linux, Write-Up]
comments: false
---

**Les repos Git peuvent permettre d'obtenir des infos confidentielles, etc. Voici quelques exemples provenant des challs Bandit d'Over The Wire**


# bandit28

There is a git repository at ssh://bandit27-git@localhost/home/bandit27-git/repo. The password for the user bandit27-git is the same as for the user bandit27.

Clone the repository and find the password for the next level.

~~~
bandit27@bandit:~$ git clone ssh://bandit27-git@localhost/home/bandit27-git/repo
fatal: could not create work tree dir 'repo': Permission denied
bandit27@bandit:~$ mkdir /tmp/b27_0xss0rz
bandit27@bandit:~$ cd /tmp/b27_0xss0rz
bandit27@bandit:/tmp/b27_0xss0rz$ ls
bandit27@bandit:/tmp/b27_0xss0rz$ git clone ssh://bandit27-git@localhost/home/bandit27-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit27/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit27/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit27-git@localhost's password:
Permission denied, please try again.
bandit27-git@localhost's password:
remote: Counting objects: 3, done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (3/3), done.
bandit27@bandit:/tmp/b27_0xss0rz$ ls
repo
bandit27@bandit:/tmp/b27_0xss0rz$ cd repo/
bandit27@bandit:/tmp/b27_0xss0rz/repo$ ls
README
bandit27@bandit:/tmp/b27_0xss0rz/repo$ cat README
The password to the next level is: 0ef186ac70e04ea33b4c1853d2526fa2
bandit27@bandit:/tmp/b27_0xss0rz/repo$
~~~

# bandit29

~~~
bandit27@bandit:~$ cd /tmp/b27_0xss0rz
bandit27@bandit:/tmp/b27_0xss0rz$ ls
bandit27@bandit:/tmp/b27_0xss0rz$ git clone ssh://bandit27-git@localhost/home/bandit27-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit27/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit27/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit27-git@localhost's password:
Permission denied, please try again.
bandit27-git@localhost's password:
remote: Counting objects: 3, done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (3/3), done.
bandit27@bandit:/tmp/b27_0xss0rz$ ls
repo
bandit27@bandit:/tmp/b27_0xss0rz$ cd repo/
bandit27@bandit:/tmp/b27_0xss0rz/repo$ ls
README
bandit27@bandit:/tmp/b27_0xss0rz/repo$ cat README
The password to the next level is: 0ef186ac70e04ea33b4c1853d2526fa2
bandit27@bandit:/tmp/b27_0xss0rz/repo$ exit
logout
Connection to bandit.labs.overthewire.org closed.
tom@LAPTOP-O74G4SQM:~$ ssh bandit28@bandit.labs.overthewire.org -p 2220
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit28@bandit.labs.overthewire.org's password:
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

bandit28@bandit:~$ mkdir /tmp/b28_0xss0rz
bandit28@bandit:~$ cd /tmp/b28_0xss0rz
bandit28@bandit:/tmp/b28_0xss0rz$ git clone ssh://bandit28-git@localhost/home/bandit28-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit28/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit28/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit28-git@localhost's password:
Permission denied, please try again.
bandit28-git@localhost's password:
remote: Counting objects: 9, done.
remote: Compressing objects: 100% (6/6), done.
Receiving objects: 100% (9/9), 795 bytes | 0 bytes/s, done.
remote: Total 9 (delta 2), reused 0 (delta 0)
Resolving deltas: 100% (2/2), done.
bandit28@bandit:/tmp/b28_0xss0rz$ ls
repo
bandit28@bandit:/tmp/b28_0xss0rz$ cd repo/
bandit28@bandit:/tmp/b28_0xss0rz/repo$ ls
README.md
bandit28@bandit:/tmp/b28_0xss0rz/repo$ cat README.md
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: xxxxxxxxxx

bandit28@bandit:/tmp/b28_0xss0rz/repo$ ls -la
total 16
drwxr-sr-x 3 bandit28 root 4096 May  8 16:05 .
drwxr-sr-x 3 bandit28 root 4096 May  8 16:05 ..
drwxr-sr-x 8 bandit28 root 4096 May  8 16:05 .git
-rw-r--r-- 1 bandit28 root  111 May  8 16:05 README.md
bandit28@bandit:/tmp/b28_0xss0rz/repo$ git show
commit edd935d60906b33f0619605abd1689808ccdd5ee
Author: Morla Porla <morla@overthewire.org>
Date:   Thu May 7 20:14:49 2020 +0200

    fix info leak

diff --git a/README.md b/README.md
index 3f7cee8..5c6457b 100644
--- a/README.md
+++ b/README.md
@@ -4,5 +4,5 @@ Some notes for level29 of bandit.
 ## credentials

 - username: bandit29
-- password: bbc96594b4e001778eee9975372716b2
+- password: xxxxxxxxxx

bandit28@bandit:/tmp/b28_0xss0rz/repo$
~~~

# bandit30

~~~
bandit29@bandit:~$ mkdir /tmp/b29_0xss0rz
bandit29@bandit:~$ cd /tmp/b29_0xss0rz
bandit29@bandit:/tmp/b29_0xss0rz$ git clone ssh://bandit29-git@localhost/home/bandit29-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit29/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit29/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit29-git@localhost's password:
remote: Counting objects: 16, done.
remote: Compressing objects: 100% (11/11), done.
remote: Total 16 (delta 2), reused 0 (delta 0)
Receiving objects: 100% (16/16), 1.43 KiB | 0 bytes/s, done.
Resolving deltas: 100% (2/2), done.
bandit29@bandit:/tmp/b29_0xss0rz$ ls
repo
bandit29@bandit:/tmp/b29_0xss0rz$ cd repo/
bandit29@bandit:/tmp/b29_0xss0rz/repo$ ls
README.md
bandit29@bandit:/tmp/b29_0xss0rz/repo$ ls -la
total 16
drwxr-sr-x 3 bandit29 root 4096 May  8 16:07 .
drwxr-sr-x 3 bandit29 root 4096 May  8 16:07 ..
drwxr-sr-x 8 bandit29 root 4096 May  8 16:07 .git
-rw-r--r-- 1 bandit29 root  131 May  8 16:07 README.md
bandit29@bandit:/tmp/b29_0xss0rz/repo$ cat README.md
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: <no passwords in production!>

bandit29@bandit:/tmp/b29_0xss0rz/repo$ git show
commit 208f463b5b3992906eabf23c562eda3277fea912
Author: Ben Dover <noone@overthewire.org>
Date:   Thu May 7 20:14:51 2020 +0200

    fix username

diff --git a/README.md b/README.md
index 2da2f39..1af21d3 100644
--- a/README.md
+++ b/README.md
@@ -3,6 +3,6 @@ Some notes for bandit30 of bandit.

 ## credentials

-- username: bandit29
+- username: bandit30
 - password: <no passwords in production!>


bandit29@bandit:/tmp/b29_0xss0rz/repo$ git log
commit 208f463b5b3992906eabf23c562eda3277fea912
Author: Ben Dover <noone@overthewire.org>
Date:   Thu May 7 20:14:51 2020 +0200

    fix username

commit 18a6fd6d5ef7f0874bbdda2fa0d77b3b81fd63f7
Author: Ben Dover <noone@overthewire.org>
Date:   Thu May 7 20:14:51 2020 +0200

    initial commit of README.md
bandit29@bandit:/tmp/b29_0xss0rz/repo$ git show 18a6fd6d5ef7f0874bbdda2fa0d77b3b81fd63f7
commit 18a6fd6d5ef7f0874bbdda2fa0d77b3b81fd63f7
Author: Ben Dover <noone@overthewire.org>
Date:   Thu May 7 20:14:51 2020 +0200

    initial commit of README.md

diff --git a/README.md b/README.md
new file mode 100644
index 0000000..2da2f39
--- /dev/null
+++ b/README.md
@@ -0,0 +1,8 @@
+# Bandit Notes
+Some notes for bandit30 of bandit.
+
+## credentials
+
+- username: bandit29
+- password: <no passwords in production!>
+
bandit29@bandit:/tmp/b29_0xss0rz/repo$ git branch
* master
bandit29@bandit:/tmp/b29_0xss0rz/repo$ git branch -r
  origin/HEAD -> origin/master
  origin/dev
  origin/master
  origin/sploits-dev
bandit29@bandit:/tmp/b29_0xss0rz/repo$ git checkout dev
Branch dev set up to track remote branch dev from origin.
Switched to a new branch 'dev'
bandit29@bandit:/tmp/b29_0xss0rz/repo$ git branch
* dev
  master
bandit29@bandit:/tmp/b29_0xss0rz/repo$ git log
commit bc833286fca18a3948aec989f7025e23ffc16c07
Author: Morla Porla <morla@overthewire.org>
Date:   Thu May 7 20:14:52 2020 +0200

    add data needed for development

commit 8e6c203f885bd4cd77602f8b9a9ea479929ffa57
Author: Ben Dover <noone@overthewire.org>
Date:   Thu May 7 20:14:51 2020 +0200

    add gif2ascii

commit 208f463b5b3992906eabf23c562eda3277fea912
Author: Ben Dover <noone@overthewire.org>
Date:   Thu May 7 20:14:51 2020 +0200

    fix username

commit 18a6fd6d5ef7f0874bbdda2fa0d77b3b81fd63f7
Author: Ben Dover <noone@overthewire.org>
Date:   Thu May 7 20:14:51 2020 +0200

    initial commit of README.md
bandit29@bandit:/tmp/b29_0xss0rz/repo$ git show bc833286fca18a3948aec989f7025e23ffc16c07
commit bc833286fca18a3948aec989f7025e23ffc16c07
Author: Morla Porla <morla@overthewire.org>
Date:   Thu May 7 20:14:52 2020 +0200

    add data needed for development

diff --git a/README.md b/README.md
index 1af21d3..39b87a8 100644
--- a/README.md
+++ b/README.md
@@ -4,5 +4,5 @@ Some notes for bandit30 of bandit.
 ## credentials

 - username: bandit30
-- password: <no passwords in production!>
+- password: 5b90576bedb2cc04c86a9e924ce42faf

bandit29@bandit:/tmp/b29_0xss0rz/repo$
~~~

# bandit31

~~~
bandit30@bandit:/tmp/b30_0xss0rz$ git clone ssh://bandit30-git@localhost/home/bandit30-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit30/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit30/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit30-git@localhost's password:
Permission denied, please try again.
bandit30-git@localhost's password:
remote: Counting objects: 4, done.
remote: Total 4 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (4/4), done.
bandit30@bandit:/tmp/b30_0xss0rz$ cd repo/
bandit30@bandit:/tmp/b30_0xss0rz/repo$ ls
README.md
bandit30@bandit:/tmp/b30_0xss0rz/repo$ cat README.md
just an epmty file... muahaha
bandit30@bandit:/tmp/b30_0xss0rz/repo$ git show
commit 3aefa229469b7ba1cc08203e5d8fa299354c496b
Author: Ben Dover <noone@overthewire.org>
Date:   Thu May 7 20:14:54 2020 +0200

    initial commit of README.md

diff --git a/README.md b/README.md
new file mode 100644
index 0000000..029ba42
--- /dev/null
+++ b/README.md
@@ -0,0 +1 @@
+just an epmty file... muahaha
bandit30@bandit:/tmp/b30_0xss0rz/repo$ git show 3aefa229469b7ba1cc08203e5d8fa299354c496b
commit 3aefa229469b7ba1cc08203e5d8fa299354c496b
Author: Ben Dover <noone@overthewire.org>
Date:   Thu May 7 20:14:54 2020 +0200

    initial commit of README.md

diff --git a/README.md b/README.md
new file mode 100644
index 0000000..029ba42
--- /dev/null
+++ b/README.md
@@ -0,0 +1 @@
+just an epmty file... muahaha
bandit30@bandit:/tmp/b30_0xss0rz/repo$ git log
commit 3aefa229469b7ba1cc08203e5d8fa299354c496b
Author: Ben Dover <noone@overthewire.org>
Date:   Thu May 7 20:14:54 2020 +0200

    initial commit of README.md
bandit30@bandit:/tmp/b30_0xss0rz/repo$ git branch
* master
bandit30@bandit:/tmp/b30_0xss0rz/repo$ git branch -r
  origin/HEAD -> origin/master
  origin/master
bandit30@bandit:/tmp/b30_0xss0rz/repo$ git tag
secret
bandit30@bandit:/tmp/b30_0xss0rz/repo$ git show secret
47e603bb428404d265f59c42920d81e5
bandit30@bandit:/tmp/b30_0xss0rz/repo$
~~~

# bandit32

~~~
bandit31@bandit:/tmp/b32_0xss0rz/repo$ git show
commit 701b33b545902a670a46088731949ae040983d80
Author: Ben Dover <noone@overthewire.org>
Date:   Thu May 7 20:14:56 2020 +0200

    initial commit

diff --git a/.gitignore b/.gitignore
new file mode 100644
index 0000000..2211df6
--- /dev/null
+++ b/.gitignore
@@ -0,0 +1 @@
+*.txt
diff --git a/README.md b/README.md
new file mode 100644
index 0000000..0edecc0
--- /dev/null
+++ b/README.md
@@ -0,0 +1,7 @@
+This time your task is to push a file to the remote repository.
+
+Details:
+    File name: key.txt
+    Content: 'May I come in?'
+    Branch: master
+
bandit31@bandit:/tmp/b32_0xss0rz/repo$ echo 'May I come in?' > key.txt
bandit31@bandit:/tmp/b32_0xss0rz/repo$ ls
key.txt  README.md
bandit31@bandit:/tmp/b32_0xss0rz/repo$ git add key.txt
bandit31@bandit:/tmp/b32_0xss0rz/repo$ git commit -m 'poc'
[master e9bcce4] poc
 2 files changed, 2 insertions(+)
 create mode 100644 key.txt
 create mode 100644 "\302\240key.txt"
bandit31@bandit:/tmp/b32_0xss0rz/repo$ git push
Could not create directory '/home/bandit31/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit31/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit31-git@localhost's password:
Counting objects: 3, done.
Delta compression using up to 2 threads.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 323 bytes | 0 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0)
remote: ### Attempting to validate files... ####
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
remote: Well done! Here is the password for the next level:
remote: 56a9bf19c63d650ce78e6ec0354ee45e
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
To ssh://localhost/home/bandit31-git/repo
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'ssh://bandit31-git@localhost/home/bandit31-git/repo'
bandit31@bandit:/tmp/b32_0xss0rz/repo$
~~~

# bandit 33

Quand on se log on tombe sur:

~~~
WELCOME TO THE UPPERCASE SHELL
>> ls
sh: 1: LS: not found
>> ls
sh: 1: LS: not found

avec $0 on peut retrouver un shell normal

>> $0
$ id
uid=11033(bandit33) gid=11032(bandit32) groups=11032(bandit32)
$ cat /etc/bandit_pass/bandit33
c9c3199ddf4121b10cf581a98d51caee
$
~~~

**Retrouvez les solutions :**
- pour les niveaux 0 à 10 : [OverTheWire -Bandit 1](https://0xss0rz.github.io/2019-08-20-OverTheWire-Bandit-1-Write-Ups/)
- pour les niveaux 11 à 23 : [OverTheWire - Bandit 2](https://0xss0rz.github.io/2019-08-22-OverTheWire-Bandit-2-Write-Ups/)
- pour la partie réseau, SSH, SSL et telnet: [OverTheWire - Bandit 3](https://0xss0rz.github.io/2020-05-16-OverTheWire-Bandit-3-SSH-Part/)
- pour la partie élévation de privilèges (SUID, cron, vim): [OverTheWire - Bandit 4](https://0xss0rz.github.io/2020-05-17-OverTheWire-Bandit-4-EoP/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
