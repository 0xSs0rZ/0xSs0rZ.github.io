---
layout: post
title: OverTheWire - Bandit 1
subtitle: OverTheWire - Bandit - Level 0 → 11 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [CTF, OverTheWire, Bandit, Write-Up]
comments: false
---

**Le Wargame d' _OverTheWire_ est l'endroit idéal pour se dérouiller les doigts et parfaire ses connaissances des commandes Linux. Voici les solutions des niveaux 0 à 11 du jeu _Bandit_**

Avant de débuter ce _wargame_, si vous ne maitrisez pas encore les commandes essentielles sous Linux, visitez: [Commandes essentielles](https://0xss0rz.github.io/2019-08-19-commandes-essentieles/)

## 0x00 - Bandit Level 0

The goal of this level is for you to log into the game using SSH. The host to which you need to connect is bandit.labs.overthewire.org, on port 2220. The username is bandit0 and the password is bandit0. Once logged in, go to the Level 1 page to find out how to beat Level 1.

Solution:

~~~
ssh bandit0@bandit.labs.overthewire.org -p 2220
~~~

## 0x01 - Bandit Level 0 → Level 1

The password for the next level is stored in a file called readme located in the home directory. Use this password to log into bandit1 using SSH. Whenever you find a password for a level, use SSH (on port 2220) to log into that level and continue the game.

Solution:

~~~
bandit0@bandit:~$ ls
readme
bandit0@bandit:~$ cat readme
~~~

## 0x02 - Bandit Level 1 → Level 2

The password for the next level is stored in a file called - located in the home directory

~~~
bandit1@bandit:~$ ls
-
bandit1@bandit:~$ cat ./-
~~~

Ref: [https://unix.stackexchange.com/questions/189251/how-to-read-dash-files/189252](https://unix.stackexchange.com/questions/189251/how-to-read-dash-files/189252)

## 0x03 - Bandit Level 2 → Level 3

The password for the next level is stored in a file called spaces in this filename located in the home directory

Solution:

~~~
bandit2@bandit:~$ ls
spaces in this filename
bandit2@bandit:~$ cat spaces\ in\ this\ filename 
~~~

## 0x04 - Bandit Level 3 → Level 4

The password for the next level is stored in a hidden file in the inhere directory

Solution:

~~~
bandit3@bandit:~$ cd inhere/
bandit3@bandit:~/inhere$ ls -la
total 12
drwxr-xr-x 2 root    root    4096 Oct 16  2018 .
drwxr-xr-x 3 root    root    4096 Oct 16  2018 ..
-rw-r----- 1 bandit4 bandit3   33 Oct 16  2018 .hidden
bandit3@bandit:~/inhere$ cat .hidden 
~~~

## 0x05 - Bandit Level 4 → Level 5

The password for the next level is stored in the only human-readable file in the inhere directory. Tip: if your terminal is messed up, try the “reset” command.

Ref: [https://linuxhandbook.com/file-command/](https://linuxhandbook.com/file-command/)

Solution:

~~~
bandit4@bandit:~$ cd inhere/
bandit4@bandit:~/inhere$ ls
-file00  -file02  -file04  -file06  -file08
-file01  -file03  -file05  -file07  -file09
bandit4@bandit:~/inhere$ file -f -file07
~~~

## 0x06 - Bandit Level 5 → Level 6

The password for the next level is stored in a file somewhere under the inhere directory and has all of the following properties:

    human-readable
    1033 bytes in size
    not executable

Ref: [http://www.ducea.com/2008/02/12/linux-tips-find-all-files-of-a-particular-size/](http://www.ducea.com/2008/02/12/linux-tips-find-all-files-of-a-particular-size/)

Solution:

~~~ 
bandit5@bandit:~$ cd inhere/
bandit5@bandit:~/inhere$ find -size 1033c
./maybehere07/.file2
bandit5@bandit:~/inhere$ cat ./maybehere07/.file2
~~~

## 0x07 - Bandit Level 6 → Level 7

The password for the next level is stored somewhere on the server and has all of the following properties:

    owned by user bandit7
    owned by group bandit6
    33 bytes in size

Ref: [https://www.cyberciti.biz/faq/how-do-i-find-all-the-files-owned-by-a-particular-user-or-group/](https://www.cyberciti.biz/faq/how-do-i-find-all-the-files-owned-by-a-particular-user-or-group/)

Solution:

~~~
bandit6@bandit:/$ find -size 33c -group bandit6 -user bandit7
find: ‘./run/lvm’: Permission denied
find: ‘./run/screen/S-bandit27’: Permission denied
(...)
find: ‘./var/cache/apt/archives/partial’: Permission denied
./var/lib/dpkg/info/bandit7.password
find: ‘./var/lib/apt/lists/partial’: Permission denied
find: ‘./var/lib/polkit-1’: Permission denied
(...)
find: ‘./proc/13174/fd/5’: No such file or directory
find: ‘./proc/13174/fdinfo/5’: No such file or directory
find: ‘./boot/lost+found’: Permission denied
bandit6@bandit:/$ cat ./var/lib/dpkg/info/bandit7.password
~~~

## 0x08 - Bandit Level 7 → Level 8

The password for the next level is stored in the file data.txt next to the word millionth

Solution:

~~~ 
bandit7@bandit:~$ ls
data.txt
bandit7@bandit:~$ cat data.txt | grep millionth
~~~

## 0x09 - Bandit Level 8 → Level 9

The password for the next level is stored in the file data.txt and is the only line of text that occurs only once

Solution:

~~~
bandit8@bandit:~$ ls
data.txt
bandit8@bandit:~$ cat data.txt | sort | uniq -u
~~~

## 0x0A - Bandit Level 9 → Level 10

The password for the next level is stored in the file data.txt in one of the few human-readable strings, beginning with several ‘=’ characters.

Solution:

~~~
bandit9@bandit:~$ ls
data.txt
bandit9@bandit:~$ strings data.txt | grep "="
~~~

## 0x0B - Bandit Level 10 → Level 11

The password for the next level is stored in the file data.txt, which contains base64 encoded data

Solution:

~~~
bandit10@bandit:~$ base64 -d data.txt 
~~~

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).


